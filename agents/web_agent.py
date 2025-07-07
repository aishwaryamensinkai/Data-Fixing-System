import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from datetime import datetime
import json
from flask import Flask, render_template, request, jsonify, send_file
import tempfile

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

# Global variable to store current session data
session_data = {
    'input_file': None,
    'output_file': None,
    'validation_results': None,
    'logs': {}
}

def create_web_interface():
    """Create a simple web interface for the data fixing system"""
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Please upload a CSV file'}), 400
        
        # Save uploaded file
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, 'input.csv')
        file.save(input_path)
        
        session_data['input_file'] = input_path
        session_data['output_file'] = os.path.join(temp_dir, 'cleaned.csv')
        
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})
    
    @app.route('/process', methods=['POST'])
    def process_data():
        if not session_data['input_file']:
            return jsonify({'error': 'No file uploaded'}), 400
        
        try:
            # Import here to avoid circular imports
            from main import main
            
            # Process the data
            main(session_data['input_file'], session_data['output_file'])
            
            # Read results
            df = pd.read_csv(session_data['output_file'])
            
            # Load validation results
            validation_path = os.path.join('logs', 'validation_report.json')
            if os.path.exists(validation_path):
                with open(validation_path, 'r') as f:
                    session_data['validation_results'] = json.load(f)
            
            # Load logs
            log_files = ['detection_log.txt', 'correction_log.txt', 'enrichment_log.txt', 'validation_log.txt']
            for log_file in log_files:
                log_path = os.path.join('logs', log_file)
                if os.path.exists(log_path):
                    with open(log_path, 'r') as f:
                        session_data['logs'][log_file] = f.read()
            
            # Extract summary from validation results
            summary = {}
            validation = session_data['validation_results']
            if validation and 'summary' in validation:
                summary = validation['summary']
            elif validation and 'quality_metrics' in validation:
                summary = {
                    'total_rows': validation.get('total_rows'),
                    'quality_score': validation['quality_metrics'].get('overall_score'),
                    'total_issues': validation['quality_metrics'].get('total_issues'),
                    'remaining_duplicates': validation.get('duplicates')
                }
            
            return jsonify({
                'message': 'Processing completed successfully',
                'rows_processed': len(df),
                'columns': list(df.columns),
                'validation': session_data['validation_results'],
                'logs': session_data['logs'],
                'summary': summary
            })
            
        except Exception as e:
            return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    
    @app.route('/results')
    def get_results():
        if not session_data['output_file'] or not os.path.exists(session_data['output_file']):
            return jsonify({'error': 'No results available'}), 400
        
        try:
            df = pd.read_csv(session_data['output_file'])
            
            # Extract summary from validation results
            summary = {}
            validation = session_data['validation_results']
            if validation and 'summary' in validation:
                summary = validation['summary']
            elif validation and 'quality_metrics' in validation:
                summary = {
                    'total_rows': validation.get('total_rows'),
                    'quality_score': validation['quality_metrics'].get('overall_score'),
                    'total_issues': validation['quality_metrics'].get('total_issues'),
                    'remaining_duplicates': validation.get('duplicates')
                }
            
            return jsonify({
                'data': df.head(20).to_dict('records'),
                'total_rows': len(df),
                'columns': list(df.columns),
                'validation': session_data['validation_results'],
                'logs': session_data['logs'],
                'summary': summary
            })
        except Exception as e:
            return jsonify({'error': f'Error reading results: {str(e)}'}), 500
    
    @app.route('/download')
    def download_results():
        if not session_data['output_file'] or not os.path.exists(session_data['output_file']):
            return jsonify({'error': 'No results available'}), 400
        
        return send_file(session_data['output_file'], as_attachment=True, download_name='cleaned_data.csv')
    
    return app

def start_web_server(host='localhost', port=5050, debug=True):
    """Start the web server"""
    app = create_web_interface()
    
    # Create templates directory and HTML template
    os.makedirs('templates', exist_ok=True)
    
    html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Data Fixing System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .upload-section { border: 2px dashed #ccc; padding: 20px; text-align: center; margin: 20px 0; }
        .results-section { margin: 20px 0; }
        .log-section { background: #f5f5f5; padding: 10px; margin: 10px 0; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        button { background: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Data Fixing System</h1>
        
        <div class="upload-section">
            <h2>Upload CSV File</h2>
            <input type="file" id="csvFile" accept=".csv">
            <button onclick="uploadFile()">Upload</button>
            <button onclick="processData()" id="processBtn" disabled>Process Data</button>
        </div>
        
        <div class="results-section" id="resultsSection" style="display: none;">
            <h2>Results</h2>
            <button onclick="downloadResults()">Download Cleaned Data</button>
            <div id="resultsTable"></div>
        </div>
        
        <div class="log-section" id="logSection" style="display: none;">
            <h2>Processing Logs</h2>
            <div id="logs"></div>
        </div>
    </div>
    
    <script>
        function uploadFile() {
            const fileInput = document.getElementById('csvFile');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a file');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    alert('File uploaded successfully!');
                    document.getElementById('processBtn').disabled = false;
                }
            })
            .catch(error => {
                alert('Error uploading file: ' + error);
            });
        }
        
        function processData() {
            fetch('/process', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    alert('Processing completed!');
                    loadResults();
                }
            })
            .catch(error => {
                alert('Error processing data: ' + error);
            });
        }
        
        function loadResults() {
            fetch('/results')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    displayResults(data);
                }
            })
            .catch(error => {
                alert('Error loading results: ' + error);
            });
        }
        
        function displayResults(data) {
            const resultsSection = document.getElementById('resultsSection');
            const logSection = document.getElementById('logSection');
            
            // Display data table
            let tableHtml = '<table><tr>';
            data.columns.forEach(col => {
                tableHtml += '<th>' + col + '</th>';
            });
            tableHtml += '</tr>';
            
            data.data.forEach(row => {
                tableHtml += '<tr>';
                data.columns.forEach(col => {
                    tableHtml += '<td>' + (row[col] || '') + '</td>';
                });
                tableHtml += '</tr>';
            });
            tableHtml += '</table>';
            
            document.getElementById('resultsTable').innerHTML = tableHtml;
            resultsSection.style.display = 'block';
            
            // Display logs
            let logsHtml = '';
            for (const [logFile, logContent] of Object.entries(data.logs)) {
                logsHtml += '<h3>' + logFile + '</h3>';
                logsHtml += '<pre>' + logContent + '</pre>';
            }
            document.getElementById('logs').innerHTML = logsHtml;
            logSection.style.display = 'block';
        }
        
        function downloadResults() {
            window.location.href = '/download';
        }
    </script>
</body>
</html>
    '''
    
    # with open('templates/index.html', 'w') as f:
    #     f.write(html_template)
    
    print(f"🌐 Starting web server at http://{host}:{port}")
    print("📁 Upload your CSV file and process it through the web interface")
    
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    start_web_server() 
