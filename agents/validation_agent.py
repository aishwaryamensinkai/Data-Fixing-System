import pandas as pd
import re
from datetime import datetime
import json
import numpy as np

def log_entry(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [{level}] {message}"

def validate_data(df):
    """
    Validation Agent: Performs final quality checks and generates comprehensive reports
    """
    log_entries = []
    log_entries.append(log_entry("Validation Agent Started"))
    
    # Initialize validation results
    validation_results = {
        'total_rows': len(df),
        'duplicates': 0,
        'missing_data': {},
        'format_issues': {},
        'quality_metrics': {},
        'recommendations': [],
        'summary': {}
    }
    
    # 1. Check for remaining duplicates
    duplicates = df[df.duplicated(keep='first')]
    validation_results['duplicates'] = len(duplicates)
    if len(duplicates) > 0:
        log_entries.append(log_entry(f"WARNING: {len(duplicates)} duplicate rows still present", level="WARNING"))
        validation_results['recommendations'].append("Remove remaining duplicate rows")
    else:
        log_entries.append(log_entry("No duplicate rows found"))
    
    # 2. Check for missing data
    for column in ['name', 'email', 'phone', 'country']:
        missing_count = df[column].isna().sum()
        validation_results['missing_data'][column] = int(missing_count)  # Convert to regular int
        if missing_count > 0:
            log_entries.append(log_entry(f"WARNING: {missing_count} missing values in {column}", level="WARNING"))
        else:
            log_entries.append(log_entry(f"No missing values in {column}"))
    
    # 3. Check format issues
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    invalid_emails = df[~df['email'].astype(str).str.match(email_pattern, na=False)]
    validation_results['format_issues']['invalid_emails'] = int(len(invalid_emails))
    
    phone_pattern = r'^\d{3}-\d{3}-\d{4}$'
    invalid_phones = df[~df['phone'].astype(str).str.match(phone_pattern, na=False)]
    validation_results['format_issues']['invalid_phones'] = int(len(invalid_phones))
    
    if len(invalid_emails) > 0:
        log_entries.append(log_entry(f"WARNING: {len(invalid_emails)} invalid email formats", level="WARNING"))
    else:
        log_entries.append(log_entry("All email formats are valid"))
    
    if len(invalid_phones) > 0:
        log_entries.append(log_entry(f"WARNING: {len(invalid_phones)} invalid phone formats", level="WARNING"))
    else:
        log_entries.append(log_entry("All phone formats are valid"))
    
    # 4. Calculate quality metrics
    total_issues = sum(validation_results['missing_data'].values()) + sum(validation_results['format_issues'].values())
    quality_score = max(0, 100 - (total_issues / len(df) * 100))
    validation_results['quality_metrics']['overall_score'] = float(quality_score)
    validation_results['quality_metrics']['total_issues'] = int(total_issues)
    
    # 5. Generate recommendations
    if quality_score < 80:
        validation_results['recommendations'].append("Data quality is below 80% - consider additional cleaning")
    
    if validation_results['missing_data']['email'] > 0:
        validation_results['recommendations'].append("Consider email validation service for missing emails")
    
    if validation_results['missing_data']['phone'] > 0:
        validation_results['recommendations'].append("Consider phone number validation service")
    
    # 6. Data distribution analysis
    validation_results['distributions'] = {
        'countries': df['country'].value_counts().to_dict(),
        'email_providers': df['email_provider'].value_counts().to_dict() if 'email_provider' in df.columns else {},
        'phone_types': df['phone_type'].value_counts().to_dict() if 'phone_type' in df.columns else {}
    }
    
    # Convert numpy types to regular Python types for JSON serialization
    for key in validation_results['distributions']:
        if validation_results['distributions'][key]:
            validation_results['distributions'][key] = {
                str(k): int(v) for k, v in validation_results['distributions'][key].items()
            }
    
    # 7. Summary statistics
    log_entries.append(log_entry("\n=== VALIDATION SUMMARY ==="))
    log_entries.append(log_entry(f"Total rows: {validation_results['total_rows']}"))
    log_entries.append(log_entry(f"Overall quality score: {quality_score:.1f}%"))
    log_entries.append(log_entry(f"Total issues found: {total_issues}"))
    log_entries.append(log_entry(f"Remaining duplicates: {validation_results['duplicates']}"))
    
    if validation_results['recommendations']:
        log_entries.append(log_entry("\n=== RECOMMENDATIONS ==="))
        for rec in validation_results['recommendations']:
            log_entries.append(log_entry(f"- {rec}"))
    
    log_entries.append(log_entry("Validation Agent Completed"))
    
    # Write detailed log
    with open("logs/validation_log.txt", "w") as f:
        f.write("\n".join(log_entries))
    
    # Write validation report as JSON
    with open("logs/validation_report.json", "w") as f:
        json.dump(validation_results, f, indent=2)
    
    # After calculating quality_score, total_issues, etc.
    validation_results['summary'] = {
        'total_rows': validation_results['total_rows'],
        'quality_score': validation_results['quality_metrics']['overall_score'],
        'total_issues': validation_results['quality_metrics']['total_issues'],
        'remaining_duplicates': validation_results['duplicates']
    }
    
    return validation_results 
