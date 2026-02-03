"""
Crisis Report Generator
Generates comprehensive PDF reports combining media coverage and social media sentiment analysis.
Perfect for executive briefings and stakeholder updates during crisis situations.
"""

import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import seaborn as sns
import io


class CrisisReportGenerator:
    """Generate comprehensive crisis reports combining media and social analysis."""
    
    def __init__(self, media_file, comments_file, crisis_name='Crisis Incident', crisis_date=None):
        """
        Initialize CrisisReportGenerator.
        
        Args:
            media_file: Path to media coverage CSV
            comments_file: Path to comments CSV
            crisis_name: Name of the crisis for report title
            crisis_date: Date of crisis onset (defaults to today)
        """
        self.crisis_name = crisis_name
        self.crisis_date = crisis_date or datetime.now().strftime('%Y-%m-%d')
        self.report_date = datetime.now().strftime('%B %d, %Y')
        
        # Load and preprocess data
        self.media_data = self._load_and_prep_media(media_file)
        self.comments_data = self._load_and_prep_comments(comments_file)
        
        # Calculate metrics
        self._calculate_metrics()
    
    def _load_and_prep_media(self, file_path):
        """Load and preprocess media data."""
        data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.sort_values('Date')
        return data
    
    def _load_and_prep_comments(self, file_path):
        """Load and preprocess comments data."""
        data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.sort_values('Date')
        return data
    
    def _calculate_metrics(self):
        """Calculate all metrics needed for the report."""
        # Media metrics
        self.total_mentions = len(self.media_data)
        self.media_sentiment = self.media_data['Sentiment'].value_counts()
        self.media_sources = self.media_data['Source'].nunique()
        self.media_platforms = self.media_data['Platform'].nunique()
        self.media_date_range = f"{self.media_data['Date'].min().strftime('%Y-%m-%d')} to {self.media_data['Date'].max().strftime('%Y-%m-%d')}"
        
        # Comments metrics
        self.total_comments = len(self.comments_data)
        self.comments_sentiment = self.comments_data['Sentiment'].value_counts()
        self.comments_platforms = self.comments_data['Platform'].nunique()
        self.comments_categories = self.comments_data['Category'].nunique()
        
        # Calculate risk level
        self._calculate_risk_level()
    
    def _calculate_risk_level(self):
        """Determine overall risk level based on sentiment and volume."""
        # Negative sentiment percentage
        total_sentiment = len(self.media_data) + len(self.comments_data)
        total_negative = (self.media_sentiment.get('Negative', 0) + 
                         self.comments_sentiment.get('Negative', 0))
        
        negative_pct = (total_negative / total_sentiment * 100) if total_sentiment > 0 else 0
        
        # Comment volume spike detection
        daily_comments = self.comments_data.groupby('Date').size()
        avg_daily = daily_comments.mean()
        max_daily = daily_comments.max()
        spike_factor = max_daily / avg_daily if avg_daily > 0 else 1
        
        # Determine risk level
        if negative_pct > 60 or spike_factor > 3:
            self.risk_level = "HIGH"
            self.risk_color = colors.red
        elif negative_pct > 40 or spike_factor > 2:
            self.risk_level = "MODERATE"
            self.risk_color = colors.orange
        else:
            self.risk_level = "LOW"
            self.risk_color = colors.green
    
    def _create_cover_page(self):
        """Create cover page content."""
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        elements = []
        elements.append(Spacer(1, 1.5*inch))
        elements.append(Paragraph(f"CRISIS COMMUNICATION", title_style))
        elements.append(Paragraph(f"SITUATION REPORT", title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(self.crisis_name, subtitle_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Key metrics box
        metrics_data = [
            ['METRIC', 'VALUE'],
            ['Total Media Mentions', str(self.total_mentions)],
            ['Total Comments/Posts', str(self.total_comments)],
            ['Risk Assessment', self.risk_level],
            ['Report Date', self.report_date],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Risk level highlight
        risk_style = ParagraphStyle(
            'Risk',
            parent=styles['Normal'],
            fontSize=14,
            textColor=self.risk_color,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        elements.append(Paragraph(f"Risk Level: {self.risk_level}", risk_style))
        
        return elements
    
    def _create_executive_summary(self):
        """Create executive summary page."""
        styles = getSampleStyleSheet()
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        elements = []
        elements.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Overview text
        negative_media = self.media_sentiment.get('Negative', 0)
        negative_comments = self.comments_sentiment.get('Negative', 0)
        
        overview = f"""
        This report provides a comprehensive analysis of media coverage and social media sentiment 
        regarding {self.crisis_name}. The incident began on {self.crisis_date}, and this report 
        was generated on {self.report_date}.
        <br/><br/>
        <b>Key Findings:</b><br/>
        • Media coverage spans {self.media_platforms} platforms across {self.media_sources} sources<br/>
        • {negative_media} negative media mentions out of {self.total_mentions} total mentions<br/>
        • Social media shows {negative_comments} negative comments out of {self.total_comments} total<br/>
        • Overall risk assessment: <b>{self.risk_level}</b><br/>
        """
        
        elements.append(Paragraph(overview, styles['BodyText']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Sentiment summary table
        elements.append(Paragraph("SENTIMENT BREAKDOWN", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        sentiment_data = [['Sentiment', 'Media Mentions', 'Comments', 'Total']]
        for sentiment in ['Positive', 'Neutral', 'Negative']:
            media_count = self.media_sentiment.get(sentiment, 0)
            comments_count = self.comments_sentiment.get(sentiment, 0)
            total = media_count + comments_count
            sentiment_data.append([sentiment, str(media_count), str(comments_count), str(total)])
        
        sentiment_table = Table(sentiment_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        sentiment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(sentiment_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Recommendation
        elements.append(Paragraph("RECOMMENDATION", heading_style))
        if self.risk_level == "HIGH":
            recommendation = "Immediate escalation to senior leadership and implementation of crisis response protocols recommended."
        elif self.risk_level == "MODERATE":
            recommendation = "Continue monitoring closely and consider proactive communications to address sentiment concerns."
        else:
            recommendation = "Maintain current communication strategy. Monitor for any sentiment changes."
        
        elements.append(Paragraph(recommendation, styles['BodyText']))
        
        return elements
    
    def _create_media_analysis_page(self):
        """Create detailed media analysis page."""
        styles = getSampleStyleSheet()
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        elements = []
        elements.append(Paragraph("MEDIA COVERAGE ANALYSIS", heading_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Overview stats
        overview = f"""
        <b>Coverage Period:</b> {self.media_date_range}<br/>
        <b>Total Mentions:</b> {self.total_mentions}<br/>
        <b>Platforms Covered:</b> {self.media_platforms}<br/>
        <b>Unique Sources:</b> {self.media_sources}<br/>
        """
        elements.append(Paragraph(overview, styles['BodyText']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Platform breakdown
        elements.append(Paragraph("Coverage by Platform", heading_style))
        platform_breakdown = self.media_data['Platform'].value_counts()
        
        platform_data = [['Platform', 'Mentions']]
        for platform, count in platform_breakdown.items():
            platform_data.append([platform, str(count)])
        
        platform_table = Table(platform_data, colWidths=[3*inch, 2*inch])
        platform_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(platform_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # Sentiment distribution
        elements.append(Paragraph("Sentiment Distribution", heading_style))
        sentiment_text = ""
        for sentiment, count in self.media_sentiment.items():
            pct = (count / self.total_mentions * 100) if self.total_mentions > 0 else 0
            sentiment_text += f"{sentiment}: {count} ({pct:.1f}%)<br/>"
        
        elements.append(Paragraph(sentiment_text, styles['BodyText']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Top sources
        elements.append(Paragraph("Top News Sources", heading_style))
        top_sources = self.media_data['Source'].value_counts().head(5)
        
        sources_data = [['Source', 'Mentions']]
        for source, count in top_sources.items():
            sources_data.append([source, str(count)])
        
        sources_table = Table(sources_data, colWidths=[3*inch, 2*inch])
        sources_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(sources_table)
        
        return elements
    
    def _create_social_analysis_page(self):
        """Create detailed social media analysis page."""
        styles = getSampleStyleSheet()
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        elements = []
        elements.append(Paragraph("SOCIAL MEDIA ANALYSIS", heading_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Overview stats
        daily_avg = self.total_comments / len(self.comments_data['Date'].unique()) if len(self.comments_data['Date'].unique()) > 0 else 0
        overview = f"""
        <b>Total Comments/Posts:</b> {self.total_comments}<br/>
        <b>Platforms Monitored:</b> {self.comments_platforms}<br/>
        <b>Comment Categories:</b> {self.comments_categories}<br/>
        <b>Average Daily Volume:</b> {daily_avg:.1f} comments/day<br/>
        """
        elements.append(Paragraph(overview, styles['BodyText']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Platform sentiment breakdown
        elements.append(Paragraph("Sentiment by Platform", heading_style))
        platform_sentiment = pd.crosstab(self.comments_data['Platform'], self.comments_data['Sentiment'])
        
        sentiment_by_platform = [['Platform', 'Positive', 'Neutral', 'Negative']]
        for platform in platform_sentiment.index:
            row = [platform]
            for sentiment in ['Positive', 'Neutral', 'Negative']:
                count = platform_sentiment.loc[platform, sentiment] if sentiment in platform_sentiment.columns else 0
                row.append(str(int(count)))
            sentiment_by_platform.append(row)
        
        platform_sentiment_table = Table(sentiment_by_platform, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        platform_sentiment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(platform_sentiment_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # Category breakdown
        elements.append(Paragraph("Comments by Category", heading_style))
        category_breakdown = self.comments_data['Category'].value_counts().head(5)
        
        category_data = [['Category', 'Count']]
        for category, count in category_breakdown.items():
            category_data.append([category, str(count)])
        
        category_table = Table(category_data, colWidths=[3*inch, 2*inch])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(category_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # Overall sentiment
        elements.append(Paragraph("Overall Sentiment Distribution", heading_style))
        sentiment_text = ""
        for sentiment, count in self.comments_sentiment.items():
            pct = (count / self.total_comments * 100) if self.total_comments > 0 else 0
            sentiment_text += f"{sentiment}: {count} ({pct:.1f}%)<br/>"
        
        elements.append(Paragraph(sentiment_text, styles['BodyText']))
        
        return elements
    
    def generate_pdf_report(self, output_path='crisis_report.pdf'):
        """
        Generate comprehensive PDF report.
        
        Args:
            output_path: Path to save the PDF
        """
        # Create PDF
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        elements = []
        
        # Page 1: Cover Page
        elements.extend(self._create_cover_page())
        elements.append(PageBreak())
        
        # Page 2: Executive Summary
        elements.extend(self._create_executive_summary())
        elements.append(PageBreak())
        
        # Page 3: Media Analysis
        elements.extend(self._create_media_analysis_page())
        elements.append(PageBreak())
        
        # Page 4: Social Media Analysis
        elements.extend(self._create_social_analysis_page())
        
        # Build PDF
        doc.build(elements)
        print(f"PDF Report saved to {output_path}")
    
    def generate_quick_summary(self):
        """
        Generate a quick text summary for email/Slack.
        
        Returns:
            str: Formatted summary text
        """
        summary = f"""
CRISIS COMMUNICATION REPORT - {self.crisis_name.upper()}
Generated: {self.report_date}
Risk Level: {self.risk_level}

📊 KEY METRICS
├─ Media Mentions: {self.total_mentions}
├─ Social Comments: {self.total_comments}
├─ Risk Assessment: {self.risk_level}
└─ Total Impact Points: {self.total_mentions + self.total_comments}

📺 MEDIA COVERAGE
├─ Platforms: {self.media_platforms}
├─ Sources: {self.media_sources}
├─ Negative Mentions: {self.media_sentiment.get('Negative', 0)}
└─ Coverage Period: {self.media_date_range}

💬 SOCIAL MEDIA
├─ Platforms: {self.comments_platforms}
├─ Categories: {self.comments_categories}
├─ Negative Comments: {self.comments_sentiment.get('Negative', 0)}
└─ Total Comments: {self.total_comments}

⚠️  RECOMMENDATION
"""
        
        if self.risk_level == "HIGH":
            summary += "Immediate escalation to senior leadership required.\nImplement full crisis response protocols."
        elif self.risk_level == "MODERATE":
            summary += "Continue close monitoring.\nConsider proactive stakeholder communications."
        else:
            summary += "Current strategy is effective.\nMaintain routine monitoring."
        
        return summary


# Example usage
if __name__ == "__main__":
    # Generate report
    report = CrisisReportGenerator(
        media_file='templates/media_coverage_template.csv',
        comments_file='templates/comments_template.csv',
        crisis_name='Data Security Incident'
    )
    
    # Generate PDF
    report.generate_pdf_report('crisis_report.pdf')
    
    # Print quick summary
    print(report.generate_quick_summary())