"""
Prompts for different types of ESG reports using Grok AI
"""

# Base system prompt for ESG reporting
SYSTEM_PROMPT = """You are an expert ESG (Environmental, Social, and Governance) analyst and report writer. 
Your role is to generate comprehensive, professional, and data-driven ESG reports based on the provided data.
You should follow international standards like GRI, SASB, TCFD, and IFRS S1/S2 where applicable.
Always maintain a professional tone and ensure accuracy in data interpretation."""


# Comprehensive ESG Report Prompt
COMPREHENSIVE_REPORT_PROMPT = """
Generate a comprehensive ESG report based on the following data:

{data}

The report should include:

1. EXECUTIVE SUMMARY
   - Overview of ESG performance
   - Key highlights and achievements
   - Areas of concern or improvement needed

2. ENVIRONMENTAL PERFORMANCE
   - Greenhouse Gas Emissions (Scope 1, 2, and 3)
   - Energy consumption and renewable energy usage
   - Water management and conservation
   - Waste management and recycling
   - Climate-related investments and initiatives
   - Analysis of trends (comparison with previous year and targets)

3. SOCIAL PERFORMANCE
   - Employee diversity and inclusion metrics
   - Health and safety performance
   - Employee turnover and retention
   - Gender pay equity
   - Community investment and engagement
   - Human rights and non-discrimination policies

4. GOVERNANCE STRUCTURE
   - Board composition and independence
   - ESG oversight mechanisms
   - Executive compensation and ESG linkages
   - Risk management processes
   - Data privacy and whistleblowing mechanisms

5. STRATEGY AND TARGETS
   - ESG materiality assessment
   - Climate scenario analysis
   - Net Zero 2050 alignment
   - Specific targets and timelines
   - Progress towards goals

6. COMPLIANCE AND DISCLOSURE
   - Regulatory compliance status
   - Sustainability reporting frameworks used
   - External assurance and verification
   - SDG alignment

7. KEY PERFORMANCE INDICATORS (KPIs)
   - Summary table of all major metrics
   - Year-over-year comparisons
   - Progress towards targets

8. RECOMMENDATIONS
   - Strategic recommendations for improvement
   - Priority areas for action
   - Best practice suggestions

Format the report professionally with clear sections, subsections, and data tables where appropriate.
Use markdown formatting for structure.
"""


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
