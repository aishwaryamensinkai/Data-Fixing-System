import os
import pandas as pd
import json
from main import main

def display_banner():
    """Display system banner"""
    print("=" * 60)
    print("🤖 MINI AGENT-BASED DATA FIXING SYSTEM")
    print("=" * 60)
    print("Powered by intelligent agents for data cleaning and enrichment")
    print("=" * 60)

def view_logs():
    """Display all available logs"""
    log_files = [
        "detection_log.txt",
        "correction_log.txt", 
        "enrichment_log.txt",
        "validation_log.txt"
    ]
    
    print("\n📋 AGENT LOGS")
    print("-" * 40)
    
    for log_file in log_files:
        path = os.path.join("logs", log_file)
        if os.path.exists(path):
            print(f"\n📄 {log_file.upper()}")
            print("-" * 30)
            with open(path, 'r') as f:
                content = f.read()
                print(content)
        else:
            print(f"\n❌ {log_file} not found")

def view_validation_report():
    """Display validation report"""
    report_path = os.path.join("logs", "validation_report.json")
    if os.path.exists(report_path):
        print("\n📊 VALIDATION REPORT")
        print("-" * 40)
        
        with open(report_path, 'r') as f:
            report = json.load(f)
        
        print(f"Total Rows: {report['total_rows']}")
        print(f"Quality Score: {report['quality_metrics']['overall_score']:.1f}%")
        print(f"Total Issues: {report['quality_metrics']['total_issues']}")
        print(f"Duplicates: {report['duplicates']}")
        
        print("\n📈 Missing Data:")
        for field, count in report['missing_data'].items():
            print(f"  {field}: {count}")
        
        print("\n🔧 Format Issues:")
        for issue, count in report['format_issues'].items():
            print(f"  {issue}: {count}")
        
        if report['recommendations']:
            print("\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"  - {rec}")
    else:
        print("❌ Validation report not found. Run the pipeline first.")

def compare_data():
    """Compare original vs cleaned data"""
    try:
        original = pd.read_csv("data/input.csv")
        cleaned = pd.read_csv("data/cleaned.csv")
        
        print("\n📊 DATA COMPARISON")
        print("-" * 40)
        print(f"Original rows: {len(original)}")
        print(f"Cleaned rows: {len(cleaned)}")
        print(f"Rows removed: {len(original) - len(cleaned)}")
        
        # Show sample of cleaned data
        print("\n📋 Sample of cleaned data:")
        print(cleaned.head(5).to_string(index=False))
        
    except FileNotFoundError:
        print("❌ Data files not found. Run the pipeline first.")

def start_web_interface():
    """Start the web interface"""
    try:
        from agents.web_agent import start_web_server
        print("\n🌐 Starting web interface...")
        print("📁 Open your browser and go to http://localhost:5000")
        print("📤 Upload your CSV file and process it through the web interface")
        print("⏹️  Press Ctrl+C to stop the web server")
        start_web_server()
    except ImportError:
        print("❌ Flask not installed. Install with: pip install flask")
    except KeyboardInterrupt:
        print("\n👋 Web server stopped.")

def cli():
    """Main CLI interface"""
    display_banner()
    
    while True:
        print("\n🎯 OPTIONS:")
        print("1. 🚀 Run Complete Cleaning Pipeline")
        print("2. 📋 View Agent Logs")
        print("3. 📊 View Validation Report")
        print("4. 📈 Compare Original vs Cleaned Data")
        print("5. 📁 View Sample Data")
        print("6. 🌐 Start Web Interface")
        print("7. ❌ Exit")

        choice = input("\nChoose an option (1-7): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting pipeline...")
            main()
            
        elif choice == "2":
            view_logs()
            
        elif choice == "3":
            view_validation_report()
            
        elif choice == "4":
            compare_data()
            
        elif choice == "5":
            try:
                print("\n📁 SAMPLE INPUT DATA:")
                print("-" * 40)
                df = pd.read_csv("data/input.csv")
                print(df.head(10).to_string(index=False))
                
                if os.path.exists("data/cleaned.csv"):
                    print("\n📁 SAMPLE CLEANED DATA:")
                    print("-" * 40)
                    cleaned_df = pd.read_csv("data/cleaned.csv")
                    print(cleaned_df.head(10).to_string(index=False))
            except FileNotFoundError:
                print("❌ Data files not found")
                
        elif choice == "6":
            start_web_interface()
            
        elif choice == "7":
            print("\n👋 Goodbye! Thanks for using the Agent-Based Data Fixing System!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    cli()
