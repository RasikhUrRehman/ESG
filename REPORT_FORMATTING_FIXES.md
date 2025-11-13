# Report Formatting Fixes

## Changes Made (November 12-13, 2025)

### 1. Fixed Character Encoding Issues ✅

**Problem:** Special characters like tCO₂e were not rendering correctly in reports, appearing as broken text.

**Solution:** 
- Updated system prompt to instruct AI to use "tCO2e" instead of special characters
- Added explicit formatting rules in `SYSTEM_PROMPT`

### 2. Improved Table Formatting ✅

**Problem:** Markdown tables were not being properly converted to formatted tables in PDF/Word documents.

**Solution:**
- Added markdown table parser in both `PDFReportGenerator` and `WordReportGenerator`
- Tables are now properly detected and converted with:
  - Header row styling (green background for PDF, bold for Word)
  - Proper grid lines and borders
  - Alternating row colors for better readability in PDF
  - Word tables use built-in 'Light Grid Accent 1' style

### 3. Removed Generic Company Introductions ✅

**Problem:** Reports included placeholder text like "[Company Name]" and generic introductions.

**Solution:**
- Updated `COMPREHENSIVE_REPORT_PROMPT` to explicitly instruct AI to:
  - NOT include generic company introductions
  - NOT use placeholder text like "[Company Name]", "[Insert X]"
  - Start directly with Executive Summary
  - Only report on actual data provided

### 4. Fixed Empty Charts Issue ✅

**Problem:** Charts were being created even when no data was available, showing empty/placeholder visualizations.

**Solution:**
- Modified all chart generation methods to:
  - Check for actual data availability before creating charts
  - Return `None` if no data exists
  - Only include positive numeric values
  - Log when charts are skipped due to missing data

### 5. Fixed Bold/Italic Formatting ✅

**Problem:** Inline markdown formatting like `**Environmental:**` was not being converted to bold in PDF/Word output.

**Solution:**

#### PDF Generator:
- Added `_convert_markdown_to_html()` method to convert markdown to HTML tags
- Converts `**text**` to `<b>text</b>` for bold
- Converts `*text*` to `<i>text</i>` for italic
- Applied to all paragraph text before rendering

#### Word Generator:
- Added `_add_paragraph_with_formatting()` method to handle inline formatting
- Uses regex to split text and identify bold/italic patterns
- Applies proper Word formatting (bold/italic) to text runs
- Works with list items and regular paragraphs

### 6. Removed Chart Descriptions from AI Output ✅

**Problem:** AI was adding "Suggested Visualizations" sections with placeholder chart descriptions even when no data existed.

**Solution:**
- Updated system prompt to explicitly forbid chart/visualization suggestions
- Removed `CHART_INSTRUCTIONS` from being added to the AI prompt
- Added instruction: "Do NOT add 'Suggested Visualizations' or chart descriptions - charts will be added automatically"
- Charts are now generated separately and added to document without AI involvement

### 7. Smart Column Removal in Tables ✅ (NEW - Nov 13)

**Problem:** Tables included columns with "Not Available" for all rows, making tables cluttered and unhelpful.

**Solution:**
- Updated system prompt with TABLE FORMATTING RULES:
  - Only include columns that have actual data values
  - If a column has "Not Available" or empty values for ALL rows, skip that column
  - Use exact column names from the data source
  - Dynamic table structure based on available data

**Examples:**
- Full data: `Metric | Prev Year | Current | Target | Unit`
- No targets: `Metric | Prev Year | Current | Unit`
- Only current: `Metric | Current | Unit`

### 8. Dynamic Chart Generation Based on Available Data ✅ (NEW - Nov 13)

**Problem:** Fixed 3 charts were attempted regardless of data availability, leading to empty or irrelevant visualizations.

**Solution:**

#### New `analyze_data_for_charts()` Method:
Intelligently analyzes the data to determine what charts can be created:

**Chart Categories Detected:**
1. **Emissions Data** (scope, emission, ghg, co2) → Bar Chart
2. **Energy Data** (energy, renewable, electricity, fuel) → Bar Chart  
3. **Diversity Data** (diversity, gender, female, male, women) → Pie Chart
4. **Social Metrics** (employee, turnover, safety, injury) → Bar Chart
5. **Water Management** (water, consumption, reclamation) → Bar Chart
6. **Waste Management** (waste, recycling, landfill) → Bar Chart
7. **Trend Data** (prev year + current + target) → Line Chart

**Requirements:**
- Minimum 2 data points needed for any chart
- Trend charts need at least 2 of: previous year, current, target
- Only positive numeric values are included
- Limit of 3 trend charts to avoid clutter

#### Chart Creation Flow:
1. Analyze all data for chartable metrics
2. Generate chart specifications for each viable category
3. Create only the charts with sufficient data
4. Log what was created and what was skipped

**Benefits:**
- No empty charts
- Relevant visualizations only
- Scales from 0 charts (no data) to many charts (rich data)
- Automatic selection of appropriate chart types

## Files Modified

1. **app/prompts.py**
   - Updated `SYSTEM_PROMPT` with formatting rules
   - Added TABLE FORMATTING RULES for dynamic columns
   - Rewrote `COMPREHENSIVE_REPORT_PROMPT` recommendations section
   - Added explicit instructions against chart suggestions

2. **app/report_generator.py**
   - Added `analyze_data_for_charts()` - intelligent chart detection
   - Added `_extract_numeric_data()` - extract data by keywords
   - Added `_check_for_trends()` - detect trend data
   - Added `create_chart()` - generic chart creation dispatcher
   - Added `_create_bar_chart()` - bar chart creation
   - Added `_create_pie_chart()` - pie chart creation
   - Added `_create_line_chart()` - trend line chart creation
   - Updated report generation to use dynamic chart analysis
   - Added `_convert_markdown_to_html()` to PDF generator
   - Added `_add_paragraph_with_formatting()` to Word generator
   - Enhanced table parsing for both PDF and Word
   - Kept old chart methods for backward compatibility

## Testing Recommendations

### Basic Tests:
1. ✅ **Test with full data:** Generate report with complete ESG data
2. ✅ **Test with partial data:** Generate report with missing sections
3. ✅ **Test table formatting:** Verify tables render correctly in PDF and Word
4. ✅ **Test character encoding:** Verify "tCO2e" appears correctly
5. ✅ **Test content:** Verify no placeholder text appears
6. ✅ **Test bold formatting:** Verify `**Environmental:**` appears bold

### New Tests (Nov 13):
7. ✅ **Test empty columns:** Verify columns with all "Not Available" are excluded
8. ✅ **Test partial columns:** Verify only populated columns appear
9. ✅ **Test dynamic charts:** Verify correct number of charts based on data
10. ✅ **Test chart variety:** Verify different chart types (bar, pie, line) based on data
11. ✅ **Test no-data scenario:** Verify 0 charts when no chartable data exists
12. ✅ **Test rich-data scenario:** Verify multiple relevant charts created

### Example Test Cases:

**Case 1: Only Current Values**
- Input: Data with only "Current" column filled
- Expected Table: `Metric | Current Value | Unit`
- Expected Charts: Based on available current values

**Case 2: No Target Data**
- Input: Data with Prev Year and Current, no Targets
- Expected Table: `Metric | Prev Year | Current | Unit`
- Expected Charts: May include trend charts with 2 points

**Case 3: Emissions Only**
- Input: Only emissions data available
- Expected Table: One table for emissions
- Expected Charts: 1 bar chart for emissions (if ≥2 data points)

**Case 4: Rich Dataset**
- Input: All categories with data
- Expected Charts: Multiple charts (emissions, energy, diversity, social, water, waste, trends)

## Expected Behavior

### Report with Full Data:
- Tables include all relevant columns with data
- Multiple charts covering different ESG categories
- Proper bold formatting throughout
- No placeholder text
- Professional appearance

### Report with Sparse Data:
- Tables only show columns with actual values
- Only relevant charts are created
- Sections without data are skipped
- Clean, focused presentation
- No empty visualizations

### Report with No Chartable Data:
- Text report with tables
- No "Charts and Visualizations" section
- Still provides analysis of available data
- Professional and complete without charts

## Migration Notes

**Backward Compatibility:**
- Old chart methods (`create_emissions_chart()`, etc.) are retained
- Can still be called directly if needed
- New dynamic system is now the default

**Performance:**
- Single data analysis pass for all charts
- More efficient than creating fixed charts
- Scales better with large datasets

**Extensibility:**
- Easy to add new chart categories
- Just add keywords and chart spec to `analyze_data_for_charts()`
- Customize chart types per category
