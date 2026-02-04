#!/usr/bin/env python3
"""
Generate Example Reports for Crisis Communication Framework
This script reads the sample data and generates example reports
that are referenced in the README.

Usage:
    python generate_examples_complete.py

The script will create:
    - media_coverage_report.png
    - sentiment_analysis_report.png
    - crisis_report.pdf

in the examples/sample_data/output/ directory.
"""

import os
import sys
from pathlib import Path

# Add tools directory to path so we can import the modules
tools_dir = Path(__file__).parent / "tools"
sys.path.insert(0, str(tools_dir))

from media_tracker import MediaTracker
from sentiment_analyzer import SentimentAnalyzer
from crisis_report_generator import CrisisReportGenerator


def main():
    """Generate example reports from sample data."""
    
    # Define paths
    base_dir = Path(__file__).parent
    templates_dir = base_dir / "templates"
    output_dir = base_dir / "examples" / "sample_data" / "output"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Media data file
    media_file = templates_dir / "media_coverage_template.csv"
    comments_file = templates_dir / "comments_template.csv"
    
    # Check files exist
    if not media_file.exists():
        print(f"Error: Media data file not found: {media_file}")
        return False
    
    if not comments_file.exists():
        print(f"Error: Comments data file not found: {comments_file}")
        return False
    
    print("Generating example reports...")
    print(f"Input data: {media_file}")
    print(f"Output directory: {output_dir}")
    print()
    
    try:
        # Generate Media Coverage Report
        print("1. Generating Media Coverage Report...")
        tracker = MediaTracker(str(media_file))
        media_output = output_dir / "media_coverage_report.png"
        tracker.export_report(str(media_output))
        print(f"   ✓ Created: {media_output}")
        
        # Generate Sentiment Analysis Report
        print("\n2. Generating Sentiment Analysis Report...")
        analyzer = SentimentAnalyzer(str(comments_file))
        sentiment_output = output_dir / "sentiment_analysis_report.png"
        analyzer.export_report(str(sentiment_output))
        print(f"   ✓ Created: {sentiment_output}")
        
        # Generate Crisis Report PDF
        print("\n3. Generating Crisis Report PDF...")
        crisis_report = CrisisReportGenerator(
            media_file=str(media_file),
            comments_file=str(comments_file),
            crisis_name='Data Security Incident',
            crisis_date='15 January 2024'
        )
        pdf_output = output_dir / "crisis_report.pdf"
        crisis_report.generate_pdf_report(str(pdf_output))
        print(f"   ✓ Created: {pdf_output}")
        
        print("\n✓ Successfully generated all example reports!")
        print(f"\nThe reports are now ready:")
        print(f"  - {media_output.relative_to(base_dir)}")
        print(f"  - {sentiment_output.relative_to(base_dir)}")
        print(f"  - {pdf_output.relative_to(base_dir)}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error generating reports: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)