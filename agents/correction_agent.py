import pandas as pd
from fuzzywuzzy import process
from datetime import datetime
import re

def log_entry(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [{level}] {message}"

def correct_issues(df, issues):
    """
    Correction Agent: Fixes detected issues using various correction strategies
    """
    log_entries = []
    log_entries.append(log_entry("Correction Agent Started"))
    corrections_made = 0
    
    # 1. Remove duplicates
    original_count = len(df)
    df = df.drop_duplicates(keep='first')
    duplicates_removed = original_count - len(df)
    if duplicates_removed > 0:
        log_entries.append(log_entry(f"Removed {duplicates_removed} duplicate rows"))
        corrections_made += duplicates_removed
    
    # 2. Fix malformed emails
    for idx in issues.get('malformed_emails', []):
        if idx in df.index:
            original_email = df.at[idx, 'email']
            fixed_email = fix_email(original_email)
            df.at[idx, 'email'] = fixed_email
            log_entries.append(log_entry(f"Fixed email at row {idx}: '{original_email}' -> '{fixed_email}'"))
            corrections_made += 1
    
    # 3. Fix invalid countries using fuzzy matching
    try:
        with open("data/valid_countries.txt") as f:
            valid_countries = [line.strip() for line in f if line.strip()]
        
        for idx in issues.get('invalid_countries', []):
            if idx in df.index:
                original_country = df.at[idx, 'country']
                best_match, confidence = process.extractOne(str(original_country), valid_countries)
                if confidence > 70:
                    df.at[idx, 'country'] = best_match
                    log_entries.append(log_entry(f"Fixed country at row {idx}: '{original_country}' -> '{best_match}' (confidence: {confidence}%)"))
                    corrections_made += 1
                else:
                    log_entries.append(log_entry(f"Could not find good match for country '{original_country}' at row {idx} (best: '{best_match}', confidence: {confidence}%)", level="WARNING"))
    except FileNotFoundError:
        log_entries.append(log_entry("Warning: valid_countries.txt not found - skipping country corrections", level="WARNING"))
    
    # 4. Fix invalid phone numbers
    for idx in issues.get('invalid_phones', []):
        if idx in df.index:
            original_phone = df.at[idx, 'phone']
            fixed_phone = fix_phone_number(original_phone)
            df.at[idx, 'phone'] = fixed_phone
            log_entries.append(log_entry(f"Fixed phone at row {idx}: '{original_phone}' -> '{fixed_phone}'"))
            corrections_made += 1
    
    # 5. Fix missing names
    for idx in issues.get('missing_names', []):
        if idx in df.index:
            df.at[idx, 'name'] = 'Unknown'
            log_entries.append(log_entry(f"Fixed missing name at row {idx}: set to 'Unknown'"))
            corrections_made += 1
    
    # 6. Fix malformed names
    for idx in issues.get('malformed_names', []):
        if idx in df.index:
            original_name = df.at[idx, 'name']
            fixed_name = fix_name(original_name)
            df.at[idx, 'name'] = fixed_name
            log_entries.append(log_entry(f"Fixed name at row {idx}: '{original_name}' -> '{fixed_name}'"))
            corrections_made += 1
    
    log_entries.append(log_entry(f"Total corrections made: {corrections_made}"))
    log_entries.append(log_entry("Correction Agent Completed"))
    
    with open("logs/correction_log.txt", "w") as f:
        f.write("\n".join(log_entries))
    
    return df

def fix_email(email):
    """Fix common email formatting issues"""
    if pd.isna(email) or email == '':
        return 'unknown@domain.com'
    
    email = str(email)
    
    # Replace [at] with @
    email = email.replace('[at]', '@')
    
    # Remove spaces
    email = email.replace(' ', '')
    
    # Basic validation
    if '@' in email and '.' in email.split('@')[1]:
        return email
    else:
        return 'invalid@domain.com'

def fix_phone_number(phone):
    """Fix common phone number formatting issues"""
    if pd.isna(phone) or phone == '':
        return '000-000-0000'
    
    phone = str(phone)
    
    # Remove all non-digit characters
    digits = re.sub(r'[^\d]', '', phone)
    
    # Format as XXX-XXX-XXXX
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        return '000-000-0000'

def fix_name(name):
    """Fix common name formatting issues"""
    if pd.isna(name) or name == '':
        return 'Unknown'
    
    name = str(name)
    
    # Remove extra spaces and capitalize properly
    name = ' '.join(name.split())
    name = name.title()
    
    # Remove invalid characters
    name = re.sub(r'[^a-zA-Z\s\.\-]', '', name)
    
    if len(name.strip()) < 2:
        return 'Unknown'
    
    return name.strip()
