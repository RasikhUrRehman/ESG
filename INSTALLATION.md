# 🚀 INSTALLATION & RUNNING GUIDE

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.11 or higher installed
- [ ] pip (Python package manager)
- [ ] PowerShell (comes with Windows)
- [ ] 500 MB free disk space
- [ ] Internet connection (for package installation)

---

## 🎯 Quick Start (5 Minutes)

### Step 1: Open PowerShell
```powershell
# Navigate to the project directory
cd d:\Github\ESG
```

### Step 2: Run the Application
```powershell
# This script does everything automatically!
.\run.ps1
```

That's it! The script will:
1. ✅ Create virtual environment (if needed)
2. ✅ Install all dependencies
3. ✅ Check for .env file
4. ✅ Create necessary directories
5. ✅ Start the server

### Step 3: Verify Installation
Open your browser and visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

If you see the Swagger documentation, you're ready to go! 🎉

---

## 📝 Detailed Installation Steps

### Option A: Automatic (Recommended)

```powershell
# 1. Navigate to project
cd d:\Github\ESG

# 2. Run the startup script
.\run.ps1

# The script handles everything!
```

### Option B: Manual Installation

```powershell
# 1. Navigate to project
cd d:\Github\ESG

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify .env file exists
Get-Content .env

# 6. Create directories
New-Item -ItemType Directory -Force -Path "uploads"
New-Item -ItemType Directory -Force -Path "reports"

# 7. Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🐳 Docker Installation (Alternative)

### Prerequisites for Docker
- Docker Desktop installed and running
- Docker Compose installed

### Steps
```powershell
# 1. Navigate to project
cd d:\Github\ESG

# 2. Build and start containers
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Stop containers
docker-compose down
```

---

## 🧪 Testing the Installation

### Test 1: Check API Health
```powershell
# Using curl (if available)
curl http://localhost:8000/health

# Using PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

**Expected Response:**
```json
{"status": "healthy"}
```

### Test 2: List Templates
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/templates" | Select-Object -Expand Content
```

**Expected Response:**
```json
{
  "templates": [
    {
      "name": "ADX_ESG_Template_v2_10.csv",
      "display_name": "ADX ESG Template v2 10",
      ...
    }
  ]
}
```

### Test 3: Run Column Matcher Test
```powershell
python test_matcher.py
```

**Expected Output:**
```
================================================================================
Testing Column Matcher
================================================================================

Available Templates:
  - ADX_ESG_Template_v2_10.csv
  - DIFC_ESG_Template_v2_10.csv
  ...
```

---

## 🌐 Using the Frontend

### Step 1: Open Frontend
```powershell
# Open in default browser
start frontend\index.html

# Or manually open in browser:
# File -> Open -> Browse to d:\Github\ESG\frontend\index.html
```

### Step 2: Ensure API is Running
The frontend connects to: `http://localhost:8000`

Make sure the API is running before using the frontend!

### Step 3: Upload and Generate
1. Select a template from dropdown
2. Choose a CSV/Excel file
3. Click "Upload & Match Columns"
4. Review matching results
5. Select report type and format
6. Click "Generate Report"
6. Download your report!

---

## 🔧 Troubleshooting

### Issue 1: "python" not recognized
**Cause**: Python not in PATH

**Solution**:
```powershell
# Find Python installation
where.exe python

# If not found, reinstall Python and check "Add to PATH"
```

### Issue 2: Cannot activate virtual environment
**Cause**: Execution policy restrictions

**Solution**:
```powershell
# Check current policy
Get-ExecutionPolicy

# Temporarily allow scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Then try again
.\venv\Scripts\Activate.ps1
```

### Issue 3: Port 8000 already in use
**Cause**: Another application using port 8000

**Solution**:
```powershell
# Option 1: Find and kill the process
netstat -ano | findstr :8000
# Note the PID and kill it:
taskkill /PID <PID> /F

# Option 2: Use a different port
uvicorn app.main:app --reload --port 8001
```

### Issue 4: Import errors
**Cause**: Dependencies not installed

**Solution**:
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue 5: .env file not found
**Cause**: Missing environment file

**Solution**:
```powershell
# Create .env file
@"
GROK_API_KEY=your_actual_grok_api_key_here
"@ | Out-File -FilePath .env -Encoding UTF8
```

### Issue 6: Frontend can't connect to API
**Cause**: CORS or API not running

**Solution**:
1. Ensure API is running: http://localhost:8000
2. Check browser console for errors (F12)
3. Verify CORS is enabled in `app/main.py`

---

## 📊 Verification Checklist

After installation, verify:

- [ ] Virtual environment created (`venv/` folder exists)
- [ ] Dependencies installed (no errors when running)
- [ ] .env file present and contains API key
- [ ] `uploads/` directory created
- [ ] `reports/` directory created
- [ ] API accessible at http://localhost:8000
- [ ] Swagger docs load at http://localhost:8000/docs
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Templates endpoint returns 5 templates
- [ ] Frontend opens in browser
- [ ] Frontend can list templates

---

## 🎯 Next Steps After Installation

### 1. Test File Upload
- Prepare a CSV file with ESG data
- Use frontend or API to upload
- Check matching results

### 2. Generate Your First Report
- Upload data file
- Select report type
- Choose PDF or Word format
- Generate and download

### 3. Customize (Optional)
- Edit prompts in `app/prompts.py`
- Modify frontend styling in `frontend/index.html`
- Add custom templates to `templates/` folder

---

## 📚 Documentation Reference

After installation, read these files:

1. **README.md** - Project overview and features
2. **QUICKSTART.md** - Quick start guide
3. **PROJECT_DOCUMENTATION.md** - Complete technical docs
4. **PROJECT_SUMMARY.md** - What's included

---

## 🚀 Running in Different Environments

### Development
```powershell
# Hot reload enabled
uvicorn app.main:app --reload
```

### Production (Local)
```powershell
# No reload, optimized
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Development
```powershell
# With volume mounting for live changes
docker-compose up
```

### Docker Production
```powershell
# Build and run detached
docker-compose up -d --build
```

---

## 🔄 Updating the Application

```powershell
# 1. Pull latest changes (if from Git)
git pull

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Update dependencies
pip install -r requirements.txt --upgrade

# 4. Restart application
# Stop current server (Ctrl+C)
# Start again
.\run.ps1
```

---

## 🛑 Stopping the Application

### If running normally:
```
Press Ctrl+C in the terminal
```

### If running in Docker:
```powershell
docker-compose down
```

### To fully clean up:
```powershell
# Stop server
# Then delete temporary files
Remove-Item -Path uploads\* -Force
Remove-Item -Path reports\* -Force
```

---

## 💡 Tips for Success

1. **Always activate virtual environment** before running commands
2. **Check .env file** has correct API key
3. **Use run.ps1** for easiest startup
4. **Open Swagger docs** to test API endpoints
5. **Check logs** if something doesn't work
6. **Read error messages** - they're usually helpful!

---

## 📞 Getting Help

### Check Logs
```powershell
# Application logs are displayed in terminal
# Look for error messages or warnings
```

### Verify Configuration
```powershell
# Check Python version
python --version

# Check pip version
pip --version

# Check installed packages
pip list
```

### Test Components
```powershell
# Test column matcher
python test_matcher.py

# Test API examples
python example_usage.py
```

---

## ✅ Installation Complete!

If you've followed these steps and all tests pass, your ESG Report Generation System is ready to use!

### What You Can Do Now:
1. ✅ Upload ESG data files
2. ✅ Match columns with templates
3. ✅ Extract data
4. ✅ Generate AI-powered reports
5. ✅ Export to PDF or Word
6. ✅ Download and share reports

---

## 🎉 Success Indicators

You'll know everything works when you can:

1. **Access API Docs** → http://localhost:8000/docs loads
2. **See Templates** → Frontend shows 5 templates
3. **Upload File** → File upload completes without errors
4. **Match Columns** → See matching percentage
5. **Generate Report** → AI creates report successfully
6. **Download** → PDF/Word file downloads correctly

---

**Happy ESG Reporting! 📊✨**

For detailed usage instructions, see README.md or PROJECT_DOCUMENTATION.md
