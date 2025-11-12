"""
FastAPI Main Application for ESG Report Generation
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional, List
import logging
import json
import uuid

from .config import settings
from .models import (
    ReportFormat, TemplateType, ColumnMatchResult,
    UploadResponse, ExtractionResponse, ReportResponse, ReportRequest
)
from .column_matcher import ColumnMatcher, get_data_summary, format_data_for_report
from .report_generator import ReportGenerator
from .utils import (
    generate_unique_id, is_allowed_file, save_uploaded_file,
    cleanup_old_files
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ESG Report Generation API with column matching and AI-powered report creation"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store file metadata in memory (use database in production)
file_storage = {}
extraction_storage = {}


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Create necessary directories
    settings.UPLOADS_DIR.mkdir(exist_ok=True)
    settings.REPORTS_DIR.mkdir(exist_ok=True)
    
    # Clean up old files
    cleanup_old_files(settings.UPLOADS_DIR)
    cleanup_old_files(settings.REPORTS_DIR)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/templates")
async def list_templates():
    """List available ESG templates"""
    templates = []
    for template_name in settings.AVAILABLE_TEMPLATES:
        templates.append({
            "name": template_name,
            "display_name": template_name.replace("_", " "),
            "columns": len(ColumnMatcher(template_name).get_template_columns())
        })
    
    return {
        "templates": templates,
        "total": len(templates)
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    template: str = Form(...)
):
    """
    Upload a file and match columns with selected template
    
    Args:
        file: Uploaded CSV/Excel file
        template: Template name to match against
        
    Returns:
        UploadResponse with matching results
    """
    try:
        # Validate file extension
        if not is_allowed_file(file.filename, settings.ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Validate template
        if template not in settings.AVAILABLE_TEMPLATES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid template. Available templates: {settings.AVAILABLE_TEMPLATES}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Check file size
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / (1024*1024)} MB"
            )
        
        # Save uploaded file
        file_path = save_uploaded_file(file_content, file.filename, settings.UPLOADS_DIR)
        
        # Generate unique file ID
        file_id = generate_unique_id()
        
        # Initialize column matcher
        matcher = ColumnMatcher(template)
        
        # Process file: match columns and extract data
        match_result, extracted_data = matcher.process_file(file_path)
        
        # Store file metadata and extracted data
        file_storage[file_id] = {
            "file_id": file_id,
            "filename": file.filename,
            "template": template,
            "file_path": str(file_path),
            "match_result": match_result.dict()
        }
        
        extraction_storage[file_id] = extracted_data
        
        logger.info(f"File uploaded and processed: {file_id}")
        
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            template_used=template,
            match_result=match_result,
            message="File uploaded and columns matched successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/{file_id}")
async def get_file_info(file_id: str):
    """Get information about an uploaded file"""
    if file_id not in file_storage:
        raise HTTPException(status_code=404, detail="File not found")
    
    return file_storage[file_id]


@app.get("/extract/{file_id}", response_model=ExtractionResponse)
async def extract_data(file_id: str):
    """
    Extract required columns from uploaded file
    
    Args:
        file_id: ID of the uploaded file
        
    Returns:
        ExtractionResponse with extracted data
    """
    if file_id not in extraction_storage:
        raise HTTPException(status_code=404, detail="File not found or not processed")
    
    extracted_data = extraction_storage[file_id]
    
    return ExtractionResponse(
        file_id=file_id,
        data=extracted_data,
        total_records=len(extracted_data)
    )


@app.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    """
    Generate ESG report based on uploaded data
    
    Args:
        request: Report generation request
        background_tasks: FastAPI background tasks
        
    Returns:
        ReportResponse with download information
    """
    try:
        # Validate file exists
        if request.file_id not in extraction_storage:
            raise HTTPException(status_code=404, detail="File not found or not processed")
        
        # Get extracted data
        extracted_data = extraction_storage[request.file_id]
        
        if not extracted_data:
            raise HTTPException(status_code=400, detail="No data available for report generation")
        
        # Generate unique report ID
        report_id = generate_unique_id()
        
        # Create output filename
        output_filename = f"esg_report_{report_id}"
        
        # Initialize report generator
        report_gen = ReportGenerator()
        
        # Generate report
        logger.info(f"Generating {request.report_format} report...")
        report_path = await report_gen.generate_report(
            data=extracted_data,
            report_type=request.report_type,
            output_format=request.report_format.value,
            output_filename=output_filename,
            include_charts=request.include_charts
        )
        
        # Create download URL
        download_url = f"/download-report/{report_id}.{request.report_format.value}"
        
        logger.info(f"Report generated successfully: {report_id}")
        
        return ReportResponse(
            report_id=report_id,
            report_format=request.report_format.value,
            download_url=download_url,
            message="Report generated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download-report/{filename}")
async def download_report(filename: str):
    """
    Download generated report
    
    Args:
        filename: Report filename
        
    Returns:
        File response with the report
    """
    report_path = settings.REPORTS_DIR / filename
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Determine media type
    media_type = "application/pdf" if filename.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    return FileResponse(
        path=report_path,
        media_type=media_type,
        filename=filename
    )


@app.get("/report-types")
async def list_report_types():
    """List available report types"""
    return {
        "report_types": [
            {"value": "comprehensive", "label": "Comprehensive ESG Report"},
            {"value": "environmental", "label": "Environmental Performance Report"},
            {"value": "social", "label": "Social Impact Report"},
            {"value": "governance", "label": "Governance Report"},
            {"value": "compliance", "label": "Compliance and Regulatory Report"},
            {"value": "executive", "label": "Executive Summary"}
        ]
    }


@app.get("/formats")
async def list_formats():
    """List available report formats"""
    return {
        "formats": [
            {"value": "pdf", "label": "PDF Document"},
            {"value": "docx", "label": "Word Document (.docx)"}
        ]
    }


@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete uploaded file and associated data"""
    if file_id not in file_storage:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get file path
    file_info = file_storage[file_id]
    file_path = Path(file_info["file_path"])
    
    # Delete file from disk
    if file_path.exists():
        file_path.unlink()
    
    # Remove from storage
    del file_storage[file_id]
    if file_id in extraction_storage:
        del extraction_storage[file_id]
    
    logger.info(f"File deleted: {file_id}")
    
    return {"message": "File deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
