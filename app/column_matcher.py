"""
Column matching and data extraction utilities using pandas
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging

from .models import ColumnMatchResult, ExtractedData
from .config import settings
from .utils import load_sme_csv_to_dataframe

logger = logging.getLogger(__name__)


# Static column definitions for each template
TEMPLATE_COLUMNS = {
    "ADX_ESG": [
        "Section / القسم",
        "Field (EN)",
        "الحقل (AR)",
        "Prev Year",
        "Current",
        "Target",
        "Unit",
        "Notes",
        "Applicability",
        "Input Type",
        "Options"
    ],
    "DIFC_ESG": [
        "Section / القسم",
        "Field (EN)",
        "الحقل (AR)",
        "Prev Year",
        "Current",
        "Target",
        "Unit",
        "Notes",
        "Applicability",
        "Input Type",
        "Options",
        "Evidence Required?",
        "Confidential?"
    ],
    "MOCCAE": [
        "Section (EN)",
        "Section (AR)",
        "Field (EN)",
        "الحقل (AR)",
        "Response / الإدخال",
        "Unit / الوحدة",
        "Prev Year / العام السابق",
        "Current / العام الحالي",
        "Target / الهدف",
        "Notes / ملاحظات",
        "Applicability",
        "Evidence Required?",
        "Confidential?"
    ],
    "SCHOOLS": [
        "Section / القسم",
        "Field (EN)",
        "الحقل (AR)",
        "Prev Year",
        "Current",
        "Target",
        "Unit",
        "Notes",
        "Applicability",
        "Input Type",
        "Options",
        "Evidence Required?",
        "Confidential?"
    ],
    "SME": [
        "Section / القسم",
        "Field (EN)",
        "الحقل (AR)",
        "Prev Year",
        "Current",
        "Target",
        "Unit",
        "Notes",
        "Applicability",
        "Input Type",
        "Options",
        "Evidence Required?",
        "Confidential?"
    ]
}


class ColumnMatcher:
    """Handles column matching between uploaded files and templates"""
    
    def __init__(self, template_name: str):
        """
        Initialize the column matcher with a template
        
        Args:
            template_name: Name of the template (e.g., 'ADX_ESG', 'DIFC_ESG', 'MOCCAE', 'SCHOOLS', 'SME')
        """
        self.template_name = template_name
        self.template_columns = TEMPLATE_COLUMNS.get(template_name)
        
        if self.template_columns is None:
            raise ValueError(f"Unknown template: {template_name}. Available templates: {list(TEMPLATE_COLUMNS.keys())}")
        
        logger.info(f"Initialized column matcher for template: {self.template_name}")
    
    def get_template_columns(self) -> List[str]:
        """Get the list of column names from the template"""
        return self.template_columns
    
    def load_uploaded_file(self, file_path: Path) -> pd.DataFrame:
        """
        Load uploaded file (CSV or Excel) into a DataFrame
        
        Args:
            file_path: Path to the uploaded file
            
        Returns:
            DataFrame containing the uploaded data
        """
        file_extension = file_path.suffix.lower()
        
        try:
            if file_extension == '.csv':
                # Use robust CSV loader for uploaded CSV files
                df = load_sme_csv_to_dataframe(
                    str(file_path),
                    preserve_brackets=True,
                    merge_excess_into_notes=True,
                    encoding='utf-8',
                    verbose=False
                )
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            logger.info(f"Loaded uploaded file: {file_path.name}")
            return df
        except Exception as e:
            logger.error(f"Error loading uploaded file {file_path}: {e}")
            raise
    
    def match_columns(self, uploaded_df: pd.DataFrame) -> ColumnMatchResult:
        """
        Match columns between uploaded file and template
        Position of columns does not matter - only presence is checked.
        
        Args:
            uploaded_df: DataFrame from uploaded file
            
        Returns:
            ColumnMatchResult containing matching details
        """
        template_columns = set(self.get_template_columns())
        
        # Get uploaded columns and filter out empty/null column names
        uploaded_columns_raw = uploaded_df.columns.tolist()
        uploaded_columns = set([
            col for col in uploaded_columns_raw 
            if col and str(col).strip() and str(col).strip().lower() not in ['', 'nan', 'none', 'unnamed']
        ])
        
        # Find matches (position-independent matching)
        matched = list(template_columns.intersection(uploaded_columns))
        unmatched_uploaded = list(uploaded_columns - template_columns)
        unmatched_template = list(template_columns - uploaded_columns)
        
        # Calculate match percentage based on template columns
        if len(template_columns) > 0:
            match_percentage = (len(matched) / len(template_columns)) * 100
        else:
            match_percentage = 0.0
        
        # Log any ambiguities or issues
        if unmatched_uploaded:
            logger.warning(f"Extra columns in uploaded file not in template: {unmatched_uploaded}")
        if unmatched_template:
            logger.warning(f"Missing columns from template: {unmatched_template}")
        
        # Count invalid columns that were filtered out
        invalid_columns = [
            col for col in uploaded_columns_raw 
            if not col or not str(col).strip() or str(col).strip().lower() in ['', 'nan', 'none'] or str(col).startswith('Unnamed:')
        ]
        if invalid_columns:
            logger.warning(f"Filtered out {len(invalid_columns)} invalid/empty column names from uploaded file")
        
        # Build ambiguity message
        has_ambiguity = bool(unmatched_uploaded or unmatched_template)
        ambiguity_message = None
        
        if has_ambiguity:
            messages = []
            if unmatched_template:
                messages.append(f"⚠️ MISSING COLUMNS ({len(unmatched_template)}): These required columns are missing from your file: {', '.join(sorted(unmatched_template))}")
            if unmatched_uploaded:
                messages.append(f"ℹ️ EXTRA COLUMNS ({len(unmatched_uploaded)}): These columns in your file are not in the template: {', '.join(sorted(unmatched_uploaded))}")
            if invalid_columns:
                messages.append(f"⚠️ INVALID COLUMNS ({len(invalid_columns)}): Filtered out empty or unnamed columns")
            ambiguity_message = " | ".join(messages)
        
        result = ColumnMatchResult(
            matched_columns=sorted(matched),  # Sort for consistent output
            unmatched_uploaded=sorted(unmatched_uploaded),
            unmatched_template=sorted(unmatched_template),
            match_percentage=round(match_percentage, 2),
            total_uploaded_columns=len(uploaded_columns),  # Only valid columns
            total_template_columns=len(template_columns),
            has_ambiguity=has_ambiguity,
            ambiguity_message=ambiguity_message
        )
        
        logger.info(f"Column matching complete. Match percentage: {result.match_percentage}%")
        logger.info(f"Matched {len(matched)}/{len(template_columns)} template columns")
        if has_ambiguity:
            logger.warning(f"Ambiguity detected: {ambiguity_message}")
        
        return result
    
    def extract_required_data(
        self, 
        uploaded_df: pd.DataFrame,
        match_result: ColumnMatchResult
    ) -> List[Dict[str, Any]]:
        """
        Extract all columns from uploaded data
        
        Args:
            uploaded_df: DataFrame from uploaded file
            match_result: Result from column matching
            
        Returns:
            List of dictionaries containing all extracted data
        """
        # Extract all data from the DataFrame
        extracted_data = []
        
        # Get all column names from the uploaded file
        all_columns = uploaded_df.columns.tolist()
        
        for idx, row in uploaded_df.iterrows():
            record = {}
            # Include all columns from the uploaded file
            for col in all_columns:
                # Skip invalid/unnamed columns
                if col and str(col).strip() and not str(col).startswith('Unnamed:'):
                    # Convert to string and handle NaN values
                    value = row.get(col, '')
                    record[col] = str(value) if pd.notna(value) else ''
            
            extracted_data.append(record)
        
        logger.info(f"Extracted {len(extracted_data)} records with {len(all_columns)} columns from uploaded file")
        return extracted_data
    
    def process_file(self, file_path: Path) -> Tuple[ColumnMatchResult, List[Dict[str, Any]]]:
        """
        Process uploaded file: load, match columns, and extract data
        
        Args:
            file_path: Path to uploaded file
            
        Returns:
            Tuple of (ColumnMatchResult, extracted_data)
        """
        # Load uploaded file
        uploaded_df = self.load_uploaded_file(file_path)
        
        # Match columns
        match_result = self.match_columns(uploaded_df)
        
        # Extract data
        extracted_data = self.extract_required_data(uploaded_df, match_result)
        
        return match_result, extracted_data


def get_data_summary(extracted_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a summary of extracted data for reporting
    
    Args:
        extracted_data: List of extracted data records
        
    Returns:
        Dictionary containing data summary
    """
    if not extracted_data:
        return {}
    
    # Define possible column name mappings
    SECTION_COLUMNS = ["Section / القسم", "Section (EN)", "Section (AR)", "section"]
    CURRENT_COLUMNS = ["Current", "Current / العام الحالي", "Response / الإدخال", "current"]
    TARGET_COLUMNS = ["Target", "Target / الهدف", "target"]
    
    # Extract sections
    sections = []
    section_counts = {}
    filled_current = 0
    filled_target = 0
    
    for row in extracted_data:
        # Find section
        section = _find_column(row, SECTION_COLUMNS)
        if section:
            sections.append(section)
            section_counts[section] = section_counts.get(section, 0) + 1
        
        # Check filled fields
        if _find_column(row, CURRENT_COLUMNS):
            filled_current += 1
        if _find_column(row, TARGET_COLUMNS):
            filled_target += 1
    
    # Get unique sections
    unique_sections = list(set(sections))
    total_fields = len(extracted_data)
    
    summary = {
        'total_records': total_fields,
        'sections': unique_sections,
        'section_counts': section_counts,
        'total_fields': total_fields,
        'filled_current': filled_current,
        'filled_target': filled_target,
        'completion_rate_current': round((filled_current / total_fields) * 100, 2) if total_fields > 0 else 0,
        'completion_rate_target': round((filled_target / total_fields) * 100, 2) if total_fields > 0 else 0
    }
    
    return summary


def _find_column(row: Dict[str, Any], possible_names: List[str]) -> Any:
    """
    Find a column value by checking multiple possible column names
    
    Args:
        row: Data row dictionary
        possible_names: List of possible column names to check
        
    Returns:
        Value if found, None otherwise
    """
    for name in possible_names:
        if name in row:
            value = row[name]
            if pd.notna(value) and str(value).strip() and str(value) != 'nan':
                return value
    return None


def format_data_for_report(extracted_data: List[Dict[str, Any]]) -> str:
    """
    Format extracted data into a readable string for AI report generation
    
    Args:
        extracted_data: List of extracted data records
        
    Returns:
        Formatted string representation of the data
    """
    if not extracted_data:
        return "No data available."
    
    formatted_lines = []
    formatted_lines.append("ESG DATA SUMMARY")
    formatted_lines.append("=" * 80)
    formatted_lines.append("")
    
    # Define possible column name mappings for different templates
    SECTION_COLUMNS = ["Section / القسم", "Section (EN)", "Section (AR)", "section"]
    FIELD_COLUMNS = ["Field (EN)", "الحقل (AR)", "field"]
    PREV_YEAR_COLUMNS = ["Prev Year", "Prev Year / العام السابق", "prev_year"]
    CURRENT_COLUMNS = ["Current", "Current / العام الحالي", "Response / الإدخال", "current"]
    TARGET_COLUMNS = ["Target", "Target / الهدف", "target"]
    UNIT_COLUMNS = ["Unit", "Unit / الوحدة", "unit"]
    NOTES_COLUMNS = ["Notes", "Notes / ملاحظات", "notes"]
    
    # Group data by section
    current_section = None
    
    for row in extracted_data:
        # Find section value
        section = _find_column(row, SECTION_COLUMNS)
        
        if section and section != current_section:
            current_section = section
            formatted_lines.append(f"\n## {section}")
            formatted_lines.append("-" * 80)
        
        # Find field value
        field = _find_column(row, FIELD_COLUMNS)
        
        if field:
            formatted_lines.append(f"\n### {field}")
            
            # Find other values
            prev_year = _find_column(row, PREV_YEAR_COLUMNS)
            if prev_year:
                formatted_lines.append(f"  Previous Year: {prev_year}")
            
            current = _find_column(row, CURRENT_COLUMNS)
            if current:
                formatted_lines.append(f"  Current: {current}")
            
            target = _find_column(row, TARGET_COLUMNS)
            if target:
                formatted_lines.append(f"  Target: {target}")
            
            unit = _find_column(row, UNIT_COLUMNS)
            if unit:
                formatted_lines.append(f"  Unit: {unit}")
            
            notes = _find_column(row, NOTES_COLUMNS)
            if notes:
                formatted_lines.append(f"  Notes: {notes}")
    
    return "\n".join(formatted_lines)
