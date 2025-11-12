# ESG Report Generation System - Complete Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Features](#features)
4. [Technology Stack](#technology-stack)
5. [File Structure](#file-structure)
6. [API Documentation](#api-documentation)
7. [Workflow](#workflow)
8. [Installation & Setup](#installation--setup)
9. [Usage Examples](#usage-examples)
10. [Customization Guide](#customization-guide)

---

## 🎯 Project Overview

The ESG Report Generation System is a comprehensive FastAPI-based application that automates the process of:
- **Column Matching**: Automatically matches uploaded CSV/Excel files with predefined ESG templates
- **Data Extraction**: Extracts relevant ESG metrics from uploaded files
- **AI-Powered Report Generation**: Uses Grok AI to generate professional ESG reports
- **Multi-Format Export**: Generates reports in PDF or Word (DOCX) format
- **Visualization**: Includes charts and graphs in generated reports

### Key Benefits
✅ Automated template matching with detailed mismatch reporting  
✅ Support for multiple ESG frameworks (ADX, DIFC, MOCCAE, Schools, SME)  
✅ AI-powered content generation using Grok API  
✅ Professional PDF and Word report generation  
✅ RESTful API with interactive documentation  
✅ Docker-ready for easy deployment  
✅ Modular and extensible architecture  

---

## 🏗️ System Architecture

```
┌─────────────┐
│   Frontend  │ (HTML/JavaScript)
│   (Browser) │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Application                     │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │  main.py     │  │ models.py    │  │ config.py  ││
│  │  (Endpoints) │  │ (Data Models)│  │ (Settings) ││
│  └──────────────┘  └──────────────┘  └────────────┘│
│  ┌──────────────────────────────────────────────────┐│
│  │         Column Matcher (Pandas)                   ││
│  │  - Template Loading                               ││
│  │  - Column Matching                                ││
│  │  - Data Extraction                                ││
│  └──────────────────────────────────────────────────┘│
│  ┌──────────────────────────────────────────────────┐│
│  │         Report Generator                          ││
│  │  ┌───────────────┐  ┌──────────────────────────┐ ││
│  │  │  Grok AI API  │  │  Document Generators     │ ││
│  │  │   (Content)   │  │  - PDF (ReportLab)       │ ││
│  │  │               │  │  - Word (python-docx)    │ ││
│  │  └───────────────┘  └──────────────────────────┘ ││
│  │  ┌──────────────────────────────────────────────┐││
│  │  │  Chart Generator (Matplotlib/Seaborn)        │││
│  │  └──────────────────────────────────────────────┘││
│  └──────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
┌─────────────┐   ┌──────────────┐   ┌──────────────┐
│  Templates  │   │   Uploads    │   │   Reports    │
│  (CSV Files)│   │  (User Data) │   │  (PDF/DOCX)  │
└─────────────┘   └──────────────┘   └──────────────┘
```

---

## ✨ Features

### 1. File Upload & Column Matching
- Upload CSV or Excel files
- Automatic column matching with selected template
- Detailed matching statistics (% match, matched columns, unmatched columns)
- Support for 5 different ESG templates

### 2. Data Extraction
- Extract 8 key columns: Section, Field, Prev Year, Current, Target, Unit, Notes, Input Type
- Flexible column mapping to handle variations in column names
- Complete data validation and cleaning

### 3. AI-Powered Report Generation
- **6 Report Types**:
  1. Comprehensive ESG Report
  2. Environmental Performance Report
  3. Social Impact Report
  4. Governance Report
  5. Compliance & Regulatory Report
  6. Executive Summary

### 4. Document Generation
- **PDF Reports**: Professional layouts using ReportLab
- **Word Documents**: Editable DOCX files using python-docx
- Optional chart inclusion
- Custom styling and formatting

### 5. API Features
- RESTful API design
- Interactive Swagger documentation
- File management (upload, retrieve, delete)
- Background task processing
- CORS support for frontend integration

---

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Python-dotenv**: Environment management

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **OpenPyXL**: Excel file handling

### AI & Content Generation
- **Grok AI API**: Report content generation
- **HTTPx**: Async HTTP client

### Document Generation
- **ReportLab**: PDF generation
- **python-docx**: Word document generation
- **Matplotlib**: Chart generation
- **Seaborn**: Statistical visualization
- **Pillow**: Image processing

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

---

## 📁 File Structure

```
ESG/
├── app/                          # Main application package
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # FastAPI application & endpoints
│   ├── config.py                # Configuration settings
│   ├── models.py                # Pydantic data models
│   ├── prompts.py               # AI prompts for different report types
│   ├── column_matcher.py        # Column matching & data extraction
│   ├── report_generator.py      # Report generation logic
│   └── utils.py                 # Utility functions
│
├── templates/                    # ESG templates
│   ├── ADX_ESG_Template_v2_10.csv
│   ├── DIFC_ESG_Template_v2_10.csv
│   ├── MOCCAE_Compliance_Template_v2_10.csv
│   ├── Schools_Lite_Template_v2_10.csv
│   └── SME_Lite_Template_v2_10.csv
│
├── frontend/                     # Web interface
│   └── index.html               # Single-page application
│
├── uploads/                      # Uploaded files (auto-created)
├── reports/                      # Generated reports (auto-created)
│
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
│
├── Dockerfile                   # Docker image configuration
├── docker-compose.yml          # Docker Compose setup
│
├── run.ps1                     # PowerShell startup script
├── test_matcher.py            # Column matcher test script
├── example_usage.py           # API usage examples
│
├── README.md                  # Main documentation
├── QUICKSTART.md             # Quick start guide
└── PROJECT_DOCUMENTATION.md  # This file
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health & Information
```
GET  /                  - Root endpoint
GET  /health           - Health check
GET  /templates        - List available templates
GET  /report-types     - List report types
GET  /formats          - List output formats
```

#### 2. File Management
```
POST   /upload              - Upload file & match columns
GET    /files/{file_id}     - Get file information
GET    /extract/{file_id}   - Extract data from file
DELETE /files/{file_id}     - Delete file
```

#### 3. Report Generation
```
POST /generate-report        - Generate ESG report
GET  /download-report/{filename} - Download report
```

### Request/Response Examples

#### Upload File
```bash
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: (file) CSV or Excel file
- template: (string) Template name

Response:
{
  "file_id": "uuid",
  "filename": "data.csv",
  "template_used": "ADX_ESG_Template_v2_10.csv",
  "match_result": {
    "matched_columns": ["Section", "Field", ...],
    "unmatched_uploaded": [],
    "unmatched_template": [],
    "match_percentage": 95.5,
    "total_uploaded_columns": 10,
    "total_template_columns": 11
  },
  "message": "File uploaded successfully"
}
```

#### Generate Report
```bash
POST /generate-report
Content-Type: application/json

Body:
{
  "file_id": "uuid",
  "report_format": "pdf",
  "report_type": "comprehensive",
  "include_charts": true
}

Response:
{
  "report_id": "uuid",
  "report_format": "pdf",
  "download_url": "/download-report/esg_report_uuid.pdf",
  "message": "Report generated successfully"
}
```

---

## 🔄 Workflow

### User Flow
1. **Select Template** → Choose from 5 available ESG templates
2. **Upload File** → Upload CSV/Excel with ESG data
3. **Column Matching** → System automatically matches columns
4. **Review Results** → Check matching percentage and mismatches
5. **Extract Data** → View extracted data (optional)
6. **Configure Report** → Select report type and format
7. **Generate Report** → AI generates comprehensive report
8. **Download** → Download PDF or Word document

### Technical Flow
```python
# 1. File Upload
uploaded_file → save_to_disk() → generate_file_id()

# 2. Column Matching
load_template() → load_uploaded_file() → match_columns()
↓
ColumnMatchResult(matched, unmatched, percentage)

# 3. Data Extraction
extract_required_data() → map_columns() → validate_data()
↓
List[ExtractedData]

# 4. Report Generation
format_data_for_ai() → call_grok_api() → generate_content()
↓
create_pdf() or create_docx() → add_charts() → save_report()
↓
ReportResponse(download_url)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+
- pip
- Git
- Docker (optional)

### Quick Start
```powershell
# 1. Clone/Navigate to project
cd d:\Github\ESG

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
.\run.ps1

# 5. Access application
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Frontend: Open frontend/index.html
```

### Docker Setup
```powershell
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 💡 Usage Examples

### Python API Client
```python
import requests

# Upload file
files = {'file': open('data.csv', 'rb')}
data = {'template': 'ADX_ESG_Template_v2_10.csv'}
response = requests.post('http://localhost:8000/upload', 
                        files=files, data=data)
file_id = response.json()['file_id']

# Generate report
report_request = {
    'file_id': file_id,
    'report_format': 'pdf',
    'report_type': 'comprehensive',
    'include_charts': True
}
response = requests.post('http://localhost:8000/generate-report',
                        json=report_request)
download_url = response.json()['download_url']

# Download report
report = requests.get(f'http://localhost:8000{download_url}')
with open('esg_report.pdf', 'wb') as f:
    f.write(report.content)
```

### JavaScript (Frontend)
```javascript
// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('template', 'ADX_ESG_Template_v2_10.csv');

const response = await fetch('http://localhost:8000/upload', {
    method: 'POST',
    body: formData
});
const data = await response.json();
```

---

## 🎨 Customization Guide

### 1. Adding New Report Types

Edit `app/prompts.py`:
```python
CUSTOM_REPORT_PROMPT = """
Generate a custom report based on:
{data}

Include:
1. Custom Section 1
2. Custom Section 2
...
"""

REPORT_PROMPTS['custom'] = CUSTOM_REPORT_PROMPT
```

### 2. Modifying Templates

Add new template CSV to `templates/` folder and update `app/config.py`:
```python
AVAILABLE_TEMPLATES: List[str] = [
    "ADX_ESG_Template_v2_10.csv",
    # Add your template here
    "Custom_Template.csv"
]
```

### 3. Customizing PDF/Word Output

Edit `app/report_generator.py`:
- Modify `PDFReportGenerator` for PDF customization
- Modify `WordReportGenerator` for Word customization
- Adjust styles, colors, fonts, layouts

### 4. Adding Chart Types

Edit `app/report_generator.py`, add to `ChartGenerator` class:
```python
def create_custom_chart(self, data, filename):
    # Your chart logic
    pass
```

---

## 🔧 Configuration Options

### Environment Variables (.env)
```env
GROK_API_KEY=your_api_key
GROK_API_BASE=https://api.x.ai/v1
GROK_MODEL=grok-beta
```

### Application Settings (app/config.py)
```python
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = [".csv", ".xlsx", ".xls"]
REPORT_FORMATS = ["pdf", "docx"]
```

---

## 📊 Supported ESG Templates

1. **ADX ESG Template v2.10**
   - Abu Dhabi Securities Exchange
   - Comprehensive ESG metrics
   - 74 data points

2. **DIFC ESG Template v2.10**
   - Dubai International Financial Centre
   - Financial sector focus

3. **MOCCAE Compliance Template v2.10**
   - Ministry of Climate Change and Environment
   - Environmental compliance

4. **Schools Lite Template v2.10**
   - Educational institutions
   - Simplified metrics

5. **SME Lite Template v2.10**
   - Small and Medium Enterprises
   - Lightweight reporting

---

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Solution: `pip install -r requirements.txt`

2. **API Key Not Found**
   - Solution: Check `.env` file exists with `GROK_API_KEY`

3. **Port Already in Use**
   - Solution: Change port in `run.ps1` or `uvicorn` command

4. **File Upload Fails**
   - Check file size (< 10MB)
   - Verify file format (CSV/XLSX/XLS)
   - Ensure template is selected

5. **Report Generation Slow**
   - Normal for AI generation (30-60 seconds)
   - Check Grok API status
   - Verify API key validity

---

## 📈 Performance Considerations

- File uploads: < 1 second for files < 5MB
- Column matching: < 2 seconds
- Data extraction: < 1 second
- Report generation: 30-60 seconds (AI processing)
- PDF generation: 2-5 seconds
- Word generation: 1-3 seconds

---

## 🔒 Security Considerations

1. **API Key Protection**: Store in `.env`, never commit to Git
2. **File Validation**: Only allow CSV/Excel files
3. **Size Limits**: 10MB max upload size
4. **CORS**: Configure appropriately for production
5. **Input Validation**: All inputs validated with Pydantic
6. **File Cleanup**: Old files automatically deleted after 7 days

---

## 🚢 Deployment

### Production Checklist
- [ ] Update CORS settings in `app/main.py`
- [ ] Set `DEBUG=False` in config
- [ ] Use production-grade database for file metadata
- [ ] Implement authentication/authorization
- [ ] Set up logging and monitoring
- [ ] Configure SSL/TLS
- [ ] Use environment-specific `.env` files
- [ ] Set up backup for uploads/reports
- [ ] Configure rate limiting
- [ ] Use managed Grok API service

---

## 📝 License

Proprietary - All rights reserved

---

## 👥 Support & Contact

For issues, questions, or feature requests, please contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Maintained by**: ESG Development Team
