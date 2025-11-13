"""
Prompts for different types of ESG reports using Grok AI
"""

# Base system prompt for ESG reporting
SYSTEM_PROMPT = """You are an expert ESG (Environmental, Social, and Governance) analyst and report writer. 
Your role is to generate comprehensive, professional, and data-driven ESG reports based on the provided data.
You should follow international standards like GRI, SASB, TCFD, and IFRS S1/S2 where applicable.
Always maintain a professional tone and ensure accuracy in data interpretation.

IMPORTANT FORMATTING RULES:
1. Use "tCO2e" (not tCO₂e) for carbon emissions - write it as: tCO2e
2. Use "CO2e" for carbon dioxide equivalent
3. For tables, use proper markdown table formatting with pipes (|) and hyphens (-)
4. Do NOT include generic company introductions or placeholder text
5. Do NOT write things like "[Company Name]", "[Insert data]", or "[Field Name]"
6. Only report on ACTUAL data provided - do not make assumptions or add placeholders
7. If data is not available for a section, skip that section entirely
8. Do NOT add "Suggested Visualizations" or chart descriptions - charts will be added automatically
9. Do NOT add placeholder recommendations like "once data is provided" - only give specific recommendations based on actual data
10. Use **bold** for emphasis on section labels like **Environmental:** or **Social:**

TABLE FORMATTING RULES:
- ALWAYS include tables when data exists - tables are required for reporting
- Only remove a column if it is COMPLETELY EMPTY for ALL rows (e.g., every single row shows "Not Available" or empty)
- If a column has values for even ONE row, KEEP that column in the table
- Use the exact column names from the data (e.g., "Prev Year", "Current", "Target", "Response")
- Example of column to REMOVE: Target column where ALL rows = "Not Available"
- Example of column to KEEP: Target column where SOME rows have values and some are "Not Available"
- Standard table format: | Metric | Current Value | Unit | Target |
- If all metrics have data in all columns, use all columns
- Tables MUST be included - do not skip the table section"""


# Comprehensive ESG Report Prompt
COMPREHENSIVE_REPORT_PROMPT = """
Generate a comprehensive ESG report based ONLY on the actual data provided below. Do NOT add placeholders, generic introductions, or fictional company information.

{data}

STRICT REQUIREMENTS:
- ALWAYS include tables for each section where data exists
- Only report on metrics that have actual data values in at least one column
- Do NOT skip sections if there is any data available
- Only remove columns that are 100% empty across all rows
- Use proper markdown table formatting with aligned columns
- Write "tCO2e" for carbon emissions (not symbols)
- Do NOT include any text like "[Company Name]", "[Insert X]", or "[Field]"
- Do NOT add a company introduction section
- Start directly with the Executive Summary of ACTUAL performance data
- Charts will be added automatically - do not describe them in text

The report should include ONLY THE FOLLOWING SECTIONS WHERE DATA EXISTS:

## Executive Summary
Provide a brief overview of the actual ESG performance based on the data provided. Include only key highlights that have real numbers.

## Key Highlights and Achievements
List specific achievements with actual metrics from the data. Include this section if there is any reportable data.

**Environmental:**
- Report actual emissions data in format: "Achieved X tCO2e in Scope 1 emissions, Y tCO2e in Scope 2, and Z tCO2e in Scope 3"
- Only include metrics that have actual values (not "Not Available")
- If no environmental data exists, skip this subsection

**Social:**
- Report actual diversity percentages, turnover rates, safety metrics
- Format: "Maintained a workforce diversity rate of X% and a gender pay gap of Y%"
- Only include metrics with actual values
- If no social data exists, skip this subsection

**Governance:**
- Report actual board composition and independence percentages
- Only if data is available
- If no governance data exists, skip this subsection

## Environmental Performance
REQUIRED: Create a properly formatted table with actual data. Include this section if ANY environmental data exists.

Table format - only exclude a column if it's 100% empty for all rows:
| Metric | Current Value | Unit | Target |
|--------|--------------|------|--------|
| [List all metrics with at least one value] |

Rules for columns:
- If "Target" has values for ANY metric, include the Target column
- If "Target" is empty for ALL metrics, exclude the Target column
- Same logic applies to "Prev Year", "Current", etc.

After the table, provide analysis only on metrics with actual values.

## Social Performance
REQUIRED: Create a properly formatted table with actual data. Include this section if ANY social data exists.

Follow same column rules as Environmental Performance.

## Governance Structure
REQUIRED: Create a properly formatted table with actual data. Include this section if ANY governance data exists.

Follow same column rules as Environmental Performance.

## Regulatory Compliance Status
REQUIRED: Create a properly formatted table with actual compliance data. Include this section if ANY compliance data exists.

## Sustainability Reporting Frameworks Used
Only list frameworks if explicitly mentioned in the data.

## Recommendations
Provide specific, data-driven recommendations based on the actual metrics. Use this format:

**Environmental:** [Specific recommendation based on actual environmental data]
**Social:** [Specific recommendation based on actual social data]
**Governance:** [Specific recommendation based on actual governance data]

Do NOT add:
- Generic recommendations without data
- Phrases like "once data is provided"
- Placeholder text
- Chart or visualization suggestions (charts are added automatically)

If you cannot provide specific recommendations due to lack of data, skip this section entirely.

REMEMBER: 
- Use "tCO2e" not special characters
- Format all tables properly with markdown
- Use **bold** for labels like **Environmental:** and **Social:**
- Do NOT add any chart descriptions or visualization suggestions
- Only include content where actual data exists"""


# Environmental Focus Report Prompt
ENVIRONMENTAL_REPORT_PROMPT = """
Generate a focused Environmental Performance Report based on the following data:

{data}

The report should include:

1. EXECUTIVE SUMMARY
   - Overview of environmental performance
   - Key environmental metrics and trends

2. CLIMATE AND EMISSIONS
   - Detailed breakdown of Scope 1, 2, and 3 emissions
   - Emission intensity metrics
   - Carbon reduction initiatives
   - Comparison with baseline year
   - Progress towards emission targets

3. ENERGY MANAGEMENT
   - Total energy consumption
   - Renewable energy share
   - Energy intensity metrics
   - Energy efficiency initiatives

4. WATER STEWARDSHIP
   - Water consumption and sources
   - Water reclamation and recycling
   - Water discharge volumes
   - Water conservation measures

5. WASTE MANAGEMENT
   - Total waste generated
   - Waste recycling rates
   - Waste reduction initiatives
   - Circular economy practices

6. ENVIRONMENTAL INVESTMENTS
   - Climate-related investments
   - Green technology adoption
   - Research and development in sustainability

7. ENVIRONMENTAL GOVERNANCE
   - Environmental policies and procedures
   - Compliance with environmental regulations
   - Environmental risk management

8. RECOMMENDATIONS
   - Priority environmental improvements
   - Best practices for environmental management

Use markdown formatting and include specific data points with units.
"""


# Social Impact Report Prompt
SOCIAL_REPORT_PROMPT = """
Generate a Social Impact and Responsibility Report based on the following data:

{data}

The report should include:

1. EXECUTIVE SUMMARY
   - Overview of social performance
   - Key social impact achievements

2. WORKFORCE DIVERSITY AND INCLUSION
   - Gender diversity ratios
   - Board and management diversity
   - Diversity initiatives and programs
   - Progress towards diversity targets

3. EMPLOYEE WELLBEING AND SAFETY
   - Lost Time Injury Rate (LTIR)
   - Occupational health and safety policies
   - Employee health programs
   - Safety training and awareness

4. FAIR LABOR PRACTICES
   - Gender pay ratio analysis
   - Employee compensation equity
   - Temporary and contract worker percentages
   - Fair employment policies

5. TALENT MANAGEMENT
   - Employee turnover rates
   - Training and development programs
   - Career progression opportunities
   - Employee engagement initiatives

6. COMMUNITY ENGAGEMENT
   - Community investment as percentage of revenue
   - Social impact programs
   - Stakeholder engagement
   - Local community benefits

7. HUMAN RIGHTS
   - Non-discrimination policies
   - Human rights due diligence
   - Grievance mechanisms
   - Labor rights protection

8. RECOMMENDATIONS
   - Priority areas for social improvement
   - Best practices for workforce management

Format professionally with data tables and clear metrics.
"""


# Governance Report Prompt
GOVERNANCE_REPORT_PROMPT = """
Generate a Corporate Governance and ESG Oversight Report based on the following data:

{data}

The report should include:

1. EXECUTIVE SUMMARY
   - Overview of governance structure
   - Key governance highlights

2. BOARD STRUCTURE AND COMPOSITION
   - Board independence metrics
   - Board diversity analysis
   - Committee structure (Audit, Risk, ESG)
   - Director expertise and qualifications

3. ESG GOVERNANCE
   - Board oversight of ESG matters
   - Management oversight of ESG
   - ESG committee responsibilities
   - ESG integration in decision-making

4. EXECUTIVE COMPENSATION
   - CEO pay ratio
   - ESG-linked executive compensation
   - Compensation philosophy and structure
   - Alignment with performance

5. RISK MANAGEMENT
   - Climate risk management processes
   - Enterprise risk management framework
   - Risk identification and mitigation
   - Scenario analysis and stress testing

6. ETHICS AND COMPLIANCE
   - Code of conduct
   - Anti-corruption policies
   - Whistleblowing mechanisms
   - Data privacy policies
   - Compliance violations and penalties

7. TRANSPARENCY AND DISCLOSURE
   - Sustainability reporting practices
   - Frameworks and standards used
   - External assurance
   - Stakeholder communication

8. RECOMMENDATIONS
   - Governance improvement opportunities
   - Best practices for ESG oversight

Use professional formatting with clear governance metrics.
"""


# Compliance and Regulatory Report Prompt
COMPLIANCE_REPORT_PROMPT = """
Generate a Compliance and Regulatory Status Report based on the following data:

{data}

The report should include:

1. EXECUTIVE SUMMARY
   - Compliance status overview
   - Key regulatory requirements

2. REGULATORY FRAMEWORK
   - Applicable ESG regulations
   - Reporting requirements
   - Compliance deadlines

3. COMPLIANCE STATUS
   - NRCC registration status (if applicable)
   - Sustainability reporting compliance
   - Environmental permit compliance
   - Social compliance requirements

4. VIOLATIONS AND PENALTIES
   - Previous violations count
   - Violation severity assessment
   - Estimated fines and penalties
   - Corrective actions taken

5. DISCLOSURE REQUIREMENTS
   - Mandatory disclosures
   - Voluntary disclosures
   - Reporting frameworks used (GRI, SASB, TCFD, IFRS)

6. ASSURANCE AND VERIFICATION
   - External assurance status
   - Third-party verification
   - Assurance scope and methodology

7. CARBON CREDITS AND TRADING
   - Carbon credit registration
   - Estimated carbon credits
   - Carbon pricing and ROI
   - Trading opportunities

8. RECOMMENDATIONS
   - Compliance improvement actions
   - Risk mitigation strategies

Format with compliance checklists and status indicators.
"""


# Executive Summary Prompt
EXECUTIVE_SUMMARY_PROMPT = """
Generate a concise Executive Summary for ESG performance based on the following data:

{data}

The summary should include:

1. COMPANY ESG OVERVIEW
   - Brief introduction
   - Reporting period

2. KEY HIGHLIGHTS
   - Top 5 ESG achievements
   - Major milestones reached

3. PERFORMANCE SNAPSHOT
   - Environmental metrics summary
   - Social metrics summary
   - Governance metrics summary

4. CHALLENGES AND OPPORTUNITIES
   - Key challenges faced
   - Opportunities identified

5. STRATEGIC PRIORITIES
   - Near-term priorities
   - Long-term commitments

6. CONCLUSION
   - Overall ESG performance assessment
   - Forward-looking statement

Keep it concise (2-3 pages) and focus on high-level insights.
"""


# Chart Generation Instructions
CHART_INSTRUCTIONS = """
When generating reports with charts, suggest appropriate visualizations for:

1. EMISSIONS DATA
   - Bar chart comparing Scope 1, 2, and 3 emissions
   - Line chart showing emissions trends over time
   - Pie chart for emissions breakdown by source

2. ENERGY AND WATER
   - Stacked bar chart for energy consumption by source
   - Progress bar for renewable energy percentage
   - Water consumption vs reclamation comparison

3. SOCIAL METRICS
   - Gender diversity ratio visualization
   - Employee turnover trend line
   - Safety performance (LTIR) over time

4. GOVERNANCE METRICS
   - Board composition pie chart
   - Independence metrics bar chart

5. TARGETS VS ACTUALS
   - Comparison charts for all key metrics
   - Progress towards 2030/2050 targets

Provide specific data points and labels for each chart.
"""


# Report type mapping
REPORT_PROMPTS = {
    "comprehensive": COMPREHENSIVE_REPORT_PROMPT,
    "environmental": ENVIRONMENTAL_REPORT_PROMPT,
    "social": SOCIAL_REPORT_PROMPT,
    "governance": GOVERNANCE_REPORT_PROMPT,
    "compliance": COMPLIANCE_REPORT_PROMPT,
    "executive": EXECUTIVE_SUMMARY_PROMPT,
}


def get_report_prompt(report_type: str, data: str) -> str:
    """
    Get the appropriate prompt for the report type
    
    Args:
        report_type: Type of report to generate
        data: ESG data to include in the prompt
        
    Returns:
        Formatted prompt string
    """
    prompt_template = REPORT_PROMPTS.get(report_type, COMPREHENSIVE_REPORT_PROMPT)
    return prompt_template.format(data=data)
