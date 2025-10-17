"""
Crisis Report Generator
Generates comprehensive daily crisis reports combining media coverage and sentiment analysis.
Perfect for executive morning briefings.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import os

from media_tracker import MediaTracker
from sentiment_analyzer import SentimentAnalyzer


class CrisisReportGenerator:
    def __init__(self, media_file, comments_file, crisis_name="Crisis"):
        """
        Initialize Crisis Report Generator.
        
        Args:
            media_file: Path to media coverage CSV/Excel
            comments_file: Path to comments CSV/Excel
            crisis_name: Name of the crisis for report title
        """
        self.crisis_name = crisis_name
        self.media_tracker = MediaTracker(media_file)
        self.sentiment_analyzer = SentimentAnalyzer(comments_file)
        self.report_date = datetime.now().strftime('%Y-%m-%d')
        
    def generate_executive_summary(self):
        """Generate executive summary combining all data."""
        media_summary = self.media_tracker.generate_summary_stats()
        comment_summary = self.sentiment_analyzer.generate_summary_stats()
        
        # Calculate key metrics
        total_reach = media_summary['Total Mentions'] + comment_summary['Total Comments']
        
        # Media sentiment
        media_negative_pct = media_summary['Sentiment'].get('Negative', 0)
        
        # Comment sentiment
        comment_negative_pct = comment_summary['Sentiment'].get('Negative', 0)
        
        # Overall sentiment (weighted by volume)
        overall_negative = (
            (media_summary['Total Mentions'] * media_negative_pct / 100) +
            (comment_summary['Total Comments'] * comment_negative_pct / 100)
        ) / total_reach * 100
        
        summary = {
            'Report Date': self.report_date,
            'Crisis Name': self.crisis_name,
            'Total Media Mentions': media_summary['Total Mentions'],
            'Total Social Comments': comment_summary['Total Comments'],
            'Total Reach': total_reach,
            'Media Sentiment (Negative %)': round(media_negative_pct, 1),
            'Social Sentiment (Negative %)': round(comment_negative_pct, 1),
            'Overall Negative Sentiment': round(overall_negative, 1),
            'Platforms Monitored': media_summary['Platforms'],
            'Unique Media Sources': media_summary['Unique Sources'],
            'Volume Spikes Detected': comment_summary['Volume Spikes Detected']
        }
        
        return summary
    
    def _create_cover_page(self, ax, summary):
        """Create report cover page."""
        ax.axis('off')
        
        # Title
        title_text = f"{self.crisis_name.upper()}\nDAILY CRISIS REPORT"
        ax.text(0.5, 0.75, title_text, ha='center', va='center', 
               fontsize=24, fontweight='bold', transform=ax.transAxes)
        
        # Date
        ax.text(0.5, 0.65, f"Report Date: {summary['Report Date']}", 
               ha='center', va='center', fontsize=14, transform=ax.transAxes)
        
        # Key metrics box
        metrics_text = f"""
        KEY METRICS
        
        Total Media Mentions: {summary['Total Media Mentions']}
        Total Social Comments: {summary['Total Social Comments']}
        
        Overall Negative Sentiment: {summary['Overall Negative Sentiment']}%
        
        Media Sources: {summary['Unique Media Sources']}
        Platforms Monitored: {summary['Platforms Monitored']}
        Volume Spikes: {summary['Volume Spikes Detected']}
        """
        
        ax.text(0.5, 0.35, metrics_text, ha='center', va='center',
               fontsize=12, fontfamily='monospace', transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
        
        # Footer
        ax.text(0.5, 0.05, "CONFIDENTIAL - For Internal Use Only",
               ha='center', va='center', fontsize=10, style='italic',
               transform=ax.transAxes, color='gray')
    
    def _create_summary_page(self, ax, summary):
        """Create executive summary page."""
        ax.axis('off')
        
        ax.text(0.5, 0.95, "EXECUTIVE SUMMARY", ha='center', va='top',
               fontsize=18, fontweight='bold', transform=ax.transAxes)
        
        # Status assessment
        negative_pct = summary['Overall Negative Sentiment']
        if negative_pct < 30:
            status = "LOW RISK"
            status_color = 'green'
        elif negative_pct < 60:
            status = "MODERATE RISK"
            status_color = 'orange'
        else:
            status = "HIGH RISK"
            status_color = 'red'
        
        ax.text(0.5, 0.85, f"Current Status: {status}", ha='center', va='top',
               fontsize=16, fontweight='bold', color=status_color, transform=ax.transAxes)
        
        # Key findings
        findings_text = f"""
        SITUATION OVERVIEW
        
        • Media Coverage: {summary['Total Media Mentions']} mentions across 
          {summary['Unique Media Sources']} sources
        
        • Social Media: {summary['Total Social Comments']} comments with 
          {summary['Volume Spikes Detected']} volume spikes detected
        
        • Sentiment Analysis:
          - Media: {summary['Media Sentiment (Negative %)']}% negative
          - Social: {summary['Social Sentiment (Negative %)']}% negative
          - Overall: {summary['Overall Negative Sentiment']}% negative
        
        RECOMMENDED ACTIONS
        
        • Continue monitoring all platforms for emerging narratives
        • Prepare response to key negative themes
        • Brief spokespersons on common questions
        • Schedule next update for [TIME]
        """
        
        ax.text(0.1, 0.70, findings_text, ha='left', va='top',
               fontsize=11, transform=ax.transAxes, wrap=True)
    
    def generate_pdf_report(self, output_path=None):
        """Generate comprehensive PDF report for executive briefing."""
        if output_path is None:
            output_path = f"crisis_report_{self.report_date}.pdf"
        
        summary = self.generate_executive_summary()
        
        with PdfPages(output_path) as pdf:
            # Page 1: Cover
            fig = plt.figure(figsize=(11, 8.5))
            ax = fig.add_subplot(111)
            self._create_cover_page(ax, summary)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Page 2: Executive Summary
            fig = plt.figure(figsize=(11, 8.5))
            ax = fig.add_subplot(111)
            self._create_summary_page(ax, summary)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Page 3: Media Coverage Analysis
            fig = plt.figure(figsize=(11, 8.5))
            fig.suptitle('MEDIA COVERAGE ANALYSIS', fontsize=16, fontweight='bold', y=0.98)
            
            ax1 = plt.subplot(2, 2, 1)
            self.media_tracker.plot_daily_coverage(ax1)
            
            ax2 = plt.subplot(2, 2, 2)
            self.media_tracker.plot_platform_distribution(ax2)
            
            ax3 = plt.subplot(2, 2, 3)
            self.media_tracker.plot_sentiment_pie(ax3)
            
            ax4 = plt.subplot(2, 2, 4)
            ax4.axis('off')
            media_sum = self.media_tracker.generate_summary_stats()
            stats_text = f"""
            Media Coverage Stats
            
            Total: {media_sum['Total Mentions']}
            Sources: {media_sum['Unique Sources']}
            Platforms: {media_sum['Platforms']}
            
            Sentiment:
            """
            for sent, pct in media_sum['Sentiment'].items():
                stats_text += f"\n  {sent}: {pct}%"
            
            ax4.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
                    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
            
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Page 4: Social Media Analysis
            fig = plt.figure(figsize=(11, 8.5))
            fig.suptitle('SOCIAL MEDIA COMMENT ANALYSIS', fontsize=16, fontweight='bold', y=0.98)
            
            ax1 = plt.subplot(2, 2, 1)
            self.sentiment_analyzer.plot_daily_volume(ax1)
            
            ax2 = plt.subplot(2, 2, 2)
            self.sentiment_analyzer.plot_category_distribution(ax2)
            
            ax3 = plt.subplot(2, 2, 3)
            self.sentiment_analyzer.plot_sentiment_heatmap(ax3)
            
            ax4 = plt.subplot(2, 2, 4)
            ax4.axis('off')
            comment_sum = self.sentiment_analyzer.generate_summary_stats()
            stats_text = f"""
            Comment Stats
            
            Total: {comment_sum['Total Comments']}
            Avg Daily: {comment_sum['Avg Daily Comments']}
            Spikes: {comment_sum['Volume Spikes Detected']}
            
            Sentiment:
            """
            for sent, pct in comment_sum['Sentiment'].items():
                stats_text += f"\n  {sent}: {pct}%"
            
            ax4.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
                    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
            
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Metadata
            d = pdf.infodict()
            d['Title'] = f'{self.crisis_name} - Daily Crisis Report'
            d['Author'] = 'Crisis Communication Team'
            d['Subject'] = 'Crisis Communication Analysis'
            d['Keywords'] =