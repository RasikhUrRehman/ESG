# Quick Reference: Change Analysis in /map-columns

## What Was Added

The `/map-columns` endpoint now automatically adds **change analysis** to each data record:

### New Fields in Response Data

Every record in the `data` array now includes:

```json
{
  // ... existing fields from your CSV/Excel/Word file ...
  "change_percentage": -5.0,     // % change from Prev Year to Current
  "status": "improved"            // improved | worsened | slight | null
}
```

---

## Examples

### Example 1: GHG Emissions (Lower is Better)
```json
{
  "Field (EN)": "Total GHG Emissions",
  "Prev Year": "1000",
  "Current": "950",
  "Unit": "tCO2e",
  "change_percentage": -5.0,
  "status": "improved"  // ✅ Decreased by 5% = Good!
}
```

### Example 2: Employee Training (Higher is Better)
```json
{
  "Field (EN)": "Training Hours per Employee",
  "Prev Year": "20",
  "Current": "25",
  "Unit": "hours",
  "change_percentage": 25.0,
  "status": "improved"  // ✅ Increased by 25% = Good!
}
```

### Example 3: Employee Turnover (Lower is Better)
```json
{
  "Field (EN)": "Employee Turnover Rate",
  "Prev Year": "10",
  "Current": "12",
  "Unit": "%",
  "change_percentage": 20.0,
  "status": "worsened"  // ❌ Increased by 20% = Bad!
}
```

### Example 4: Slight Change
```json
{
  "Field (EN)": "Board Diversity",
  "Prev Year": "40",
  "Current": "41",
  "Unit": "%",
  "change_percentage": 2.5,
  "status": "slight"  // ⚠️ Only 2.5% change = Slight
}
```

---

## Status Logic

| Change % | Metric Type | Status |
|----------|-------------|--------|
| > +5% | Higher is better | ✅ improved |
| > +5% | Lower is better | ❌ worsened |
| < -5% | Higher is better | ❌ worsened |
| < -5% | Lower is better | ✅ improved |
| ±5% or less | Any | ⚠️ slight |
| No data | Any | ⊝ null |

---

## Metrics Where Lower is Better (Auto-Detected)

The system automatically detects these keywords in field names:
- **emission**, **ghg**, **co2** (environmental impact)
- **waste**, **discharge** (waste management)
- **consumption** (resource usage)
- **intensity** (energy/carbon intensity)
- **turnover** (employee turnover)
- **accident**, **incident** (safety)
- **gap** (e.g., pay gap, diversity gap)

---

## API Response Summary

After calling `/map-columns`, you get:

```json
{
  "file_id": "...",
  "filename": "...",
  "template_used": "...",
  "match_result": { ... },
  "message": "...",
  "data": [
    {
      // Your mapped columns
      "Section": "Environmental",
      "Field (EN)": "Total GHG Emissions",
      "Prev Year": "1000",
      "Current": "950",
      
      // 🆕 AUTO-ADDED CHANGE ANALYSIS
      "change_percentage": -5.0,
      "status": "improved"
    },
    // ... more records ...
  ]
}
```

---

## Summary Statistics

The frontend demo (`frontend/index_split_api.html`) shows:

```
┌─────────────┬───────────┬─────────┬──────────┐
│ ✅ Improved │ ❌ Worsened│ ⚠️ Slight│ ⊝ No Data│
│     15      │     8      │    12   │    5     │
└─────────────┴───────────┴─────────┴──────────┘
```

---

## Usage

1. **Upload & Compare**: `POST /compare-columns`
2. **Map Columns**: `POST /map-columns` (returns data with change analysis)
3. **Use the data**: Each record has `change_percentage` and `status`

That's it! The change analysis is automatic. 🎉
