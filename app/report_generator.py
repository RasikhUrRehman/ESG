"""
Report generation using Grok AI and document formatting
"""
import os
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from openai import OpenAI

# Document generation libraries
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from .config import settings
from .prompts import get_report_prompt, SYSTEM_PROMPT, CHART_INSTRUCTIONS

logger = logging.getLogger(__name__)


class GrokAPIClient:
    """Client for interacting with Grok AI API using OpenAI-compatible endpoint"""
    
    def __init__(self):
        self.api_key = settings.GROK_API_KEY
        self.base_url = settings.GROK_API_BASE
        self.model = settings.GROK_MODEL
        
        # Initialize OpenAI client with xAI Grok endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        
    async def generate_content(
        self, 
        prompt: str, 
        system_prompt: str = SYSTEM_PROMPT,
        max_tokens: int = 4000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate content using Grok AI
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            max_tokens: Maximum tokens in response
            temperature: Controls randomness (0.0-2.0)
            
        Returns:
            Generated content as string
            
        Raises:
            Exception: If API request fails
        """
        try:
            # Run the synchronous OpenAI client in a thread pool to avoid blocking
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            content = response.choices[0].message.content
            
            logger.info("Successfully generated content using Grok AI")
            return content
            
        except Exception as e:
            logger.error(f"Error generating content with Grok AI: {e}")
            
            # Enhanced error handling
            error_msg = str(e)
            if "401" in error_msg:
                logger.error("Invalid or expired API key")
                raise Exception("Invalid or expired Grok API key")
            elif "429" in error_msg:
                logger.error("Rate limit exceeded")
                raise Exception("Rate limit exceeded. Please try again later.")
            elif "404" in error_msg and "model" in error_msg.lower():
                logger.error(f"Model '{self.model}' not found")
                raise Exception(f"Model '{self.model}' not found. Check available models.")
            else:
                raise


class ChartGenerator:
    """Generate charts for ESG reports"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        sns.set_style("whitegrid")
        
    def create_emissions_chart(self, data: List[Dict[str, Any]], filename: str) -> Path:
        """Create emissions comparison chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract emissions data from the ESG data
        emissions = {}
        for row in data:
            # Look for emission-related fields
            for key, value in row.items():
                if any(term in str(key).lower() for term in ['scope', 'emission', 'ghg', 'co2']):
                    field_name = row.get('Field (EN)', row.get('field', key))
                    current_value = row.get('Current', row.get('current', row.get('Response / الإدخال', '')))
                    
                    # Try to convert to numeric
                    try:
                        if current_value and str(current_value).strip() and str(current_value) != 'nan':
                            numeric_value = float(str(current_value).replace(',', ''))
                            emissions[field_name] = numeric_value
                    except (ValueError, TypeError):
                        continue
        
        if emissions:
            labels = list(emissions.keys())
            values = list(emissions.values())
            
            colors_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            bar_colors = colors_list[:len(labels)]
            
            ax.bar(labels, values, color=bar_colors)
            ax.set_ylabel('Emissions (tCO₂e)', fontsize=12)
            ax.set_title('Greenhouse Gas Emissions', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
        else:
            # Create placeholder chart if no data
            ax.text(0.5, 0.5, 'No emissions data available', 
                   ha='center', va='center', fontsize=14)
            ax.set_title('Greenhouse Gas Emissions', fontsize=14, fontweight='bold')
        
        chart_path = self.output_dir / filename
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def create_diversity_chart(self, data: List[Dict[str, Any]], filename: str) -> Path:
        """Create diversity metrics chart"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Extract diversity data
        diversity_data = {}
        for row in data:
            for key, value in row.items():
                if any(term in str(key).lower() for term in ['diversity', 'gender', 'female', 'male', 'employee']):
                    field_name = row.get('Field (EN)', row.get('field', key))
                    current_value = row.get('Current', row.get('current', row.get('Response / الإدخال', '')))
                    
                    try:
                        if current_value and str(current_value).strip() and str(current_value) != 'nan':
                            numeric_value = float(str(current_value).replace(',', '').replace('%', ''))
                            diversity_data[field_name] = numeric_value
                    except (ValueError, TypeError):
                        continue
        
        if diversity_data and len(diversity_data) > 0:
            labels = list(diversity_data.keys())
            sizes = list(diversity_data.values())
            
            colors_list = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
            pie_colors = colors_list[:len(labels)]
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=pie_colors)
            ax.set_title('Diversity Metrics', fontsize=14, fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'No diversity data available', 
                   ha='center', va='center', fontsize=14)
            ax.set_title('Diversity Metrics', fontsize=14, fontweight='bold')
        
        chart_path = self.output_dir / filename
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def create_trend_chart(self, data: List[Dict[str, Any]], metric: str, filename: str) -> Path:
        """Create trend line chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract trend data - previous year, current, target
        trends = []
        labels = []
        
        for row in data:
            field_name = row.get('Field (EN)', row.get('field', ''))
            
            if metric.lower() in str(field_name).lower():
                prev_year = row.get('Prev Year', row.get('prev_year', row.get('Prev Year / العام السابق', '')))
                current = row.get('Current', row.get('current', row.get('Current / العام الحالي', '')))
                target = row.get('Target', row.get('target', row.get('Target / الهدف', '')))
                
                try:
                    values = []
                    periods = []
                    
                    if prev_year and str(prev_year).strip() and str(prev_year) != 'nan':
                        values.append(float(str(prev_year).replace(',', '')))
                        periods.append('Previous Year')
                    
                    if current and str(current).strip() and str(current) != 'nan':
                        values.append(float(str(current).replace(',', '')))
                        periods.append('Current')
                    
                    if target and str(target).strip() and str(target) != 'nan':
                        values.append(float(str(target).replace(',', '')))
                        periods.append('Target')
                    
                    if values:
                        ax.plot(periods, values, marker='o', linewidth=2, label=field_name)
                        trends.append(field_name)
                except (ValueError, TypeError):
                    continue
        
        if trends:
            ax.set_ylabel('Value', fontsize=12)
            ax.set_title(f'{metric} Trend Analysis', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(loc='best', fontsize=9)
            plt.xticks(rotation=0)
        else:
            ax.text(0.5, 0.5, f'No trend data available for {metric}', 
                   ha='center', va='center', fontsize=14)
            ax.set_title(f'{metric} Trend Analysis', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        chart_path = self.output_dir / filename
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path


class PDFReportGenerator:
    """Generate PDF reports using ReportLab"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate(
        self, 
        content: str, 
        output_path: Path,
        title: str = "ESG Report",
        charts: List[Path] = None
    ) -> Path:
        """
        Generate PDF report
        
        Args:
            content: Report content (markdown or plain text)
            output_path: Path to save PDF
            title: Report title
            charts: List of chart image paths to include
            
        Returns:
            Path to generated PDF
        """
        doc = SimpleDocTemplate(str(output_path), pagesize=A4)
        story = []
        
        # Title page
        title_para = Paragraph(title, self.styles['CustomTitle'])
        story.append(title_para)
        story.append(Spacer(1, 0.3 * inch))
        
        date_para = Paragraph(
            f"Generated on: {datetime.now().strftime('%B %d, %Y')}",
            self.styles['Normal']
        )
        story.append(date_para)
        story.append(PageBreak())
        
        # Process content
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            if not line:
                story.append(Spacer(1, 0.1 * inch))
                continue
            
            # Handle markdown headers
            if line.startswith('# '):
                para = Paragraph(line[2:], self.styles['CustomTitle'])
                story.append(para)
            elif line.startswith('## '):
                para = Paragraph(line[3:], self.styles['CustomHeading'])
                story.append(para)
            elif line.startswith('### '):
                para = Paragraph(line[4:], self.styles['Heading3'])
                story.append(para)
            else:
                para = Paragraph(line, self.styles['Normal'])
                story.append(para)
        
        # Add charts if provided
        if charts:
            story.append(PageBreak())
            story.append(Paragraph("Charts and Visualizations", self.styles['CustomHeading']))
            
            for chart_path in charts:
                if chart_path.exists():
                    try:
                        img = Image(str(chart_path), width=6*inch, height=4*inch)
                        story.append(img)
                        story.append(Spacer(1, 0.2 * inch))
                    except Exception as e:
                        logger.error(f"Error adding chart {chart_path}: {e}")
        
        # Build PDF
        doc.build(story)
        logger.info(f"PDF report generated: {output_path}")
        
        return output_path


class WordReportGenerator:
    """Generate Word documents using python-docx"""
    
    def generate(
        self,
        content: str,
        output_path: Path,
        title: str = "ESG Report",
        charts: List[Path] = None
    ) -> Path:
        """
        Generate Word report
        
        Args:
            content: Report content (markdown or plain text)
            output_path: Path to save DOCX
            title: Report title
            charts: List of chart image paths to include
            
        Returns:
            Path to generated DOCX
        """
        doc = Document()
        
        # Add title
        title_para = doc.add_heading(title, level=0)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add date
        date_para = doc.add_paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}")
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_page_break()
        
        # Process content
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            if not line:
                doc.add_paragraph()
                continue
            
            # Handle markdown headers
            if line.startswith('# '):
                doc.add_heading(line[2:], level=1)
            elif line.startswith('## '):
                doc.add_heading(line[3:], level=2)
            elif line.startswith('### '):
                doc.add_heading(line[4:], level=3)
            elif line.startswith('- ') or line.startswith('* '):
                doc.add_paragraph(line[2:], style='List Bullet')
            else:
                doc.add_paragraph(line)
        
        # Add charts if provided
        if charts:
            doc.add_page_break()
            doc.add_heading("Charts and Visualizations", level=1)
            
            for chart_path in charts:
                if chart_path.exists():
                    try:
                        doc.add_picture(str(chart_path), width=Inches(6))
                        doc.add_paragraph()
                    except Exception as e:
                        logger.error(f"Error adding chart {chart_path}: {e}")
        
        # Save document
        doc.save(str(output_path))
        logger.info(f"Word report generated: {output_path}")
        
        return output_path


class ReportGenerator:
    """Main report generator orchestrator"""
    
    def __init__(self):
        self.grok_client = GrokAPIClient()
        self.pdf_generator = PDFReportGenerator()
        self.word_generator = WordReportGenerator()
        
    async def generate_report(
        self,
        data: List[Dict[str, Any]],
        report_type: str,
        output_format: str,
        output_filename: str,
        include_charts: bool = True
    ) -> Path:
        """
        Generate complete ESG report
        
        Args:
            data: Extracted ESG data
            report_type: Type of report (comprehensive, environmental, etc.)
            output_format: Format (pdf or docx)
            output_filename: Output filename without extension
            include_charts: Whether to include charts
            
        Returns:
            Path to generated report
        """
        from .column_matcher import format_data_for_report
        
        # Format data for AI
        formatted_data = format_data_for_report(data)
        
        # Get appropriate prompt
        prompt = get_report_prompt(report_type, formatted_data)
        
        if include_charts:
            prompt += f"\n\n{CHART_INSTRUCTIONS}"
        
        # Generate content using Grok AI
        logger.info(f"Generating {report_type} report content using Grok AI...")
        content = await self.grok_client.generate_content(prompt)
        
        # Generate charts if requested
        charts = []
        if include_charts:
            chart_dir = settings.REPORTS_DIR / "charts"
            chart_generator = ChartGenerator(chart_dir)
            
            try:
                logger.info("Generating charts...")
                # Create emissions chart
                emissions_chart = chart_generator.create_emissions_chart(data, f"emissions_{output_filename}.png")
                if emissions_chart.exists():
                    charts.append(emissions_chart)
                
                # Create diversity chart
                diversity_chart = chart_generator.create_diversity_chart(data, f"diversity_{output_filename}.png")
                if diversity_chart.exists():
                    charts.append(diversity_chart)
                
                # Create trend chart for energy consumption
                trend_chart = chart_generator.create_trend_chart(data, "Energy", f"trend_{output_filename}.png")
                if trend_chart.exists():
                    charts.append(trend_chart)
                
                logger.info(f"Generated {len(charts)} charts successfully")
            except Exception as e:
                logger.error(f"Error generating charts: {e}")
        
        # Generate document
        output_path = settings.REPORTS_DIR / f"{output_filename}.{output_format}"
        
        if output_format == "pdf":
            result_path = self.pdf_generator.generate(
                content,
                output_path,
                title=f"{report_type.title()} ESG Report",
                charts=charts
            )
        elif output_format == "docx":
            result_path = self.word_generator.generate(
                content,
                output_path,
                title=f"{report_type.title()} ESG Report",
                charts=charts
            )
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        return result_path
