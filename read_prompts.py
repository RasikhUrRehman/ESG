"""
Script to read prompts from Generation Prompt.docx and update app/prompts.py
This allows you to customize AI prompts by editing the Word document
"""
from docx import Document
from pathlib import Path


def read_prompts_from_docx(docx_path: str = "Generation Prompt.docx"):
    """
    Read prompts from the Word document
    
    Args:
        docx_path: Path to the Word document
        
    Returns:
        Dictionary of prompts
    """
    try:
        doc = Document(docx_path)
        
        print("=" * 80)
        print("Reading prompts from:", docx_path)
        print("=" * 80)
        
        # Extract all paragraphs
        prompts_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                prompts_text.append(para.text)
        
        print(f"\nFound {len(prompts_text)} paragraphs")
        print("\nFirst few paragraphs:")
        for i, text in enumerate(prompts_text[:5], 1):
            print(f"\n{i}. {text[:100]}...")
        
        return prompts_text
        
    except Exception as e:
        print(f"Error reading document: {e}")
        return None


def display_current_prompts():
    """Display current prompts from app/prompts.py"""
    from app.prompts import REPORT_PROMPTS
    
    print("\n" + "=" * 80)
    print("Current Report Types Available:")
    print("=" * 80)
    
    for report_type in REPORT_PROMPTS.keys():
        print(f"  - {report_type}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("ESG Report Prompt Manager")
    print("=" * 80)
    
    # Check if Generation Prompt.docx exists
    docx_path = Path("Generation Prompt.docx")
    
    if docx_path.exists():
        print(f"\n✅ Found: {docx_path}")
        prompts = read_prompts_from_docx(str(docx_path))
        
        if prompts:
            print("\n" + "=" * 80)
            print("To integrate these prompts:")
            print("1. Review the content above")
            print("2. Edit app/prompts.py")
            print("3. Add custom prompts to REPORT_PROMPTS dictionary")
            print("=" * 80)
    else:
        print(f"\n❌ File not found: {docx_path}")
        print("Please ensure 'Generation Prompt.docx' is in the project root")
    
    # Display current prompts
    try:
        display_current_prompts()
    except Exception as e:
        print(f"\nNote: Run this after installing dependencies: {e}")
    
    print("\n" + "=" * 80)
    print("Prompt management complete!")
    print("=" * 80)
