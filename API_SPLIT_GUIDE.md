# API Split Guide - Column Comparison and Mapping

## Overview

The `/upload` API has been split into two separate endpoints to provide better control over column matching and mapping:

1. **`/compare-columns`**: Upload file and compare columns (returns columns for user review)
2. **`/map-columns`**: Apply user-confirmed column mappings and extract data

The original `/upload` endpoint is still available for backward compatibility but is now **deprecated**.

---

## API Flow

### Step 1: Compare Columns

**Endpoint:** `POST /compare-columns`

**Purpose:** Upload a file and get a list of columns from both the template and the uploaded file.

**Request:**
```bash
curl -X POST "http://localhost:8000/compare-columns" \
  -F "file=@your_file.csv" \
  -F "template=ADX_ESG"
```

**Response:**
```json
{
  "file_id": "abc123-def456-ghi789",
  "filename": "your_file.csv",
  "template_used": "ADX_ESG",
  "template_columns": [
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
  ],
  "uploaded_columns": [
    "Company Section",
    "Field Name",
    "Arabic Field",
    "Previous Year Data",
    "Current Year Data",
    "Target Value",
    "Measurement Unit",
    "Additional Notes",
    "Required",
    "Type",
    "Dropdown Options"
  ],
  "message": "Found 11 columns in uploaded file. Please review and confirm mapping."
}
```

---

### Step 2: Map Columns

**Endpoint:** `POST /map-columns`

**Purpose:** Submit the user's column mapping decisions and process the data.

**Request:**
```bash
curl -X POST "http://localhost:8000/map-columns" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "abc123-def456-ghi789",
    "mappings": [
      {
        "template_column": "Section / القسم",
        "uploaded_column": "Company Section"
      },
      {
        "template_column": "Field (EN)",
        "uploaded_column": "Field Name"
      },
      {
        "template_column": "الحقل (AR)",
        "uploaded_column": "Arabic Field"
      },
      {
        "template_column": "Prev Year",
        "uploaded_column": "Previous Year Data"
      },
      {
        "template_column": "Current",
        "uploaded_column": "Current Year Data"
      },
      {
        "template_column": "Target",
        "uploaded_column": "Target Value"
      },
      {
        "template_column": "Unit",
        "uploaded_column": "Measurement Unit"
      },
      {
        "template_column": "Notes",
        "uploaded_column": "Additional Notes"
      },
      {
        "template_column": "Applicability",
        "uploaded_column": "Required"
      },
      {
        "template_column": "Input Type",
        "uploaded_column": "Type"
      },
      {
        "template_column": "Options",
        "uploaded_column": "Dropdown Options"
      }
    ]
  }'
```

**Response:**
```json
{
  "file_id": "abc123-def456-ghi789",
  "filename": "your_file.csv",
  "template_used": "ADX_ESG",
  "match_result": {
    "matched_columns": [
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
    ],
    "unmatched_uploaded": [],
    "unmatched_template": [],
    "match_percentage": 100.0,
    "total_uploaded_columns": 11,
    "total_template_columns": 11,
    "has_ambiguity": false,
    "ambiguity_message": null
  },
  "message": "Data perfectly mapped to template",
  "data": [
    {
      "Section / القسم": "Environmental",
      "Field (EN)": "Total GHG Emissions",
      "الحقل (AR)": "إجمالي انبعاثات الغازات",
      "Prev Year": "1000",
      "Current": "950",
      "Target": "900",
      "Unit": "tCO2e",
      "Notes": "Reduced by implementing energy efficiency measures",
      "Applicability": "All",
      "Input Type": "Number",
      "Options": "",
      "change_percentage": -5.0,
      "status": "improved"
    },
    {
      "Section / القسم": "Environmental",
      "Field (EN)": "Water Consumption",
      "الحقل (AR)": "استهلاك المياه",
      "Prev Year": "500",
      "Current": "480",
      "Target": "450",
      "Unit": "m³",
      "Notes": "",
      "Applicability": "All",
      "Input Type": "Number",
      "Options": "",
      "change_percentage": -4.0,
      "status": "slight"
    },
    {
      "Section / القسم": "Social",
      "Field (EN)": "Employee Turnover Rate",
      "الحقل (AR)": "معدل دوران الموظفين",
      "Prev Year": "15",
      "Current": "18",
      "Target": "12",
      "Unit": "%",
      "Notes": "",
      "Applicability": "All",
      "Input Type": "Number",
      "Options": "",
      "change_percentage": 20.0,
      "status": "worsened"
    }
    // ... more data rows
  ]
}
```

### Change Analysis Fields

Each data record now includes two additional fields:

- **`change_percentage`**: The percentage change from "Prev Year" to "Current" (calculated as: `((Current - Prev Year) / Prev Year) * 100`)
  - Positive value = increase
  - Negative value = decrease
  - `null` if calculation not possible (missing data or non-numeric values)

- **`status`**: Status of the change based on the metric type and change percentage
  - `"improved"`: Positive change (increase for metrics where higher is better, decrease for metrics where lower is better)
  - `"worsened"`: Negative change (decrease for metrics where higher is better, increase for metrics where lower is better)
  - `"slight"`: Change within ±5% (considered insignificant)
  - `null` if calculation not possible

**Metrics where lower is better** (automatically detected):
- Emissions (GHG, CO2)
- Waste
- Discharge
- Consumption (negative context)
- Intensity
- Turnover (employee)
- Accidents/Incidents
- Pay gap
```

---

## Word/Excel File Support

### For Word Documents (.docx)

When a Word document is uploaded:

1. **`/compare-columns`**: 
   - Extracts text from the document
   - Uses Grok AI to identify data fields/columns
   - Returns identified field names for user review

2. **`/map-columns`**:
   - Maps the identified fields to template columns based on user selection
   - Extracts data from the document using Grok AI
   - Returns structured data

**Example Word File Flow:**

```bash
# Step 1: Upload Word file
curl -X POST "http://localhost:8000/compare-columns" \
  -F "file=@esg_report.docx" \
  -F "template=MOCCAE"

# Response will include extracted field names like:
# "uploaded_columns": ["Company Name", "Reporting Year", "Total Emissions", "Energy Consumption", ...]

# Step 2: Map the fields
curl -X POST "http://localhost:8000/map-columns" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "word-file-id",
    "mappings": [
      {"template_column": "Field (EN)", "uploaded_column": "Company Name"},
      {"template_column": "Current / العام الحالي", "uploaded_column": "Total Emissions"},
      // ... other mappings
    ]
  }'
```

---

## Frontend Integration Example

### React/JavaScript Example

```javascript
// Step 1: Upload file and get columns
async function compareColumns(file, template) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('template', template);
  
  const response = await fetch('/compare-columns', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  return data;
}

// Step 2: User reviews and confirms mappings in UI
// Then submit the mappings

async function mapColumns(fileId, mappings) {
  const response = await fetch('/map-columns', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      file_id: fileId,
      mappings: mappings
    })
  });
  
  const data = await response.json();
  return data;
}

// Example usage
const file = document.getElementById('fileInput').files[0];
const template = 'ADX_ESG';

// Step 1: Get columns
const compareResult = await compareColumns(file, template);

// Display columns to user for mapping
// ... UI code to let user map columns ...

// Step 2: Submit mappings
const userMappings = [
  { template_column: 'Section / القسم', uploaded_column: 'Company Section' },
  { template_column: 'Field (EN)', uploaded_column: 'Field Name' },
  // ... more mappings
];

const mapResult = await mapColumns(compareResult.file_id, userMappings);

// Use mapResult.data for further processing
console.log(mapResult.data);
```

---

## Key Benefits

1. **User Control**: Users can review and confirm column mappings before processing
2. **Better Accuracy**: Reduces errors by letting users verify mappings
3. **Flexibility**: Supports manual mapping corrections
4. **Transparency**: Users see exactly which columns are being mapped
5. **Word File Support**: Intelligently extracts fields from unstructured documents

---

## Backward Compatibility

The original `/upload` endpoint is still available but marked as **DEPRECATED**:

```bash
# Still works, but not recommended for new integrations
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your_file.csv" \
  -F "template=ADX_ESG"
```

This endpoint automatically processes the file without user review, which may lead to incorrect mappings in some cases.

---

## Error Handling

### Common Errors

1. **File not found (404)**:
   ```json
   {
     "detail": "File not found or session expired. Please upload the file again."
   }
   ```
   Solution: Re-upload the file using `/compare-columns`

2. **Invalid template (400)**:
   ```json
   {
     "detail": "Invalid template. Available templates: ['ADX_ESG', 'DIFC_ESG', 'MOCCAE', 'SCHOOLS', 'SME']"
   }
   ```
   Solution: Use one of the available template names

3. **Invalid file type (400)**:
   ```json
   {
     "detail": "Invalid file type. Allowed: ['.csv', '.xlsx', '.xls', '.docx']"
   }
   ```
   Solution: Upload a supported file format

---

## Testing

Test the new APIs using the provided test scripts or Swagger UI at `http://localhost:8000/docs`

1. Navigate to `/docs`
2. Find the `/compare-columns` endpoint
3. Click "Try it out"
4. Upload a test file and select a template
5. Copy the `file_id` from the response
6. Navigate to `/map-columns` endpoint
7. Submit your column mappings using the `file_id`

