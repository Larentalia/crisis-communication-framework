"""
Sentiment Analyzer for Social Media Comments
Analyzes comments from social media profiles during crisis situations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime

class SentimentAnalyzer:
    def __init__(self, data_file):
        """
        Initialize SentimentAnalyzer with comments data.
        
        Args:
            data_file: Path to CSV/Excel file with comments data
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
        
    def get_daily_comment_volume(self):
        """Get daily comment volumes."""
        daily = self.data.groupby('Date').size()
        return daily
    
    def get_category_breakdown(self):
        """Get breakdown by comment category."""
        category_counts = self.data['Category'].value_counts()
        return category_counts
    
    def get_sentiment_by_category(self):
        """Get sentiment distribution by category."""
        sentiment_by_cat = pd.crosstab(
            self.data['Category'], 
            self.data['Sentiment'],
            normalize='index'
        ) * 100
        return sentiment_by_cat.round(1)
    
    def get_platform_sentiment(self):
        """Get sentiment distribution by platform."""
        platform_sentiment = pd.crosstab(
            self.data['Platform'],
            self.data['Sentiment'],
            normalize='index'
        ) * 100
        return platform_sentiment.round(1)
    
    def identify_spikes(self, threshold_multiplier=2.0):
        """
        Identify unusual spikes in comment volume.
        
        Args:
            threshold_multiplier: How many times above average to flag as spike
        """
        daily = self.get_daily_comment_volume()
        avg = daily.mean()
        spikes = daily[daily > (avg * threshold_multiplier)]
        return spikes
    
    def plot_daily_volume(self, ax=None):
        """Plot daily comment volume with sentiment breakdown."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        daily_sentiment = self.data.groupby(['Date', 'Sentiment']).size().unstack(fill_value=0)
        
        # Stacked area chart
        daily_sentiment.plot(kind='area', stacked=True, ax=ax, alpha=0.7,
                            color={'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'})
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Number of Comments', fontsize=12)
        ax.set_title('Daily Comment Volume by Sentiment', fontsize=14, fontweight='bold')
        ax.legend(title='Sentiment', loc='upper left')
        ax.grid(True, alpha=0.3)
        
        return ax
    
    def plot_category_distribution(self, ax=None):
        """Plot comment categories."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        category_counts = self.get_category_breakdown()
        
        colors = sns.color_palette("Set2", len(category_counts))
        ax.barh(category_counts.index, category_counts.values, color=colors)
        ax.set_xlabel('Number of Comments', fontsize=12)
        ax.set_title('Comments by Category', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, v in enumerate(category_counts.values):
            ax.text(v, i, f' {v}', va='center', fontsize=10)
        
        return ax
    
    def plot_sentiment_heatmap(self, ax=None):
        """Plot sentiment distribution across categories as heatmap."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
        
        sentiment_by_cat = self.get_sentiment_by_category()
        
        sns.heatmap(sentiment_by_cat, annot=True, fmt='.1f', cmap='RdYlGn', 
                   center=33.33, ax=ax, cbar_kws={'label': 'Percentage'})
        ax.set_title('Sentiment Distribution by Category (%)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Category', fontsize=12)
        ax.set_xlabel('Sentiment', fontsize=12)
        
        return ax
    
    def plot_platform_comparison(self, ax=None):
        """Compare sentiment across platforms."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        platform_sentiment = self.get_platform_sentiment()
        
        platform_sentiment.plot(kind='bar', ax=ax, 
                               color={'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'},
                               width=0.8)
        
        ax.set_xlabel('Platform', fontsize=12)
        ax.set_ylabel('Percentage', fontsize=12)
        ax.set_title('Sentiment Distribution by Platform', fontsize=14, fontweight='bold')
        ax.legend(title='Sentiment', loc='upper right')
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')
        
        return ax
    
    def generate_summary_stats(self):
        """Generate summary statistics."""
        total_comments = len(self.data)
        date_range = f"{self.data['Date'].min().strftime('%Y-%m-%d')} to {self.data['Date'].max().strftime('%Y-%m-%d')}"
        platforms = self.data['Platform'].nunique()
        categories = self.data['Category'].nunique()
        
        sentiment_dist = (self.data['Sentiment'].value_counts() / total_comments * 100).round(1)
        
        avg_daily = self.get_daily_comment_volume().mean()
        spikes = self.identify_spikes()
        
        summary = {
            'Total Comments': total_comments,
            'Date Range': date_range,
            'Platforms': platforms,
            'Categories': categories,
            'Avg Daily Comments': round(avg_daily, 1),
            'Volume Spikes Detected': len(spikes),
            'Sentiment': sentiment_dist.to_dict()
        }
        
        return summary
    
    def export_report(self, output_path='sentiment_analysis_report.png'):
        """Generate and save comprehensive visual report."""
        fig = plt.figure(figsize=(16, 12))
        
        # Daily volume
        ax1 = plt.subplot(2, 2, 1)
        self.plot_daily_volume(ax1)
        
        # Category distribution
        ax2 = plt.subplot(2, 2, 2)
        self.plot_category_distribution(ax2)
        
        # Sentiment heatmap
        ax3 = plt.subplot(2, 2, 3)
        self.plot_sentiment_heatmap(ax3)
        
        # Summary stats
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        summary = self.generate_summary_stats()
        
        summary_text = f"""
        COMMENT ANALYSIS SUMMARY
        
        Total Comments: {summary['Total Comments']}
        Date Range: {summary['Date Range']}
        Platforms: {summary['Platforms']}
        Categories: {summary['Categories']}
        Avg Daily Comments: {summary['Avg Daily Comments']}
        Volume Spikes: {summary['Volume Spikes Detected']}
        
        Overall Sentiment:
        """
        for sentiment, pct in summary['Sentiment'].items():
            summary_text += f"\n  • {sentiment}: {pct}%"
        
        ax4.text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center',
                fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Report saved to {output_path}")
        
        return fig


# Example usage
if __name__ == "__main__":
    # Example: Load data and generate report
    analyzer = SentimentAnalyzer('templates/comments_template.csv')
    
    # Print summary
    print("=== Comment Analysis Summary ===")
    summary = analyzer.generate_summary_stats()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Identify spikes
    spikes = analyzer.identify_spikes()
    if len(spikes) > 0:
        print("\n=== Volume Spikes Detected ===")
        for date, volume in spikes.items():
            print(f"{date.strftime('%Y-%m-%d')}: {volume} comments")
    
    # Generate visual report
    analyzer.export_report('sentiment_analysis_report.png')