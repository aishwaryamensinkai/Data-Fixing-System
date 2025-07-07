#!/usr/bin/env python3
"""
🤖 Agent-Based Data Fixing System - Complete Demo
==================================================

This script demonstrates all the capabilities of the enhanced system.
"""

import os
import pandas as pd
import json
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_system():
    """Run a complete demonstration of the system"""
    
    print_header("AGENT-BASED DATA FIXING SYSTEM DEMO")
    print("🚀 This demo showcases all system capabilities")
    
    # 1. Show original data
    print_section("ORIGINAL DATA SAMPLE")
    try:
        original_df = pd.read_csv("data/input.csv")
        print(f"📊 Original data: {len(original_df)} rows")
        print("\nSample of messy data:")
        print(original_df.head(5).to_string(index=False))
    except FileNotFoundError:
        print("❌ Input data not found")
        return
    
    # 2. Run the complete pipeline
    print_section("RUNNING COMPLETE PIPELINE")
    print("🔍 Detection Agent: Scanning for issues...")
    print("🔧 Correction Agent: Fixing detected issues...")
    print("✨ Enrichment Agent: Adding new attributes...")
    print("✅ Validation Agent: Final quality check...")
    
    # Import and run the main pipeline
    from main import main
    main()
    
    # 3. Show cleaned data
    print_section("CLEANED DATA SAMPLE")
    try:
        cleaned_df = pd.read_csv("data/cleaned.csv")
        print(f"📊 Cleaned data: {len(cleaned_df)} rows")
        print(f"📈 New columns added: {len(cleaned_df.columns) - len(original_df.columns)}")
        print("\nSample of cleaned data:")
        print(cleaned_df.head(5).to_string(index=False))
    except FileNotFoundError:
        print("❌ Cleaned data not found")
        return
    
    # 4. Show validation report
    print_section("VALIDATION REPORT")
    try:
        with open("logs/validation_report.json", 'r') as f:
            report = json.load(f)
        
        print(f"📊 Total Rows: {report['total_rows']}")
        print(f"🎯 Quality Score: {report['quality_metrics']['overall_score']:.1f}%")
        print(f"🔧 Total Issues: {report['quality_metrics']['total_issues']}")
        print(f"🔄 Duplicates: {report['duplicates']}")
        
        print("\n📈 Missing Data:")
        for field, count in report['missing_data'].items():
            print(f"  {field}: {count}")
        
        print("\n🔧 Format Issues:")
        for issue, count in report['format_issues'].items():
            print(f"  {issue}: {count}")
            
    except FileNotFoundError:
        print("❌ Validation report not found")
    
    # 5. Show agent logs summary
    print_section("AGENT LOGS SUMMARY")
    log_files = [
        ("detection_log.txt", "🔍 Detection Agent"),
        ("correction_log.txt", "🔧 Correction Agent"),
        ("enrichment_log.txt", "✨ Enrichment Agent"),
        ("validation_log.txt", "✅ Validation Agent")
    ]
    
    for log_file, agent_name in log_files:
        log_path = os.path.join("logs", log_file)
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                content = f.read()
                lines = content.strip().split('\n')
                if lines:
                    print(f"\n{agent_name}:")
                    # Show key metrics from each log
                    for line in lines:
                        if any(keyword in line.lower() for keyword in ['found', 'fixed', 'added', 'total', 'quality']):
                            print(f"  {line}")
    
    # 6. Show data comparison
    print_section("DATA COMPARISON")
    print(f"📊 Original rows: {len(original_df)}")
    print(f"📊 Cleaned rows: {len(cleaned_df)}")
    print(f"📈 Rows removed: {len(original_df) - len(cleaned_df)}")
    print(f"✨ New columns: {len(cleaned_df.columns) - len(original_df.columns)}")
    
    # 7. Show enriched features
    print_section("ENRICHED FEATURES")
    new_columns = [col for col in cleaned_df.columns if col not in original_df.columns]
    print("New columns added:")
    for col in new_columns:
        print(f"  📊 {col}")
    
    # 8. Show email provider distribution
    if 'email_provider' in cleaned_df.columns:
        print_section("EMAIL PROVIDER DISTRIBUTION")
        provider_counts = cleaned_df['email_provider'].value_counts()
        for provider, count in provider_counts.items():
            print(f"  📧 {provider}: {count}")
    
    # 9. Show country distribution
    if 'country_code' in cleaned_df.columns:
        print_section("COUNTRY DISTRIBUTION")
        country_counts = cleaned_df['country_code'].value_counts()
        for country, count in country_counts.items():
            print(f"  🌍 {country}: {count}")
    
    # 10. Show quality metrics
    if 'data_quality_score' in cleaned_df.columns:
        print_section("QUALITY METRICS")
        avg_score = cleaned_df['data_quality_score'].mean()
        min_score = cleaned_df['data_quality_score'].min()
        max_score = cleaned_df['data_quality_score'].max()
        print(f"  📊 Average Quality Score: {avg_score:.1f}%")
        print(f"  📊 Min Quality Score: {min_score:.1f}%")
        print(f"  📊 Max Quality Score: {max_score:.1f}%")
    
    print_header("DEMO COMPLETED SUCCESSFULLY!")
    print("🎉 The Agent-Based Data Fixing System has successfully:")
    print("  ✅ Detected and fixed data quality issues")
    print("  ✅ Enriched data with new attributes")
    print("  ✅ Validated final data quality")
    print("  ✅ Generated comprehensive reports")
    print("\n🚀 Ready for production use!")

if __name__ == "__main__":
    demo_system() 
