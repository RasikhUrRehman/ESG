# Template System Changes

## Overview
The ESG Report Generator has been updated to use **static column definitions** instead of loading template CSV files. This improves performance and simplifies maintenance.

## Changes Made

### 1. Template Names Updated
The template naming convention has been simplified:

| Old Name | New Name |
|----------|----------|
| `ADX_ESG_Template_v2_10.csv` | `ADX_ESG` |
| `DIFC_ESG_Template_v2_10.csv` | `DIFC_ESG` |
| `MOCCAE_Compliance_Template_v2_10.csv` | `MOCCAE` |
| `Schools_Lite_Template_v2_10.csv` | `SCHOOLS` |
| `SME_Lite_Template_v2_10.csv` | `SME` |

### 2. Static Column Definitions

Each template now has a static column definition in `app/column_matcher.py`:

#### ADX_ESG
```python
[
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
]
```

#### DIFC_ESG
```python
[
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
```

#### MOCCAE
```python
[
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
]
```

#### SCHOOLS
```python
[
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
```

#### SME
```python
[
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
```

### 3. Files Modified

#### `app/models.py`
- Updated `TemplateType` enum with new template names

#### `app/column_matcher.py`
- Removed `load_template()` method
- Removed dependency on template CSV files
- Added `TEMPLATE_COLUMNS` dictionary with static definitions
- Updated `__init__()` to use static columns
- Simplified `get_template_columns()` method

#### `app/config.py`
- Updated `AVAILABLE_TEMPLATES` list with new names

#### `app/main.py`
- Updated `/templates` endpoint to use static column counts
- Removed file path checks (no longer needed)

#### `example_usage.py`
- Updated example to use new template name format

#### `test_matcher.py`
- Updated test to use new template name format

## Benefits

### Performance
- **Faster Initialization**: No file I/O required for template loading
- **Reduced Memory**: No need to load CSV files into DataFrames for column matching
- **Lower Latency**: Instant template column access

### Maintainability
- **Single Source of Truth**: Column definitions in code, not scattered across CSV files
- **Version Control**: Easier to track template changes in git
- **Type Safety**: Column names are explicit and can be validated at compile time

### Simplicity
- **No File Dependencies**: Templates don't need CSV files in the `templates/` folder for column matching
- **Clearer API**: Template names are more intuitive (e.g., `ADX_ESG` vs `ADX_ESG_Template_v2_10.csv`)

## Usage Examples

### API Request
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@data.csv" \
  -F "template=ADX_ESG"
```

### Python Code
```python
from app.column_matcher import ColumnMatcher

# Create matcher with new template name
matcher = ColumnMatcher("ADX_ESG")

# Get columns
columns = matcher.get_template_columns()
print(f"Template has {len(columns)} columns")
```

### Frontend
```javascript
// Select template
const template = "ADX_ESG";

// Upload file
const formData = new FormData();
formData.append('file', file);
formData.append('template', template);

fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData
});
```

## Migration Notes

### For API Users
- Update any code that references old template names (with `.csv` extension)
- Use new simplified names: `ADX_ESG`, `DIFC_ESG`, `MOCCAE`, `SCHOOLS`, `SME`

### For Developers
- To add a new template, add its column list to `TEMPLATE_COLUMNS` in `app/column_matcher.py`
- Add the template name to `TemplateType` enum in `app/models.py`
- Add the template name to `AVAILABLE_TEMPLATES` in `app/config.py`

### Template CSV Files
- The template CSV files in `templates/` folder are still used for **data rows** (validation rules, field definitions, etc.)
- They are just not loaded for **column matching** purposes
- This separation allows for more efficient column matching while preserving template data

## Testing

Run the test script to verify the changes:
```bash
python test_matcher.py
```

## Backward Compatibility

⚠️ **Breaking Change**: This update changes the template naming convention. 

If you have existing code or saved configurations using the old template names, you'll need to update them to use the new names.

## Questions or Issues?

If you encounter any problems with the new template system, please check:
1. Template name matches one of: `ADX_ESG`, `DIFC_ESG`, `MOCCAE`, `SCHOOLS`, `SME`
2. Column definitions in `TEMPLATE_COLUMNS` match your expected template structure
3. API endpoints use the new template names
