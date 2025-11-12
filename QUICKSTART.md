# Quick Start Guide

## Prerequisites
- Python 3.11 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation Steps

### 1. Install Dependencies

```powershell
# Navigate to project directory
cd d:\Github\ESG

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 2. Verify Environment Variables

Ensure your `.env` file contains:
```
GROK_API_KEY=your_actual_grok_api_key_here
```

### 3. Run the Application

#### Option A: Using PowerShell Script (Recommended)
```powershell
.\run.ps1
```

#### Option B: Manual Start
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option C: Using Docker
```powershell
docker-compose up -d
```

### 4. Access the Application

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Frontend UI**: Open `frontend/index.html` in a browser

## Testing the Application

### Test 1: Check API Health
```powershell
curl http://localhost:8000/health
```

### Test 2: List Templates
```powershell
curl http://localhost:8000/templates
```

### Test 3: Column Matching Test
```powershell
python test_matcher.py
```

### Test 4: Upload a File (via Frontend)
1. Open `frontend/index.html` in a browser
2. Select a template from dropdown
3. Choose a CSV/Excel file
4. Click "Upload & Match Columns"

## Common Issues & Solutions

### Issue 1: Import Errors
**Solution**: Install dependencies
```powershell
pip install -r requirements.txt
```

### Issue 2: Port Already in Use
**Solution**: Change port in run.ps1 or use:
```powershell
uvicorn app.main:app --reload --port 8001
```

### Issue 3: CORS Errors in Frontend
**Solution**: Ensure the API is running on http://localhost:8000

### Issue 4: File Upload Fails
**Possible Causes**:
- File too large (max 10MB)
- Invalid format (only CSV, XLSX, XLS allowed)
- Missing template selection

## Project Structure Quick Reference

```
ESG/
├── app/                     # Main application code
│   ├── main.py             # FastAPI endpoints
│   ├── column_matcher.py   # Column matching logic
│   ├── report_generator.py # AI report generation
│   ├── config.py           # Configuration
│   ├── models.py           # Data models
│   ├── prompts.py          # AI prompts
│   └── utils.py            # Helper functions
├── templates/              # ESG templates
├── uploads/               # Uploaded files (auto-created)
├── reports/              # Generated reports (auto-created)
├── frontend/             # Simple web UI
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
└── docker-compose.yml   # Docker Compose setup
```

## Next Steps

1. **Upload Your Data**: Use the frontend or API to upload ESG data files
2. **Review Matching**: Check column matching results
3. **Generate Reports**: Create comprehensive ESG reports in PDF or Word format
4. **Customize**: Modify prompts in `app/prompts.py` for custom report styles

## Support

- Check API documentation at http://localhost:8000/docs
- Review logs for detailed error messages
- Ensure all dependencies are installed correctly
