# API Split Implementation Summary

## Overview

The `/upload` API has been successfully split into two separate endpoints with enhanced change analysis functionality. This provides better user control over column mapping and automatic calculation of performance changes.

---

## Changes Made

### 1. New API Endpoints

#### **`POST /compare-columns`**
- **Purpose**: Upload file and extract columns for user review
- **Input**: File + Template selection
- **Output**: File ID, template columns, uploaded file columns
- **Supports**: CSV, Excel (.xlsx, .xls), Word (.docx)

#### **`POST /map-columns`**
- **Purpose**: Process data with user-confirmed column mappings
- **Input**: File ID + Column mappings
- **Output**: Matched data with **change analysis** (change_percentage, status)
- **New Features**:
  - `change_percentage`: % change from Prev Year to Current
  - `status`: "improved", "worsened", or "slight" based on metric type

### 2. Enhanced Data Models

#### New Models (`app/models.py`):
```python
class CompareColumnsResponse(BaseModel):
    """Response for /compare-columns endpoint"""
    file_id: str
    filename: str
    template_used: str
    template_columns: List[str]
    uploaded_columns: List[str]
    message: str

class ColumnMapping(BaseModel):
    """Column mapping definition"""
    template_column: str
    uploaded_column: Optional[str]  # None if not mapped

class ColumnMappingRequest(BaseModel):
    """Request for /map-columns endpoint"""
    file_id: str
    mappings: List[ColumnMapping]

class MapColumnsResponse(BaseModel):
    """Response for /map-columns endpoint"""
    file_id: str
    filename: str
    template_used: str
    match_result: ColumnMatchResult
    message: str
    data: List[Dict[str, Any]]  # Now includes change_percentage and status
```

### 3. Enhanced Column Matcher (`app/column_matcher.py`)

#### New Methods:
```python
async def extract_columns_only(file_path: Path) -> List[str]:
    """Extract only column names without full processing"""
    # Handles CSV, Excel, and Word files
    # Uses Grok AI for Word documents to identify fields

async def extract_columns_from_text(text_content: str) -> List[str]:
    """Use Grok AI to extract column names from unstructured text"""
    # For Word documents and unstructured Excel files

async def process_file_with_mappings(file_path: Path, mappings: List[Any]) -> Tuple[...]:
    """Process file with user-provided column mappings"""
    # Applies user's mapping decisions
    # Returns matched data with change analysis

async def apply_column_mappings(raw_df: pd.DataFrame, mapping_dict: Dict) -> pd.DataFrame:
    """Apply user-provided column mappings to raw dataframe"""
    # Maps columns according to user selection
```

### 4. Change Analysis Integration

The `calculate_change_analysis()` function is now integrated into the `/map-columns` response:

#### Change Analysis Logic:
- **Calculates**: `((Current - Prev Year) / Prev Year) * 100`
- **Status Determination**:
  - `"improved"`: Positive change (context-aware)
  - `"worsened"`: Negative change (context-aware)
  - `"slight"`: Change within ±5%
  - `null`: No data or non-numeric values

#### Metrics Where Lower is Better:
- Emissions (GHG, CO2)
- Waste, Discharge
- Energy/Water Consumption
- Employee Turnover
- Accidents/Incidents
- Pay Gap

---

## File Changes

### Modified Files:
1. **`app/main.py`**
   - Added `/compare-columns` endpoint
   - Added `/map-columns` endpoint with change analysis
   - Kept `/upload` endpoint (marked as DEPRECATED)
   - Added intermediate storage for multi-step processing

2. **`app/models.py`**
   - Added `CompareColumnsResponse`
   - Added `ColumnMapping`
   - Added `ColumnMappingRequest`
   - Added `MapColumnsResponse`

3. **`app/column_matcher.py`**
   - Added `extract_columns_only()` method
   - Added `extract_columns_from_text()` method
   - Added `process_file_with_mappings()` method
   - Added `apply_column_mappings()` method
   - Added `create_match_result_from_mappings()` method

### New Files:
1. **`API_SPLIT_GUIDE.md`**
   - Comprehensive documentation for new split API
   - Usage examples with curl and JavaScript
   - Change analysis field descriptions

2. **`test_split_api.py`**
   - Test script for new split API flow
   - Demonstrates column comparison and mapping
   - Shows change analysis results

3. **`frontend/index_split_api.html`**
   - Interactive demo of split API
   - Visual change analysis display
   - Auto-mapping with user review

---

## Response Example

### `/map-columns` Response with Change Analysis:

```json
{
  "file_id": "abc-123",
  "filename": "esg_data.csv",
  "template_used": "ADX_ESG",
  "match_result": {
    "matched_columns": ["Section", "Field (EN)", "Prev Year", "Current", ...],
    "match_percentage": 95.0,
    ...
  },
  "message": "Data perfectly mapped to template",
  "data": [
    {
      "Section": "Environmental",
      "Field (EN)": "Total GHG Emissions",
      "Prev Year": "1000",
      "Current": "950",
      "Target": "900",
      "Unit": "tCO2e",
      "change_percentage": -5.0,
      "status": "improved"  // Lower emissions = improved
    },
    {
      "Section": "Social",
      "Field (EN)": "Employee Training Hours",
      "Prev Year": "20",
      "Current": "25",
      "Target": "30",
      "Unit": "hours",
      "change_percentage": 25.0,
      "status": "improved"  // More training = improved
    },
    {
      "Section": "Social",
      "Field (EN)": "Employee Turnover",
      "Prev Year": "10",
      "Current": "12",
      "Target": "8",
      "Unit": "%",
      "change_percentage": 20.0,
      "status": "worsened"  // Higher turnover = worsened
    }
  ]
}
```

---

## Usage Flow

### 1. Compare Columns
```bash
curl -X POST "http://localhost:8000/compare-columns" \
  -F "file=@data.csv" \
  -F "template=ADX_ESG"
```

### 2. Review & Map Columns
```bash
curl -X POST "http://localhost:8000/map-columns" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "abc-123",
    "mappings": [
      {"template_column": "Section", "uploaded_column": "Category"},
      {"template_column": "Field (EN)", "uploaded_column": "Field Name"},
      ...
    ]
  }'
```

### 3. Analyze Results
The response includes:
- All mapped data
- `change_percentage` for each record
- `status` indicator (improved/worsened/slight)
- Summary statistics in frontend

---

## Benefits

### 1. **User Control**
- Users review column mappings before processing
- Reduces errors from incorrect auto-matching
- Transparent mapping process

### 2. **Change Analysis**
- Automatic calculation of YoY changes
- Context-aware status determination
- Immediate insights into performance trends

### 3. **Word File Support**
- Extracts fields from unstructured documents
- Uses Grok AI for intelligent field detection
- Same mapping workflow as CSV/Excel

### 4. **Backward Compatibility**
- Original `/upload` endpoint still available
- Marked as DEPRECATED for new integrations
- Gradual migration path

---

## Testing

### Run Test Script:
```bash
python test_split_api.py uploads/test.csv ADX_ESG
```

### View Frontend Demo:
```bash
# Start the API server
docker-compose up -d

# Open in browser
open frontend/index_split_api.html
```

---

## Change Analysis Details

### Calculation:
```
change_percentage = ((Current - Prev Year) / Prev Year) * 100
```

### Status Logic:
```python
if abs(change_percentage) <= 5:
    status = "slight"
elif change_percentage > 5:
    status = "improved" if higher_is_better else "worsened"
else:  # change_percentage < -5
    status = "worsened" if higher_is_better else "improved"
```

### Auto-Detection Keywords:
Fields containing these keywords are marked as "lower is better":
- emission, ghg, co2
- waste, discharge
- consumption (in negative context)
- intensity, turnover
- accident, incident
- gap (e.g., pay gap)

---

## Future Enhancements

1. **Machine Learning Column Matching**
   - Train model on common column mappings
   - Suggest most likely mappings

2. **Advanced Change Analysis**
   - Trend analysis over multiple years
   - Anomaly detection
   - Predictive targets

3. **Batch Processing**
   - Upload multiple files at once
   - Aggregate change analysis

4. **Export Options**
   - Export mappings as template
   - Save mapping configurations
   - Reuse mappings for similar files

---

## API Documentation

Full interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

All new endpoints are documented with:
- Request/response schemas
- Example payloads
- Field descriptions
- Error responses
