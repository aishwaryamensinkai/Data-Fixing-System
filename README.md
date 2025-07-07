# 🤖 Mini Agent-Based Data Fixing System

## 📋 Overview

This project implements a sophisticated agent-based data cleaning and enrichment system that processes messy CSV files containing customer records. The system uses multiple specialized agents that work together to detect, correct, enrich, and validate data quality issues.

## 🧠 Agent Architecture

### 1. **Detection Agent** 🔍

- **Purpose**: Scans data for common quality issues
- **Capabilities**:
  - Email format validation
  - Duplicate row detection
  - Country name validation
  - Phone number format checking
  - Name validation and formatting issues
  - Missing data identification

### 2. **Correction Agent** 🔧

- **Purpose**: Fixes detected issues using intelligent correction strategies
- **Capabilities**:
  - Email format correction (fixes `[at]` syntax, removes spaces)
  - Duplicate removal with configurable strategies
  - Country name correction using fuzzy matching
  - Phone number standardization (XXX-XXX-XXXX format)
  - Name formatting and validation
  - Missing data handling

### 3. **Enrichment Agent** ✨

- **Purpose**: Adds new useful attributes and enhances existing data
- **Capabilities**:
  - Email domain extraction
  - Email provider classification (Gmail, Yahoo, etc.)
  - Phone number type classification
  - Country code mapping
  - Name analysis (length, word count)
  - Data quality scoring
  - First/last name extraction
  - Validity flags for emails and phones

### 4. **Validation Agent** ✅

- **Purpose**: Performs final quality checks and generates comprehensive reports
- **Capabilities**:
  - Final duplicate detection
  - Missing data analysis
  - Format validation
  - Quality score calculation
  - Data distribution analysis
  - Recommendations generation
  - JSON report generation

## 🚀 Features

### Core Features

- **Modular Agent Design**: Each agent operates independently and can be run separately
- **Comprehensive Logging**: Detailed logs for each agent with timestamps
- **Error Handling**: Robust error handling with graceful degradation
- **Data Quality Scoring**: Automatic quality assessment with recommendations
- **Fuzzy Matching**: Intelligent country name correction using fuzzy string matching

### Enhanced Features

- **Interactive CLI**: User-friendly command-line interface with multiple options
- **Data Comparison**: Side-by-side comparison of original vs cleaned data
- **Validation Reports**: Detailed JSON reports with quality metrics
- **Sample Data**: Built-in sample data with various quality issues
- **Extensible Design**: Easy to add new agents or modify existing ones

## 📊 Sample Data Issues

The system handles various data quality issues including:

- **Email Issues**: `[at]` syntax, missing @ symbols, invalid domains
- **Phone Issues**: Inconsistent formats, missing numbers, invalid characters
- **Country Issues**: Typos (Indai → India), abbreviations (US → United States)
- **Name Issues**: Missing names, malformed characters, inconsistent formatting
- **Duplicate Data**: Exact and near-duplicate detection and removal

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/aishwaryamensinkai/Data-Fixing-System.git
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the system**:
   ```bash
   python cli.py
   ```

## 📖 Usage

### Quick Start

```bash
# Run the complete pipeline
python main.py

# Or use the interactive CLI
python cli.py

# Or use the web interface
python agents/web_agent.py
```

### CLI Options

1. **Run Complete Cleaning Pipeline**: Processes the input CSV through all agents
2. **View Agent Logs**: Display detailed logs from each agent
3. **View Validation Report**: Show comprehensive quality metrics
4. **Compare Data**: Side-by-side comparison of original vs cleaned data
5. **View Sample Data**: Preview input and output data samples
6. **Exit**: Close the application

### Programmatic Usage

```python
from main import main

# Run with default files
main()

# Run with custom files
main("path/to/input.csv", "path/to/output.csv")
```

## 📁 File Structure

```
data_fixing_system/
├── agents/
│   ├── detection_agent.py      # Issue detection logic
│   ├── correction_agent.py     # Data correction logic
│   ├── enrichment_agent.py     # Data enrichment logic
│   └── validation_agent.py     # Quality validation logic
├── data/
│   ├── input.csv              # Sample input data (50 rows)
│   ├── cleaned.csv            # Output cleaned data
│   └── valid_countries.txt    # Valid country names
├── logs/
│   ├── detection_log.txt      # Detection agent logs
│   ├── correction_log.txt     # Correction agent logs
│   ├── enrichment_log.txt     # Enrichment agent logs
│   ├── validation_log.txt     # Validation agent logs
│   └── validation_report.json # Detailed validation report
├── main.py                    # Main pipeline orchestration
├── cli.py                     # Interactive CLI interface
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 📈 Output Data

The cleaned data includes all original columns plus enriched fields:

- `email_domain`: Extracted email domain
- `email_provider`: Classified email provider (Gmail, Yahoo, etc.)
- `phone_type`: Phone number classification
- `country_code`: Standardized country codes
- `name_length`: Length of name field
- `name_word_count`: Number of words in name
- `first_name`: Extracted first name
- `last_name`: Extracted last name
- `data_quality_score`: Quality score (0-100)
- `email_valid`: Boolean email validity flag
- `phone_valid`: Boolean phone validity flag

## 🔧 Configuration

### Valid Countries File

Create `data/valid_countries.txt` with one country per line:

```
United States
Canada
Mexico
India
Germany
France
...
```

### Custom Input Data

Place your CSV file in the `data/` directory and update the file path in `main.py` or use the CLI interface.

## 📊 Quality Metrics

The system provides comprehensive quality metrics:

- **Overall Quality Score**: Percentage-based quality assessment
- **Issue Breakdown**: Detailed count of each type of issue
- **Data Distribution**: Analysis of country, email provider, and phone type distributions
- **Recommendations**: Actionable suggestions for further improvement

## 🎯 Example Output

### Before Cleaning

```
id,name,email,phone,country
1,Alice Smith,alice.smith[at]email.com,,USA
2,Bob Johnson,bob.johnson@email.com,123-456-7890,U.S.A
3,Charlie Brown,,456-789-1230,Indai
```

### After Cleaning

```
id,name,email,phone,country,email_domain,email_provider,phone_type,country_code,data_quality_score,email_valid,phone_valid
1,Alice Smith,alice.smith@email.com,000-000-0000,United States,email.com,Other,missing,US,75,True,False
2,Bob Johnson,bob.johnson@email.com,123-456-7890,United States,email.com,Other,standard,US,100,True,True
3,Charlie Brown,unknown@domain.com,456-789-1230,India,domain.com,Other,standard,IN,85,False,True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Built with ❤️ using Python and intelligent agent architecture**

### Web Interface

To use the web interface:

```bash
python agents/web_agent.py
```

Then open your browser and go to [http://localhost:5000](http://localhost:5000).
Upload a CSV, process it, and view/download results.
