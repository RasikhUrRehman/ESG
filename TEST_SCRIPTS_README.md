# ESG Report Generation Test Scripts

This directory contains test scripts for generating ESG reports locally without using the API.

## Test Scripts

### 1. `test_generate_report.py` - Full Featured Test Script

Comprehensive test script with multiple options for testing report generation.

#### Usage Examples:

**Test a single template (both PDF and DOCX):**
```powershell
python test_generate_report.py
```

**Test a specific template:**
```powershell
python test_generate_report.py --template ADX_ESG_Template_v2_10
```

**Generate only PDF:**
```powershell
python test_generate_report.py --format pdf
```

**Generate only DOCX:**
```powershell
python test_generate_report.py --format docx
```

**Test all templates:**
```powershell
python test_generate_report.py --all
```

**Generate executive summary report:**
```powershell
python test_generate_report.py --type executive
```

#### Available Options:

- `--template` : Template name (default: ADX_ESG_Template_v2_10)
  - ADX_ESG_Template_v2_10
  - DIFC_ESG_Template_v2_10
  - MOCCAE_Compliance_Template_v2_10
  - Schools_Lite_Template_v2_10
  - SME_Lite_Template_v2_10

- `--format` : Output format (default: both)
  - pdf
  - docx
  - both

- `--type` : Report type (default: comprehensive)
  - comprehensive
  - executive
  - technical

- `--all` : Test all available templates

### 2. `quick_test_report.py` - Quick Test Script

Simple script for quick testing. No arguments needed.

#### Usage:
```powershell
python quick_test_report.py
```

This will generate both PDF and DOCX reports using the ADX_ESG template.

## Prerequisites

Make sure you have:

1. **Environment Variables Set:**
   - `GROK_API_KEY` must be set in your `.env` file

2. **Dependencies Installed:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Template Files Available:**
   - Templates should be in the `templates/` directory
   - Current templates:
     - ADX_ESG_Template_v2_10.csv
     - DIFC_ESG_Template_v2_10.csv
     - MOCCAE_Compliance_Template_v2_10.csv
     - Schools_Lite_Template_v2_10.csv
     - SME_Lite_Template_v2_10.csv

## Output

Generated reports will be saved in the `reports/` directory with the following naming convention:
- PDF: `test_report_{template}_{format}_{timestamp}.pdf`
- DOCX: `test_report_{template}_{format}_{timestamp}.docx`

## Troubleshooting

### Error: "Template file not found"
Make sure the template files are in the `templates/` directory.

### Error: "Invalid or expired Grok API key"
Check your `.env` file and ensure `GROK_API_KEY` is set correctly.

### Error: "Module not found"
Install dependencies:
```powershell
pip install -r requirements.txt
```

## Examples

### Generate a comprehensive ADX report:
```powershell
python test_generate_report.py --template ADX_ESG_Template_v2_10 --type comprehensive --format pdf
```

### Test all templates and formats:
```powershell
python test_generate_report.py --all
```

### Quick test:
```powershell
python quick_test_report.py
```

## Log Output

The scripts provide detailed logging showing:
- Template loading progress
- Data formatting steps
- Report generation status
- File paths of generated reports
- Error messages if any issues occur

## Notes

- The scripts use the same report generation engine as the main API
- Generated reports will have the same quality and formatting as API-generated reports
- You can customize metadata (company name, period, etc.) by editing the test scripts
- Reports are generated asynchronously using asyncio
