"""
Test script for improved column matching with ambiguity detection
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.column_matcher import ColumnMatcher, TEMPLATE_COLUMNS
import pandas as pd


def test_perfect_match():
    """Test with perfect column match"""
    print("\n" + "=" * 80)
    print("TEST 1: Perfect Column Match")
    print("=" * 80)
    
    matcher = ColumnMatcher("ADX_ESG")
    
    # Create a DataFrame with exact template columns
    df = pd.DataFrame(columns=TEMPLATE_COLUMNS["ADX_ESG"])
    
    result = matcher.match_columns(df)
    
    print(f"Match Percentage: {result.match_percentage}%")
    print(f"Matched: {len(result.matched_columns)}/{result.total_template_columns}")
    print(f"Has Ambiguity: {result.has_ambiguity}")
    print(f"Ambiguity Message: {result.ambiguity_message}")
    print(f"Extra Columns: {result.unmatched_uploaded}")
    print(f"Missing Columns: {result.unmatched_template}")


def test_extra_column():
    """Test with extra columns"""
    print("\n" + "=" * 80)
    print("TEST 2: Extra Column in Upload")
    print("=" * 80)
    
    matcher = ColumnMatcher("ADX_ESG")
    
    # Create a DataFrame with template columns + extra column
    columns = TEMPLATE_COLUMNS["ADX_ESG"] + ["Extra Column 1", ""]
    df = pd.DataFrame(columns=columns)
    
    result = matcher.match_columns(df)
    
    print(f"Match Percentage: {result.match_percentage}%")
    print(f"Matched: {len(result.matched_columns)}/{result.total_template_columns}")
    print(f"Has Ambiguity: {result.has_ambiguity}")
    print(f"Ambiguity Message: {result.ambiguity_message}")
    print(f"Extra Columns: {result.unmatched_uploaded}")
    print(f"Missing Columns: {result.unmatched_template}")


def test_missing_column():
    """Test with missing required columns"""
    print("\n" + "=" * 80)
    print("TEST 3: Missing Required Columns")
    print("=" * 80)
    
    matcher = ColumnMatcher("ADX_ESG")
    
    # Create a DataFrame with only some template columns
    columns = TEMPLATE_COLUMNS["ADX_ESG"][:5]  # Only first 5 columns
    df = pd.DataFrame(columns=columns)
    
    result = matcher.match_columns(df)
    
    print(f"Match Percentage: {result.match_percentage}%")
    print(f"Matched: {len(result.matched_columns)}/{result.total_template_columns}")
    print(f"Has Ambiguity: {result.has_ambiguity}")
    print(f"Ambiguity Message: {result.ambiguity_message}")
    print(f"Extra Columns: {result.unmatched_uploaded}")
    print(f"Missing Columns: {result.unmatched_template}")


def test_mixed_scenario():
    """Test with both extra and missing columns"""
    print("\n" + "=" * 80)
    print("TEST 4: Mixed Scenario (Extra + Missing)")
    print("=" * 80)
    
    matcher = ColumnMatcher("ADX_ESG")
    
    # Create a DataFrame with some template columns + extra columns
    columns = TEMPLATE_COLUMNS["ADX_ESG"][:8] + ["Unknown Column", "", "Unnamed: 0"]
    df = pd.DataFrame(columns=columns)
    
    result = matcher.match_columns(df)
    
    print(f"Match Percentage: {result.match_percentage}%")
    print(f"Matched: {len(result.matched_columns)}/{result.total_template_columns}")
    print(f"Has Ambiguity: {result.has_ambiguity}")
    print(f"\nAmbiguity Message:")
    if result.ambiguity_message:
        for msg in result.ambiguity_message.split(' | '):
            print(f"  {msg}")
    print(f"\nExtra Columns: {result.unmatched_uploaded}")
    print(f"Missing Columns: {result.unmatched_template}")


def test_all_templates():
    """Test all template definitions"""
    print("\n" + "=" * 80)
    print("TEST 5: All Template Definitions")
    print("=" * 80)
    
    for template_name, columns in TEMPLATE_COLUMNS.items():
        print(f"\n{template_name}:")
        print(f"  Total Columns: {len(columns)}")
        print(f"  Columns: {', '.join(columns[:3])}... (+{len(columns)-3} more)")


if __name__ == "__main__":
    print("=" * 80)
    print("Column Matching Tests - Enhanced with Ambiguity Detection")
    print("=" * 80)
    
    test_perfect_match()
    test_extra_column()
    test_missing_column()
    test_mixed_scenario()
    test_all_templates()
    
    print("\n" + "=" * 80)
    print("All Tests Complete!")
    print("=" * 80)
