# Simple Working PDF Export for Mood Tracker
# Fixes all character encoding and font issues

import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

class SimplePDFExporter:
    """Simple, working PDF exporter without character encoding issues."""
    
    def __init__(self, df, data_file):
        self.df = df
        self.data_file = data_file
        self.mood_scale = {
            1: "Very Sad",
            2: "Sad", 
            3: "Neutral",
            4: "Happy",
            5: "Very Happy"
        }
    
    def clean_text(self, text):
        """Remove emojis and special characters for PDF compatibility."""
        if not text:
            return ""
        
        # Convert to string and remove non-ASCII characters
        text_str = str(text)
        cleaned = ''.join(char for char in text_str if ord(char) < 128)
        return cleaned.strip()
    
    def generate_charts_for_pdf(self):
        """Generate clean charts for PDF embedding."""
        if len(self.df) < 2:
            return {}
        
        chart_paths = {}
        
        try:
            # 1. Simple Trends Chart
            plt.figure(figsize=(10, 6))
            plt.style.use('default')  # Use default style
            
            sorted_df = self.df.sort_values('Date')
            plt.plot(sorted_df['Date'], sorted_df['Mood_Score'], 
                    marker='o', linewidth=2, markersize=6, color='blue')
            
            plt.title('Mood Trends Over Time', fontsize=14, fontweight='bold')
            plt.xlabel('Date')
            plt.ylabel('Mood Score') 
            plt.ylim(0.5, 5.5)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            trends_path = 'data/charts/simple_trends.png'
            plt.savefig(trends_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            chart_paths['trends'] = trends_path
            
            # 2. Simple Bar Chart for Distribution
            plt.figure(figsize=(8, 6))
            mood_counts = self.df['Mood_Score'].value_counts().sort_index()
            
            plt.bar(mood_counts.index, mood_counts.values, color='lightblue', edgecolor='blue')
            plt.title('Mood Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Mood Score')
            plt.ylabel('Frequency')
            plt.xticks([1, 2, 3, 4, 5], ['Very Sad', 'Sad', 'Neutral', 'Happy', 'Very Happy'])
            
            # Add value labels on bars
            for i, v in enumerate(mood_counts.values):
                plt.text(mood_counts.index[i], v + 0.1, str(v), ha='center', va='bottom')
            
            plt.tight_layout()
            
            dist_path = 'data/charts/simple_distribution.png'
            plt.savefig(dist_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            chart_paths['distribution'] = dist_path
            
            return chart_paths
            
        except Exception as e:
            print(f"Error generating charts: {e}")
            return {}
    
    def create_simple_pdf_report(self):
        """Create a simple, working PDF report."""
        if len(self.df) == 0:
            print("No data available for PDF report!")
            return None
        
        try:
            print("Generating simple PDF report...")
            
            # Generate charts
            chart_paths = self.generate_charts_for_pdf()
            
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 15, 'MOOD TRACKING REPORT', 0, 1, 'C')
            
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, datetime.now().strftime('Generated on %B %d, %Y'), 0, 1, 'C')
            pdf.ln(10)
            
            # Basic Statistics
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, 'SUMMARY STATISTICS', 0, 1)
            
            pdf.set_font('Arial', '', 11)
            total_entries = len(self.df)
            avg_mood = self.df['Mood_Score'].mean()
            date_range = (self.df['Date'].max() - self.df['Date'].min()).days + 1
            
            stats = [
                f"Total Entries: {total_entries}",
                f"Average Mood: {avg_mood:.2f}/5.0", 
                f"Tracking Period: {date_range} days",
                f"Date Range: {self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}"
            ]
            
            for stat in stats:
                pdf.cell(0, 8, stat, 0, 1)
            
            pdf.ln(10)
            
            # Mood Distribution
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'MOOD BREAKDOWN', 0, 1)
            pdf.set_font('Arial', '', 10)
            
            mood_counts = self.df['Mood_Score'].value_counts().sort_index()
            for mood_score, count in mood_counts.items():
                mood_label = self.mood_scale[mood_score]
                percentage = (count / total_entries) * 100
                pdf.cell(0, 6, f"{mood_label}: {count} times ({percentage:.1f}%)", 0, 1)
            
            # Add charts if available
            if chart_paths:
                pdf.add_page()
                pdf.set_font('Arial', 'B', 14)
                pdf.cell(0, 10, 'MOOD VISUALIZATIONS', 0, 1, 'C')
                pdf.ln(10)
                
                # Add trends chart
                if 'trends' in chart_paths:
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(0, 8, 'Mood Trends Over Time', 0, 1)
                    pdf.image(chart_paths['trends'], x=10, y=pdf.get_y(), w=190)
                    pdf.ln(100)
                
                # Add distribution chart  
                if 'distribution' in chart_paths:
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(0, 8, 'Mood Distribution', 0, 1)
                    pdf.image(chart_paths['distribution'], x=20, y=pdf.get_y(), w=170)
            
            # Recent entries (simplified)
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, 'RECENT ENTRIES', 0, 1, 'C')
            pdf.ln(5)
            
            recent_df = self.df.sort_values('Date', ascending=False).head(8)
            
            pdf.set_font('Arial', '', 10)
            for _, row in recent_df.iterrows():
                date_str = row['Date'].strftime('%Y-%m-%d')
                mood_str = f"Mood: {row['Mood_Score']}/5 ({self.mood_scale[row['Mood_Score']]})"
                
                pdf.cell(0, 6, f"Date: {date_str}", 0, 1)
                pdf.cell(0, 6, mood_str, 0, 1)
                
                # Add note if available (cleaned)
                if pd.notna(row['Note']) and str(row['Note']).strip():
                    note_text = self.clean_text(str(row['Note']))
                    if len(note_text) > 80:
                        note_text = note_text[:80] + "..."
                    pdf.cell(0, 6, f"Note: {note_text}", 0, 1)
                
                pdf.ln(3)
            
            # Save PDF
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_filename = f'data/reports/simple_mood_report_{timestamp}.pdf'
            pdf.output(pdf_filename)
            
            print(f"PDF report created successfully!")
            print(f"Saved as: {pdf_filename}")
            
            return pdf_filename
            
        except Exception as e:
            print(f"Error creating PDF: {e}")
            return None

# Integration function to add to your existing code
def export_simple_pdf(mood_tracker_instance):
    """
    Simple function to export PDF from any of your mood tracker versions.
    
    Usage:
    pdf_exporter = SimplePDFExporter(self.df, self.data_file)
    pdf_exporter.create_simple_pdf_report()
    """
    if len(mood_tracker_instance.df) == 0:
        print("No mood data available for PDF export!")
        print("Generate sample data first!")
        return
    
    exporter = SimplePDFExporter(mood_tracker_instance.df, mood_tracker_instance.data_file)
    return exporter.create_simple_pdf_report()

# Test function
def test_pdf_export():
    """Test function to verify PDF export works."""
    import pandas as pd
    from datetime import datetime, timedelta
    import random
    
    # Create sample data
    sample_data = []
    base_date = datetime.now() - timedelta(days=10)
    
    for i in range(10):
        date = base_date + timedelta(days=i)
        mood_score = random.randint(2, 5)
        mood_label = {1: "Very Sad", 2: "Sad", 3: "Neutral", 4: "Happy", 5: "Very Happy"}[mood_score]
        note = f"Sample note for day {i+1}"
        
        sample_data.append({
            'Date': date,
            'Mood_Score': mood_score,
            'Mood_Label': mood_label,
            'Note': note,
            'Sentiment_Score': 0.1,
            'Sentiment_Label': 'Positive'
        })
    
    df = pd.DataFrame(sample_data)
    
    # Test PDF export
    exporter = SimplePDFExporter(df, 'test_data.csv')
    return exporter.create_simple_pdf_report()

if __name__ == "__main__":
    test_pdf_export()