#!/usr/bin/env python3
"""
Quick test script to generate a single ESG report
Usage: python quick_test_report.py
"""
import asyncio
import pandas as pd
from pathlib import Path
import sys

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.column_matcher import ColumnMatcher, format_data_for_report
from app.report_generator import ReportGenerator
from app.config import settings


async def quick_test():
    """Generate a quick test report"""
    
    print("🚀 ESG Report Generation Quick Test")
    print("=" * 60)
    
    # Configuration
    template_file = "ADX_ESG_Template_v2_10.csv"
    template_type = "ADX_ESG"
    
    # Load template
    print(f"\n📂 Loading template: {template_file}")
    template_path = settings.TEMPLATES_DIR / template_file
    df = pd.read_csv(template_path)
    print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Format data
    print("\n🔄 Formatting data...")
    matcher = ColumnMatcher(template_type)
    formatted_data = format_data_for_report(df, matcher)
    print(f"✅ Formatted {len(formatted_data)} characters of data")
    
    # Prepare metadata
    metadata = {
        "company_name": "Sample Corporation",
        "reporting_period": "2024",
        "template_type": template_type
    }
    
    # Generate PDF report
    print("\n📄 Generating PDF report...")
    generator = ReportGenerator()
    pdf_path = await generator.generate_report(
        data=formatted_data,
        metadata=metadata,
        report_format="pdf",
        report_type="comprehensive",
        output_filename="quick_test_report_pdf"
    )
    print(f"✅ PDF generated: {pdf_path}")
    
    # Generate DOCX report
    print("\n📝 Generating DOCX report...")
    docx_path = await generator.generate_report(
        data=formatted_data,
        metadata=metadata,
        report_format="docx",
        report_type="comprehensive",
        output_filename="quick_test_report_docx"
    )
    print(f"✅ DOCX generated: {docx_path}")
    
    print("\n" + "=" * 60)
    print("🎉 Test completed successfully!")
    print(f"📁 Reports saved in: {settings.REPORTS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(quick_test())
