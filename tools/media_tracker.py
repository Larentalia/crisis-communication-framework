"""
Media Coverage Tracker
Analyzes media mentions during crisis situations and generates visual reports.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from collections import Counter

class MediaTracker:
    def __init__(self, data_file):
        """
        Initialize MediaTracker with data file.
        
        Args:
            data_file: Path to CSV/Excel file with media coverage data
        """
        self.data = self._load_data(data_file)
        self._preprocess()
        
    def _load_data(self, file_path):
        """Load data from CSV or Excel file."""
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")
    
    def _preprocess(self):
        """Preprocess data: convert dates, clean text."""
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data = self.data.sort_values('Date')
        
    def get_daily_summary(self):
        """Generate daily coverage summary."""
        daily = self.data.groupby('Date').agg({
            'Source': 'count',
            'Sentiment': lambda x: x.value_counts().to_dict()
        }).rename(columns={'Source': 'Total_Mentions'})
        
        return daily
    
    def get_platform_breakdown(self):
        """Get breakdown by platform."""
        platform_counts = self.data['Platform'].value_counts()
        return platform_counts
    
    def get_source_breakdown(self):
        """Get breakdown by news source."""
        source_counts = self.data['Source'].value_counts()
        return source_counts.head(10)  # Top 10 sources
    
    def get_sentiment_distribution(self):
        """Calculate overall sentiment distribution."""
        sentiment_counts = self.data['Sentiment'].value_counts()
        sentiment_pct = (sentiment_counts / len(self.data) * 100).round(1)
        return sentiment_pct
    
    def plot_daily_coverage(self, ax=None):
        """Plot daily media coverage over time."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        daily = self.data.groupby('Date').size()
        
        ax.plot(daily.index, daily.values, marker='o', linewidth=2, markersize=6)
        ax.fill_between(daily.index, daily.values, alpha=0.3)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Number of Mentions', fontsize=12)
        ax.set_title('Daily Media Coverage', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        return ax
    
    def plot_platform_distribution(self, ax=None):
        """Plot coverage by platform."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        platform_counts = self.get_platform_breakdown()
        
        colors = sns.color_palette("husl", len(platform_counts))
        ax.barh(platform_counts.index, platform_counts.values, color=colors)
        ax.set_xlabel('Number of Mentions', fontsize=12)
        ax.set_title('Coverage by Platform', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        return ax
    
    def plot_sentiment_pie(self, ax=None):
        """Plot sentiment distribution as pie chart."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))
        
        sentiment_counts = self.data['Sentiment'].value_counts()
        colors = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
        sentiment_colors = [colors.get(s, '#3498db') for s in sentiment_counts.index]
        
        ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
               startangle=90, colors=sentiment_colors, textprops={'fontsize': 12})
        ax.set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
        
        return ax
    
    def generate_summary_stats(self):
        """Generate summary statistics."""
        total_mentions = len(self.data)
        date_range = f"{self.data['Date'].min().strftime('%Y-%m-%d')} to {self.data['Date'].max().strftime('%Y-%m-%d')}"
        platforms = self.data['Platform'].nunique()
        sources = self.data['Source'].nunique()
        
        sentiment_dist = self.get_sentiment_distribution()
        
        summary = {
            'Total Mentions': total_mentions,
            'Date Range': date_range,
            'Platforms': platforms,
            'Unique Sources': sources,
            'Sentiment': sentiment_dist.to_dict()
        }
        
        return summary
    
    def export_report(self, output_path='media_coverage_report.png'):
        """Generate and save comprehensive visual report."""
        fig = plt.figure(figsize=(16, 12))
        
        # Daily coverage
        ax1 = plt.subplot(2, 2, 1)
        self.plot_daily_coverage(ax1)
        
        # Platform distribution
        ax2 = plt.subplot(2, 2, 2)
        self.plot_platform_distribution(ax2)
        
        # Sentiment distribution
        ax3 = plt.subplot(2, 2, 3)
        self.plot_sentiment_pie(ax3)
        
        # Summary stats
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        summary = self.generate_summary_stats()
        
        summary_text = f"""
        MEDIA COVERAGE SUMMARY
        
        Total Mentions: {summary['Total Mentions']}
        Date Range: {summary['Date Range']}
        Platforms Monitored: {summary['Platforms']}
        Unique Sources: {summary['Unique Sources']}
        
        Sentiment Breakdown:
        """
        for sentiment, pct in summary['Sentiment'].items():
            summary_text += f"\n  • {sentiment}: {pct}%"
        
        ax4.text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center',
                fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Report saved to {output_path}")
        
        return fig


# Example usage
if __name__ == "__main__":
    # Example: Load data and generate report
    tracker = MediaTracker('templates/media_coverage_template.csv')
    
    # Print summary
    print("=== Media Coverage Summary ===")
    summary = tracker.generate_summary_stats()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Generate visual report
    tracker.export_report('media_coverage_report.png')