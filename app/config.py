"""
Configuration settings for the ESG application
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    APP_NAME: str = "ESG Report Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Grok API Configuration
    GROK_API_KEY: str
    GROK_API_BASE: str = "https://api.x.ai/v1"
    GROK_MODEL: str = "grok-3"  # Options: grok-3, grok-4, grok-3-mini
    
    # File Configuration
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    UPLOADS_DIR: Path = BASE_DIR / "uploads"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    
    # Upload Configuration
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls", ".docx"]
    
    # Template Files
    AVAILABLE_TEMPLATES: List[str] = [
        "ADX_ESG",
        "DIFC_ESG",
        "MOCCAE",
        "SCHOOLS",
        "SME"
    ]
    
    # Report Configuration
    REPORT_FORMATS: List[str] = ["pdf", "docx"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()

# Create necessary directories
settings.UPLOADS_DIR.mkdir(exist_ok=True)
settings.REPORTS_DIR.mkdir(exist_ok=True)
