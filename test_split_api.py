"""
Test script for the new split API endpoints: /compare-columns and /map-columns

This script demonstrates:
1. Uploading a file to compare columns
2. Reviewing the columns returned
3. Creating column mappings
4. Submitting the mappings to process the data

Usage:
    python test_split_api.py <file_path> <template_name>

Example:
    python test_split_api.py uploads/test.csv ADX_ESG
    python test_split_api.py uploads/report.docx MOCCAE
"""

import requests
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional


BASE_URL = "http://localhost:8000"


def compare_columns(file_path: str, template: str) -> Dict:
    """
    Step 1: Upload file and compare columns
    
    Args:
        file_path: Path to the file to upload
        template: Template name (e.g., 'ADX_ESG', 'MOCCAE')
        
    Returns:
        Response data with file_id, template_columns, and uploaded_columns
    """
    print(f"\n{'='*80}")
    print(f"STEP 1: Comparing columns")
    print(f"{'='*80}")
    print(f"File: {file_path}")
    print(f"Template: {template}")
    
    url = f"{BASE_URL}/compare-columns"
    
    # Open and upload file
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'template': template}
        
        response = requests.post(url, files=files, data=data)
    
    if response.status_code != 200:
        print(f"\n❌ Error: {response.status_code}")
        print(response.json())
        sys.exit(1)
    
    result = response.json()
    
    print(f"\n✅ Success!")
    print(f"File ID: {result['file_id']}")
    print(f"Filename: {result['filename']}")
    print(f"\nTemplate Columns ({len(result['template_columns'])}):")
    for i, col in enumerate(result['template_columns'], 1):
        print(f"  {i}. {col}")
    
    print(f"\nUploaded File Columns ({len(result['uploaded_columns'])}):")
    for i, col in enumerate(result['uploaded_columns'], 1):
        print(f"  {i}. {col}")
    
    print(f"\nMessage: {result['message']}")
    
    return result


def create_automatic_mappings(template_columns: List[str], uploaded_columns: List[str]) -> List[Dict]:
    """
    Create automatic column mappings (simple exact match + similarity)
    
    In a real application, this would be done through a UI where users
    confirm or adjust the mappings.
    
    Args:
        template_columns: List of template column names
        uploaded_columns: List of uploaded file column names
        
    Returns:
        List of column mappings
    """
    print(f"\n{'='*80}")
    print(f"Creating automatic mappings (in production, user would review these)")
    print(f"{'='*80}")
    
    mappings = []
    
    for template_col in template_columns:
        # Try exact match first
        matched_col = None
        
        if template_col in uploaded_columns:
            matched_col = template_col
        else:
            # Try case-insensitive match
            for uploaded_col in uploaded_columns:
                if template_col.lower() == uploaded_col.lower():
                    matched_col = uploaded_col
                    break
        
        # Try partial match (if no exact match found)
        if not matched_col:
            template_lower = template_col.lower()
            for uploaded_col in uploaded_columns:
                uploaded_lower = uploaded_col.lower()
                # Check if significant words match
                template_words = set(template_lower.split())
                uploaded_words = set(uploaded_lower.split())
                common_words = template_words & uploaded_words
                
                if len(common_words) > 0 and len(common_words) >= min(2, len(template_words)):
                    matched_col = uploaded_col
                    break
        
        mapping = {
            "template_column": template_col,
            "uploaded_column": matched_col  # Will be None if no match found
        }
        
        mappings.append(mapping)
        
        if matched_col:
            print(f"✓ {template_col} → {matched_col}")
        else:
            print(f"✗ {template_col} → (no match)")
    
    return mappings


def map_columns(file_id: str, mappings: List[Dict]) -> Dict:
    """
    Step 2: Submit column mappings and process data
    
    Args:
        file_id: File ID from compare_columns response
        mappings: List of column mappings
        
    Returns:
        Response data with extracted and mapped data
    """
    print(f"\n{'='*80}")
    print(f"STEP 2: Mapping columns and processing data")
    print(f"{'='*80}")
    
    url = f"{BASE_URL}/map-columns"
    
    payload = {
        "file_id": file_id,
        "mappings": mappings
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print(f"\n❌ Error: {response.status_code}")
        print(response.json())
        sys.exit(1)
    
    result = response.json()
    
    print(f"\n✅ Success!")
    print(f"File ID: {result['file_id']}")
    print(f"Filename: {result['filename']}")
    print(f"Template: {result['template_used']}")
    print(f"\nMatch Result:")
    print(f"  Match Percentage: {result['match_result']['match_percentage']}%")
    print(f"  Matched Columns: {len(result['match_result']['matched_columns'])}")
    print(f"  Unmatched Template Columns: {len(result['match_result']['unmatched_template'])}")
    print(f"  Extra Uploaded Columns: {len(result['match_result']['unmatched_uploaded'])}")
    
    if result['match_result']['unmatched_template']:
        print(f"\n  Missing columns: {', '.join(result['match_result']['unmatched_template'])}")
    
    if result['match_result']['unmatched_uploaded']:
        print(f"\n  Extra columns: {', '.join(result['match_result']['unmatched_uploaded'])}")
    
    print(f"\nMessage: {result['message']}")
    print(f"\nExtracted Data: {len(result['data'])} records")
    
    # Show first few records with change analysis
    if result['data']:
        print(f"\nFirst 3 records with change analysis (sample):")
        for i, record in enumerate(result['data'][:3], 1):
            print(f"\n  Record {i}:")
            # Show all fields
            for key, value in record.items():
                if key == 'change_percentage' and value is not None:
                    print(f"    {key}: {value}%")
                elif key == 'status' and value is not None:
                    status_icon = "✅" if value == "improved" else "⚠️" if value == "slight" else "❌"
                    print(f"    {key}: {status_icon} {value}")
                else:
                    # Truncate long values
                    display_value = str(value)[:50] + "..." if len(str(value)) > 50 else value
                    print(f"    {key}: {display_value}")
        
        # Show change analysis summary
        print(f"\n{'='*80}")
        print("Change Analysis Summary:")
        print(f"{'='*80}")
        
        improved_count = sum(1 for r in result['data'] if r.get('status') == 'improved')
        worsened_count = sum(1 for r in result['data'] if r.get('status') == 'worsened')
        slight_count = sum(1 for r in result['data'] if r.get('status') == 'slight')
        no_data_count = sum(1 for r in result['data'] if r.get('status') is None)
        
        print(f"  ✅ Improved: {improved_count}")
        print(f"  ❌ Worsened: {worsened_count}")
        print(f"  ⚠️  Slight change: {slight_count}")
        print(f"  ⊝  No comparison data: {no_data_count}")
    
    return result


def main():
    """Main test function"""
    if len(sys.argv) < 3:
        print("Usage: python test_split_api.py <file_path> <template_name>")
        print("\nAvailable templates:")
        print("  - ADX_ESG")
        print("  - DIFC_ESG")
        print("  - MOCCAE")
        print("  - SCHOOLS")
        print("  - SME")
        print("\nExample:")
        print("  python test_split_api.py uploads/test.csv ADX_ESG")
        print("  python test_split_api.py uploads/report.docx MOCCAE")
        sys.exit(1)
    
    file_path = sys.argv[1]
    template = sys.argv[2]
    
    # Validate file exists
    if not Path(file_path).exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    
    print(f"\n{'='*80}")
    print(f"Testing Split API Flow")
    print(f"{'='*80}")
    
    try:
        # Step 1: Compare columns
        compare_result = compare_columns(file_path, template)
        
        # Create mappings (in production, user would do this via UI)
        mappings = create_automatic_mappings(
            compare_result['template_columns'],
            compare_result['uploaded_columns']
        )
        
        # Step 2: Map columns
        map_result = map_columns(compare_result['file_id'], mappings)
        
        print(f"\n{'='*80}")
        print(f"✅ Test completed successfully!")
        print(f"{'='*80}")
        print(f"\nYou can now:")
        print(f"1. Use file_id '{map_result['file_id']}' to extract data via /extract/{map_result['file_id']}")
        print(f"2. Generate a report using /generate-report")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
