import pandas as pd
import re
from datetime import datetime
import requests
import json

def log_entry(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [{level}] {message}"

def enrich_data(df):
    """
    Enrichment Agent: Adds new useful attributes and enhances existing data
    """
    log_entries = []
    log_entries.append(log_entry("Enrichment Agent Started"))
    enrichments_made = 0
    
    # 1. Extract email domain
    df["email_domain"] = df["email"].str.extract(r'@(\S+)$')
    log_entries.append(log_entry("Added email_domain column"))
    enrichments_made += 1
    
    # 2. Fill missing phone numbers with placeholder
    missing_phones = df['phone'].isna().sum()
    df = df.copy()
    df['phone'] = df['phone'].fillna('000-000-0000')
    log_entries.append(log_entry(f"Filled {missing_phones} missing phone numbers"))
    enrichments_made += missing_phones
    
    # 3. Add phone number type classification
    df['phone_type'] = df['phone'].apply(classify_phone_type)
    log_entries.append(log_entry("Added phone_type classification"))
    enrichments_made += 1
    
    # 4. Add name length and word count
    df['name_length'] = df['name'].str.len()
    df['name_word_count'] = df['name'].str.split().str.len()
    log_entries.append(log_entry("Added name analysis columns"))
    enrichments_made += 2
    
    # 5. Add country code based on country name
    df['country_code'] = df['country'].apply(get_country_code)
    log_entries.append(log_entry("Added country_code column"))
    enrichments_made += 1
    
    # 6. Add data quality score
    df['data_quality_score'] = df.apply(calculate_quality_score, axis=1)
    log_entries.append(log_entry("Added data_quality_score column"))
    enrichments_made += 1
    
    # 7. Add email validity flag
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    df['email_valid'] = df['email'].astype(str).str.match(email_pattern, na=False)
    log_entries.append(log_entry("Added email_valid flag"))
    enrichments_made += 1
    
    # 8. Add phone validity flag
    phone_pattern = r'^\d{3}-\d{3}-\d{4}$'
    df['phone_valid'] = df['phone'].astype(str).str.match(phone_pattern, na=False)
    log_entries.append(log_entry("Added phone_valid flag"))
    enrichments_made += 1
    
    # 9. Add full name (first + last) extraction
    df['first_name'] = df['name'].str.split().str[0]
    df['last_name'] = df['name'].str.split().str[-1]
    log_entries.append(log_entry("Added first_name and last_name columns"))
    enrichments_made += 2
    
    # 10. Add email provider classification
    df['email_provider'] = df['email_domain'].apply(classify_email_provider)
    log_entries.append(log_entry("Added email_provider classification"))
    enrichments_made += 1
    
    log_entries.append(log_entry(f"Total enrichments made: {enrichments_made}"))
    log_entries.append(log_entry("Enrichment Agent Completed"))
    
    with open("logs/enrichment_log.txt", "w") as f:
        f.write("\n".join(log_entries))
    
    return df

def classify_phone_type(phone):
    """Classify phone number type"""
    if pd.isna(phone) or phone == '':
        return 'unknown'
    
    phone = str(phone)
    digits = re.sub(r'[^\d]', '', phone)
    
    if len(digits) == 10:
        return 'standard'
    elif len(digits) == 11 and digits[0] == '1':
        return 'international'
    elif len(digits) == 0:
        return 'missing'
    else:
        return 'invalid'

def get_country_code(country):
    """Get country code from country name"""
    country_mapping = {
        'united states': 'US',
        'usa': 'US',
        'u.s.a': 'US',
        'us': 'US',
        'india': 'IN',
        'canada': 'CA',
        'mexico': 'MX',
        'france': 'FR',
        'germany': 'DE',
        'brazil': 'BR',
        'united kingdom': 'UK',
        'uk': 'UK',
        'australia': 'AU',
        'japan': 'JP',
        'china': 'CN'
    }
    
    if pd.isna(country):
        return 'UNKNOWN'
    
    return country_mapping.get(str(country).lower(), 'UNKNOWN')

def calculate_quality_score(row):
    """Calculate data quality score for a row"""
    score = 100
    
    # Deduct points for missing or invalid data
    if pd.isna(row['name']) or row['name'] == '':
        score -= 30
    if pd.isna(row['email']) or row['email'] == '':
        score -= 25
    if pd.isna(row['phone']) or row['phone'] == '':
        score -= 20
    if pd.isna(row['country']) or row['country'] == '':
        score -= 15
    
    # Deduct points for invalid formats
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not pd.isna(row['email']) and not re.match(email_pattern, str(row['email'])):
        score -= 10
    
    phone_pattern = r'^\d{3}-\d{3}-\d{4}$'
    if not pd.isna(row['phone']) and not re.match(phone_pattern, str(row['phone'])):
        score -= 10
    
    return max(0, score)

def classify_email_provider(domain):
    """Classify email provider"""
    if pd.isna(domain):
        return 'unknown'
    
    domain = str(domain).lower()
    
    providers = {
        'gmail.com': 'Google',
        'yahoo.com': 'Yahoo',
        'outlook.com': 'Microsoft',
        'hotmail.com': 'Microsoft',
        'icloud.com': 'Apple',
        'aol.com': 'AOL',
        'protonmail.com': 'ProtonMail'
    }
    
    return providers.get(domain, 'Other')
