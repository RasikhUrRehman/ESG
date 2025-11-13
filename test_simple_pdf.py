"""
Simple test script to generate a PDF report with tables using AI prompts only.
No template files required - just generates a report from scratch.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.report_generator import PDFReportGenerator
from app.config import settings


def test_simple_pdf_generation():
    """Generate a simple PDF with tables using AI prompts"""
    
    print("=" * 60)
    print("Simple PDF Generation Test (No Template)")
    print("=" * 60)
    
    # Sample ESG data to include in the report
    sample_data = """
    ## Environmental Metrics
    
    | Metric | Previous Year | Current Value | Unit | Target |
    |--------|---------------|---------------|------|--------|
    | Total Energy Consumption | 1250 | 1180 | MWh | 1000 |
    | Renewable Energy Percentage | 45 | 52 | % | 60 |
    | Water Usage | 5800 | 5200 | m³ | 4500 |
    | Waste Recycled | 68 | 75 | % | 80 |
    | CO2 Emissions | 890 | 820 | tCO2e | 700 |
    
    ## Social Metrics
    
    | Metric | Previous Year | Current Value | Unit | Target |
    |--------|---------------|---------------|------|--------|
    | Employee Satisfaction | 72 | 78 | % | 85 |
    | Training Hours per Employee | 28 | 35 | Hours | 40 |
    | Women in Leadership | 32 | 38 | % | 45 |
    | Workplace Accidents | 12 | 8 | Count | 5 |
    | Employee Turnover Rate | 18 | 14 | % | 10 |
    
    ## Governance Metrics
    
    | Metric | Previous Year | Current Value | Unit | Target |
    |--------|---------------|---------------|------|--------|
    | Independent Directors | 60 | 65 | % | 70 |
    | Board Diversity | 40 | 45 | % | 50 |
    | Ethics Training Completion | 88 | 95 | % | 100 |
    | Compliance Incidents | 3 | 1 | Count | 0 |
    | Audit Committee Meetings | 4 | 6 | Count | 6 |
    """
    
    # Create a simple prompt for the AI to generate a report
    prompt = f"""
    Generate a comprehensive ESG (Environmental, Social, Governance) Report based on the following data.
    
    Include:
    1. An executive summary highlighting key achievements
    2. Analysis of each metric category (Environmental, Social, Governance)
    3. Progress towards targets
    4. Recommendations for improvement
    
    Data:
    {sample_data}
    
    Format the report in markdown with clear sections and include all the tables as shown.
    """
    
    print("\nPrompt created. Generating report...")
    print(f"Using Grok API")
    
    # Initialize the PDF generator
    pdf_generator = PDFReportGenerator()
    
    # Generate the report using AI
    try:
        print("\nCalling AI to generate report content...")
        
        # Import the Grok API client
        import requests
        
        headers = {
            "Authorization": f"Bearer {settings.GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an ESG reporting expert. Generate detailed, professional ESG reports in markdown format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "grok-3",
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            ai_content = response.json()["choices"][0]["message"]["content"]
            print("\n✓ AI content generated successfully")
            print(f"Content length: {len(ai_content)} characters")
        else:
            print(f"\n✗ AI generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Fallback to the sample data if AI fails
            print("\nUsing fallback content...")
            ai_content = f"""
# ESG Report 2024

## Executive Summary

This report presents our Environmental, Social, and Governance (ESG) performance for the current year, 
showing significant progress across all three pillars of sustainability.

{sample_data}

## Environmental Performance

Our environmental metrics show strong improvement:
- Energy consumption reduced by 5.6% year-over-year
- Renewable energy usage increased to 52%, up from 45%
- Water usage decreased by 10.3%
- Waste recycling improved to 75%
- CO2 emissions reduced by 7.9%

## Social Performance

Social metrics demonstrate our commitment to employee wellbeing:
- Employee satisfaction increased to 78%
- Training hours per employee grew by 25%
- Women in leadership positions increased to 38%
- Workplace accidents reduced by 33%
- Employee turnover decreased to 14%

## Governance Performance

Governance improvements include:
- Independent directors now represent 65% of the board
- Board diversity improved to 45%
- Ethics training completion reached 95%
- Compliance incidents reduced to just 1
- Increased audit committee oversight with 6 meetings

## Recommendations

1. Continue renewable energy transition to meet 60% target
2. Enhance water conservation programs
3. Invest in advanced safety training
4. Accelerate diversity and inclusion initiatives
5. Maintain strong governance practices
"""
        
        # Create output directory
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)
        
        # Generate PDF
        output_file = output_dir / "test_simple_report.pdf"
        print(f"\nGenerating PDF: {output_file}")
        
        pdf_generator.generate(
            content=ai_content,
            output_path=output_file,
            title="ESG Report 2024 - Test"
        )
        
        print(f"\n{'='*60}")
        print(f"✓ PDF generated successfully!")
        print(f"{'='*60}")
        print(f"Location: {output_file.absolute()}")
        print(f"File size: {output_file.stat().st_size / 1024:.2f} KB")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_simple_pdf_generation()
    sys.exit(0 if success else 1)
