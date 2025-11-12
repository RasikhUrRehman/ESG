#!/usr/bin/env python3
"""
Example script demonstrating how to use the ESG API
"""
import requests
import json
from pathlib import Path


# API base URL
BASE_URL = "http://localhost:8000"


def list_templates():
    """List available templates"""
    response = requests.get(f"{BASE_URL}/templates")
    print("Available Templates:")
    print(json.dumps(response.json(), indent=2))
    return response.json()


def upload_file(file_path: str, template: str):
    """Upload a file for processing"""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'template': template}
        response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    
    print("\nUpload Response:")
    result = response.json()
    print(json.dumps(result, indent=2))
    return result


def extract_data(file_id: str):
    """Extract data from uploaded file"""
    response = requests.get(f"{BASE_URL}/extract/{file_id}")
    print("\nExtracted Data:")
    result = response.json()
    print(f"Total Records: {result['total_records']}")
    # Print first 3 records
    for i, record in enumerate(result['data'][:3]):
        print(f"\nRecord {i+1}:")
        print(json.dumps(record, indent=2))
    return result


def generate_report(file_id: str, report_format: str = "pdf", report_type: str = "comprehensive"):
    """Generate ESG report"""
    data = {
        "file_id": file_id,
        "report_format": report_format,
        "report_type": report_type,
        "include_charts": True
    }
    
    response = requests.post(f"{BASE_URL}/generate-report", json=data)
    print("\nReport Generation Response:")
    result = response.json()
    print(json.dumps(result, indent=2))
    return result


def download_report(report_url: str, output_path: str):
    """Download generated report"""
    response = requests.get(f"{BASE_URL}{report_url}")
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    print(f"\nReport downloaded to: {output_path}")


def main():
    """Main example workflow"""
    print("=" * 80)
    print("ESG Report Generation API - Example Usage")
    print("=" * 80)
    
    # Step 1: List available templates
    print("\n[STEP 1] Listing available templates...")
    templates = list_templates()
    
    # Step 2: Upload a file (replace with your actual file path)
    print("\n[STEP 2] Uploading file...")
    # Example: upload_result = upload_file("path/to/your/data.csv", "ADX_ESG")
    # For demonstration purposes, we'll skip actual upload
    # file_id = upload_result['file_id']
    
    # Step 3: Extract data
    # print("\n[STEP 3] Extracting data...")
    # extract_data(file_id)
    
    # Step 4: Generate report
    # print("\n[STEP 4] Generating report...")
    # report_result = generate_report(file_id, report_format="pdf", report_type="comprehensive")
    
    # Step 5: Download report
    # print("\n[STEP 5] Downloading report...")
    # download_report(report_result['download_url'], "esg_report.pdf")
    
    print("\n" + "=" * 80)
    print("Example completed!")
    print("Uncomment the code above to test with your actual files")
    print("=" * 80)


if __name__ == "__main__":
    main()
