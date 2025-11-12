"""
Test script for column matching functionality
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.column_matcher import ColumnMatcher
from app.config import settings


def test_column_matching():
    """Test column matching with a template"""
    
    print("=" * 80)
    print("Testing Column Matcher")
    print("=" * 80)
    
    # List available templates
    print("\nAvailable Templates:")
    for template in settings.AVAILABLE_TEMPLATES:
        print(f"  - {template}")
    
    # Test with ADX template
    template_name = "ADX_ESG"
    print(f"\nTesting with template: {template_name}")
    
    matcher = ColumnMatcher(template_name)
    
    # Get template columns
    template_cols = matcher.get_template_columns()
    print(f"\nTemplate has {len(template_cols)} columns:")
    for i, col in enumerate(template_cols[:5], 1):
        print(f"  {i}. {col}")
    print(f"  ... and {len(template_cols) - 5} more")
    
    print("\n" + "=" * 80)
    print("Column Matcher Test Complete")
    print("=" * 80)


if __name__ == "__main__":
    test_column_matching()
