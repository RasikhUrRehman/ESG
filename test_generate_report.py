#!/usr/bin/env python3
"""
Test script to generate ESG reports locally using templates
This bypasses the API and generates reports directly from template files
"""
import asyncio
import pandas as pd
from pathlib import Path
import logging
import sys

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.column_matcher import ColumnMatcher, format_data_for_report, calculate_change_analysis
from app.report_generator import ReportGenerator
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_generate_report_from_template(
    template_name: str = "ADX_ESG_Template_v2_10",
    report_format: str = "pdf",
    report_type: str = "comprehensive"
):
    """
    Generate a test ESG report from a template file
    
    Args:
        template_name: Name of the template (without .csv extension)
        report_format: Output format (pdf or docx)
        report_type: Type of report (comprehensive, executive, technical)
    """
    try:
        logger.info(f"Starting report generation test with template: {template_name}")
        
        # Step 1: Load the template file
        template_path = settings.TEMPLATES_DIR / f"{template_name}.csv"
        if not template_path.exists():
            logger.error(f"Template file not found: {template_path}")
            return
        
        logger.info(f"Loading template from: {template_path}")
        df = pd.read_csv(template_path)
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        
        # Display first few rows
        logger.info("Template data preview:")
        print(df.head())
        print("\nColumns:", df.columns.tolist())
        
        # Step 2: Initialize the column matcher
        # Extract base template type (e.g., "ADX_ESG" from "ADX_ESG_Template_v2_10")
        template_type = template_name.replace("_Template_v2_10", "")
        if template_type not in settings.AVAILABLE_TEMPLATES:
            # Try matching with available templates
            for avail in settings.AVAILABLE_TEMPLATES:
                if avail in template_name or template_name.startswith(avail):
                    template_type = avail
                    break
        
        logger.info(f"Using template type: {template_type}")
        matcher = ColumnMatcher(template_type)
        
        # Step 3: Format data for report
        logger.info("Formatting data for report...")
        formatted_data = format_data_for_report(df, matcher)
        logger.info(f"Formatted data length: {len(formatted_data)}")
        
        # Step 4: Calculate change analysis
        logger.info("Calculating change analysis...")
        change_analysis = calculate_change_analysis(df)
        logger.info(f"Change analysis items: {len(change_analysis)}")
        
        # Step 5: Prepare metadata
        metadata = {
            "company_name": "Test Company Ltd.",
            "reporting_period": "2024",
            "template_type": template_type,
            "total_metrics": len(df),
            "generation_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Step 6: Generate the report
        logger.info(f"Generating {report_format.upper()} report...")
        report_generator = ReportGenerator()
        
        output_filename = f"test_report_{template_type}_{report_format}"
        
        report_path = await report_generator.generate_report(
            data=formatted_data,
            metadata=metadata,
            report_format=report_format,
            report_type=report_type,
            output_filename=output_filename
        )
        
        logger.info(f"✅ Report generated successfully: {report_path}")
        logger.info(f"File size: {Path(report_path).stat().st_size / 1024:.2f} KB")
        
        return report_path
        
    except Exception as e:
        logger.error(f"❌ Error generating report: {e}", exc_info=True)
        raise


async def test_all_templates():
    """Test report generation for all available templates"""
    templates = [
        "ADX_ESG_Template_v2_10",
        "DIFC_ESG_Template_v2_10",
        "MOCCAE_Compliance_Template_v2_10",
        "Schools_Lite_Template_v2_10",
        "SME_Lite_Template_v2_10"
    ]
    
    results = []
    
    for template in templates:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing template: {template}")
        logger.info(f"{'='*60}\n")
        
        try:
            # Generate PDF
            pdf_path = await test_generate_report_from_template(
                template_name=template,
                report_format="pdf",
                report_type="comprehensive"
            )
            results.append({
                "template": template,
                "format": "pdf",
                "status": "✅ Success",
                "path": pdf_path
            })
            
            # Generate DOCX
            docx_path = await test_generate_report_from_template(
                template_name=template,
                report_format="docx",
                report_type="comprehensive"
            )
            results.append({
                "template": template,
                "format": "docx",
                "status": "✅ Success",
                "path": docx_path
            })
            
        except Exception as e:
            results.append({
                "template": template,
                "format": "both",
                "status": f"❌ Failed: {str(e)[:50]}",
                "path": None
            })
    
    # Print summary
    logger.info(f"\n{'='*60}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*60}\n")
    
    for result in results:
        logger.info(f"{result['template']:40} | {result['format']:5} | {result['status']}")
    
    return results


async def test_single_template():
    """Test a single template with both PDF and DOCX formats"""
    template_name = "ADX_ESG_Template_v2_10"
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing single template: {template_name}")
    logger.info(f"{'='*60}\n")
    
    # Test PDF
    logger.info("\n--- Generating PDF Report ---")
    pdf_path = await test_generate_report_from_template(
        template_name=template_name,
        report_format="pdf",
        report_type="comprehensive"
    )
    
    # Test DOCX
    logger.info("\n--- Generating DOCX Report ---")
    docx_path = await test_generate_report_from_template(
        template_name=template_name,
        report_format="docx",
        report_type="comprehensive"
    )
    
    logger.info(f"\n{'='*60}")
    logger.info("RESULTS")
    logger.info(f"{'='*60}")
    logger.info(f"PDF Report:  {pdf_path}")
    logger.info(f"DOCX Report: {docx_path}")
    
    return pdf_path, docx_path


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test ESG Report Generation")
    parser.add_argument(
        "--template",
        type=str,
        help="Template name (e.g., ADX_ESG_Template_v2_10)",
        default="ADX_ESG_Template_v2_10"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["pdf", "docx", "both"],
        default="both",
        help="Report format"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["comprehensive", "executive", "technical"],
        default="comprehensive",
        help="Report type"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Test all templates"
    )
    
    args = parser.parse_args()
    
    if args.all:
        # Test all templates
        asyncio.run(test_all_templates())
    else:
        # Test specific template
        if args.format == "both":
            asyncio.run(test_single_template())
        else:
            asyncio.run(test_generate_report_from_template(
                template_name=args.template,
                report_format=args.format,
                report_type=args.type
            ))


if __name__ == "__main__":
    main()
