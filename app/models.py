"""
Data models for the ESG application
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ReportFormat(str, Enum):
    """Supported report formats"""
    PDF = "pdf"
    DOCX = "docx"


class TemplateType(str, Enum):
    """Available ESG templates"""
    ADX_ESG = "ADX_ESG"
    DIFC_ESG = "DIFC_ESG"
    MOCCAE = "MOCCAE"
    SCHOOLS = "SCHOOLS"
    SME = "SME"


class ColumnMatchResult(BaseModel):
    """Result of column matching operation"""
    matched_columns: List[str] = Field(description="Columns that matched with template (position-independent)")
    unmatched_uploaded: List[str] = Field(description="Extra columns in uploaded file not in template")
    unmatched_template: List[str] = Field(description="Missing columns - required by template but not in uploaded file")
    match_percentage: float = Field(description="Percentage of template columns found in uploaded file")
    total_uploaded_columns: int = Field(description="Number of valid columns in uploaded file")
    total_template_columns: int = Field(description="Number of columns required by template")
    has_ambiguity: bool = Field(default=False, description="True if there are extra or missing columns")
    ambiguity_message: Optional[str] = Field(default=None, description="Detailed message about column mismatches")


class ExtractedData(BaseModel):
    """Extracted data from uploaded file"""
    section: str
    field: str
    prev_year: Optional[str] = None
    current: Optional[str] = None
    target: Optional[str] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    input_type: Optional[str] = None


class ReportRequest(BaseModel):
    """Request model for report generation"""
    file_id: str = Field(description="ID of the uploaded file")
    report_format: ReportFormat = Field(description="Format of the report (pdf or docx)")
    report_type: Optional[str] = Field(default="comprehensive", description="Type of report to generate")
    include_charts: bool = Field(default=True, description="Whether to include charts in the report")


class UploadResponse(BaseModel):
    """Response model for file upload"""
    file_id: str
    filename: str
    template_used: str
    match_result: ColumnMatchResult
    message: str
    uploaded_columns: List[str] = Field(description="List of all columns in the uploaded file")


class ExtractionResponse(BaseModel):
    """Response model for data extraction"""
    file_id: str
    data: List[Dict[str, Any]]
    total_records: int


class ReportResponse(BaseModel):
    """Response model for report generation"""
    report_id: str
    report_format: str
    download_url: str
    message: str
