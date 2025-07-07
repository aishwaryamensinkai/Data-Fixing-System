import pandas as pd
import os
from datetime import datetime
from agents.detection_agent import detect_issues
from agents.correction_agent import correct_issues
from agents.enrichment_agent import enrich_data
from agents.validation_agent import validate_data

def main(input_file="data/input.csv", output_file="data/cleaned.csv"):
    """
    Main pipeline that orchestrates all agents in sequence
    """
    print("🚀 Starting Agent-Based Data Fixing System")
    print("=" * 50)
    
    # Ensure output directories exist
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Load data
    try:
        df = pd.read_csv(input_file)
        print(f"📊 Loaded {len(df)} rows from {input_file}")
    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_file}")
        return
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Agent 1: Detection
    print("\n🔍 Detection Agent: Scanning for issues...")
    issues = detect_issues(df)
    
    # Agent 2: Correction
    print("🔧 Correction Agent: Fixing detected issues...")
    df = correct_issues(df, issues)
    
    # Agent 3: Enrichment
    print("✨ Enrichment Agent: Adding new attributes...")
    df = enrich_data(df)
    
    # Agent 4: Validation
    print("✅ Validation Agent: Final quality check...")
    validation_results = validate_data(df)
    
    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"\n💾 Cleaned data saved to {output_file}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("📈 CLEANING SUMMARY")
    print("=" * 50)
    print(f"Original rows: {len(pd.read_csv(input_file))}")
    print(f"Final rows: {len(df)}")
    print(f"Quality score: {validation_results['quality_metrics']['overall_score']:.1f}%")
    print(f"Total issues found: {validation_results['quality_metrics']['total_issues']}")
    
    if validation_results['recommendations']:
        print("\n💡 Recommendations:")
        for rec in validation_results['recommendations']:
            print(f"  - {rec}")
    
    print(f"\n📋 Check logs/ directory for detailed agent logs")
    print("✅ Pipeline completed successfully!")

if __name__ == "__main__":
    main()
