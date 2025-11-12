# ESG Report Generation Application

A comprehensive FastAPI application for ESG (Environmental, Social, and Governance) report generation with automated column matching and AI-powered report creation using Grok AI.

## Features

- 📊 **Column Matching**: Automatically match uploaded CSV/Excel files with ESG templates
- 🤖 **AI-Powered Reports**: Generate comprehensive ESG reports using Grok AI
- 📄 **Multiple Formats**: Export reports in PDF or Word (DOCX) format
- 📈 **Data Visualization**: Include charts and graphs in generated reports
- 🔄 **Multiple Templates**: Support for ADX, DIFC, MOCCAE, Schools, and SME templates
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 🔒 **Secure**: Environment-based API key management

## Project Structure

```
ESG/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic models
│   ├── prompts.py           # AI prompts for different report types
│   ├── column_matcher.py    # Column matching logic
│   ├── report_generator.py  # Report generation with Grok AI
│   └── utils.py             # Utility functions
├── templates/               # ESG template files
│   ├── ADX_ESG_Template_v2_10.csv
│   ├── DIFC_ESG_Template_v2_10.csv
│   ├── MOCCAE_Compliance_Template_v2_10.csv
│   ├── Schools_Lite_Template_v2_10.csv
│   └── SME_Lite_Template_v2_10.csv
├── uploads/                 # Uploaded files (auto-created)
├── reports/                 # Generated reports (auto-created)
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .env                    # Environment variables
└── README.md              # This file
```

## Installation

### Local Development

1. **Clone the repository**
   ```bash
   cd d:\Github\ESG
   ```

2. **Create virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Ensure `.env` file contains your Grok API key:
     ```
     GROK_API_KEY=your_grok_api_key_here
     ```

5. **Run the application**
   ```powershell
   uvicorn app.main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Deployment

1. **Build and run with Docker Compose**
   ```powershell
   docker-compose up -d
   ```

2. **View logs**
   ```powershell
   docker-compose logs -f
   ```

3. **Stop the application**
   ```powershell
   docker-compose down
   ```

## API Endpoints

### Core Endpoints

- **GET** `/` - Root endpoint
- **GET** `/health` - Health check
- **GET** `/templates` - List available ESG templates
- **GET** `/report-types` - List available report types
- **GET** `/formats` - List available output formats

### File Operations

- **POST** `/upload` - Upload file and match columns
  - Parameters: `file` (CSV/Excel), `template` (template name)
  - Returns: File ID and column matching results

- **GET** `/files/{file_id}` - Get file information
- **GET** `/extract/{file_id}` - Extract data from uploaded file
- **DELETE** `/files/{file_id}` - Delete uploaded file

### Report Generation

- **POST** `/generate-report` - Generate ESG report
  - Body: 
    ```json
    {
      "file_id": "uuid",
      "report_format": "pdf" | "docx",
      "report_type": "comprehensive",
      "include_charts": true
    }
    ```

- **GET** `/download-report/{filename}` - Download generated report

## Usage Workflow

### 1. Upload File

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your_data.csv" \
  -F "template=ADX_ESG_Template_v2_10.csv"
```

Response:
```json
{
  "file_id": "abc-123-def",
  "filename": "your_data.csv",
  "template_used": "ADX_ESG_Template_v2_10.csv",
  "match_result": {
    "matched_columns": [...],
    "unmatched_uploaded": [...],
    "unmatched_template": [...],
    "match_percentage": 85.5
  }
}
```

### 2. Extract Data

```bash
curl "http://localhost:8000/extract/{file_id}"
```

### 3. Generate Report

```bash
curl -X POST "http://localhost:8000/generate-report" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "abc-123-def",
    "report_format": "pdf",
    "report_type": "comprehensive",
    "include_charts": true
  }'
```

### 4. Download Report

```bash
curl "http://localhost:8000/download-report/{report_filename}.pdf" \
  --output report.pdf
```

## Report Types

1. **Comprehensive** - Full ESG report covering all aspects
2. **Environmental** - Focus on environmental performance
3. **Social** - Social impact and responsibility
4. **Governance** - Corporate governance and oversight
5. **Compliance** - Regulatory compliance status
6. **Executive** - Executive summary

## Templates

- **ADX ESG Template** - Abu Dhabi Securities Exchange ESG reporting
- **DIFC ESG Template** - Dubai International Financial Centre
- **MOCCAE Compliance** - Ministry of Climate Change and Environment
- **Schools Lite** - Educational institutions ESG reporting
- **SME Lite** - Small and Medium Enterprises

## Configuration

Edit `.env` file:

```env
GROK_API_KEY=your_api_key
GROK_API_BASE=https://api.x.ai/v1
GROK_MODEL=grok-beta
```

Edit `app/config.py` for advanced settings:
- Upload size limits
- Allowed file extensions
- Report directory paths

## Development

### Running Tests

```powershell
pytest tests/
```

### Code Formatting

```powershell
black app/
flake8 app/
```

## Technology Stack

- **FastAPI** - Modern web framework
- **Pandas** - Data manipulation and analysis
- **Grok AI** - Report content generation
- **ReportLab** - PDF generation
- **python-docx** - Word document generation
- **Matplotlib/Seaborn** - Chart generation
- **Docker** - Containerization

## Troubleshooting

### Import Errors
If you see import errors, install dependencies:
```powershell
pip install -r requirements.txt
```

### API Key Issues
Ensure your `.env` file has the correct Grok API key.

### File Upload Fails
Check file size (max 10MB) and format (CSV, XLSX, XLS only).

## License

This project is proprietary.

## Support

For issues or questions, please contact the development team.
