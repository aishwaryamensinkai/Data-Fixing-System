import pandas as pd
import re
from datetime import datetime

def log_entry(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [{level}] {message}"

def detect_issues(df):
    """
    Detection Agent: Scans data for common issues and returns detailed analysis
    """
    log_entries = []
    log_entries.append(log_entry("Detection Agent Started"))
    
    # Initialize issue tracking
    issues = {
        'malformed_emails': [],
        'duplicates': [],
        'invalid_countries': [],
        'invalid_phones': [],
        'missing_names': [],
        'malformed_names': []
    }
    
    # 1. Email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    malformed_emails = df[~df['email'].astype(str).str.match(email_pattern, na=False)]
    issues['malformed_emails'] = malformed_emails.index.tolist()
    log_entries.append(log_entry(f"Found {len(malformed_emails)} malformed emails"))
    
    # 2. Duplicate detection (considering all columns)
    duplicates = df[df.duplicated(keep='first')]
    issues['duplicates'] = duplicates.index.tolist()
    log_entries.append(log_entry(f"Found {len(duplicates)} duplicate rows"))
    
    # 3. Country validation
    try:
        with open("data/valid_countries.txt") as f:
            valid_countries = [line.strip().lower() for line in f if line.strip()]
        
        invalid_countries = df[~df['country'].astype(str).str.lower().isin(valid_countries)]
        issues['invalid_countries'] = invalid_countries.index.tolist()
        log_entries.append(log_entry(f"Found {len(invalid_countries)} invalid countries"))
    except FileNotFoundError:
        log_entries.append(log_entry("Warning: valid_countries.txt not found", level="WARNING"))
    
    # 4. Phone number validation
    phone_pattern = r'^[\\d\\-\\(\\)\\s\\+]+$'
    invalid_phones = df[~df['phone'].astype(str).str.match(phone_pattern, na=False)]
    issues['invalid_phones'] = invalid_phones.index.tolist()
    log_entries.append(log_entry(f"Found {len(invalid_phones)} invalid phone numbers"))
    
    # 5. Name validation
    missing_names = df[df['name'].isna() | (df['name'].astype(str).str.strip() == '')]
    issues['missing_names'] = missing_names.index.tolist()
    log_entries.append(log_entry(f"Found {len(missing_names)} missing names"))
    
    # Check for names that are too short or contain invalid characters
    name_pattern = r'^[a-zA-Z\\s\\.\\-]+$'
    malformed_names = df[~df['name'].astype(str).str.match(name_pattern, na=False)]
    issues['malformed_names'] = malformed_names.index.tolist()
    log_entries.append(log_entry(f"Found {len(malformed_names)} malformed names"))
    
    # Summary
    total_issues = sum(len(v) for v in issues.values())
    log_entries.append(log_entry(f"Total issues detected: {total_issues}"))
    log_entries.append(log_entry("Detection Agent Completed"))
    
    # Write detailed log
    with open("logs/detection_log.txt", "w") as f:
        f.write("\n".join(log_entries))
    
    return issues
