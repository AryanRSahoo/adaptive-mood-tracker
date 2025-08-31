# Adaptive Emotion-Based Productivity Assistant - GUI Version
# Beautiful desktop application with modern UI design
# Portfolio-ready for university applications

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from textblob import TextBlob
import numpy as np
import random
from PIL import Image, ImageTk

class MoodTrackerGUI:
    """
    Modern GUI version of the Mood Tracker with beautiful interface.
    """
    
    def __init__(self):
        self.data_file = 'data/mood_data.csv'
        self.mood_scale = {
            1: "Very Sad 😢",
            2: "Sad 😞", 
            3: "Neutral 😐",
            4: "Happy 😊",
            5: "Very Happy 😄"
        }
        
        # Colors for modern UI
        self.colors = {
            'primary': '#4A90E2',
            'secondary': '#7ED321', 
            'danger': '#D0021B',
            'warning': '#F5A623',
            'dark': '#2C3E50',
            'light': '#ECF0F1',
            'white': '#FFFFFF',
            'gray': '#95A5A6'
        }
        
        # Setup data
        self.setup_data_directory()
        self.initialize_csv_file()
        self.load_data()
        
        # Create GUI
        self.create_gui()
        
    def setup_data_directory(self):
        """Create data directory if it doesn't exist."""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def initialize_csv_file(self):
        """Create CSV file with proper headers if it doesn't exist."""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
    
    def load_data(self):
        """Load existing data from CSV into pandas DataFrame."""
        try:
            if os.path.exists(self.data_file):
                self.df = pd.read_csv(self.data_file)
                if len(self.df) > 0:
                    self.df['Date'] = pd.to_datetime(self.df['Date'])
                else:
                    self.df = pd.DataFrame(columns=['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
            else:
                self.df = pd.DataFrame(columns=['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
        except Exception as e:
            self.df = pd.DataFrame(columns=['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
    
    def create_gui(self):
        """Create the main GUI interface."""
        self.root = tk.Tk()
        self.root.title("Adaptive Emotion-Based Productivity Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors['light'])
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Title.TLabel', 
                           font=('Helvetica', 24, 'bold'),
                           background=self.colors['light'],
                           foreground=self.colors['dark'])
        
        self.style.configure('Heading.TLabel',
                           font=('Helvetica', 16, 'bold'),
                           background=self.colors['light'],
                           foreground=self.colors['dark'])
        
        self.style.configure('Custom.TButton',
                           font=('Helvetica', 12, 'bold'),
                           padding=(20, 10))
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create header
        self.create_header()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Create tabs
        self.create_mood_log_tab()
        self.create_dashboard_tab()
        self.create_analytics_tab()
        self.create_recommendations_tab()
        
        # Update dashboard on startup
        self.update_dashboard()
        
    def create_header(self):
        """Create the header section."""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="🌟 Adaptive Emotion-Based Productivity Assistant",
                               style='Title.TLabel')
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                 text="AI-Powered Mood Tracking & Productivity Optimization",
                                 font=('Helvetica', 12),
                                 background=self.colors['light'],
                                 foreground=self.colors['gray'])
        subtitle_label.pack()
        
        # Stats bar
        stats_frame = ttk.Frame(header_frame)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_label = ttk.Label(stats_frame,
                                   text=f"Total Entries: {len(self.df)} | Current Streak: {self.calculate_streak()} days",
                                   font=('Helvetica', 10),
                                   background=self.colors['light'],
                                   foreground=self.colors['gray'])
        self.stats_label.pack()
    
    def calculate_streak(self):
        """Calculate current logging streak."""
        if len(self.df) == 0:
            return 0
        
        # Sort by date and check consecutive days
        sorted_df = self.df.sort_values('Date', ascending=False)
        streak = 0
        current_date = datetime.now().date()
        
        for _, row in sorted_df.iterrows():
            entry_date = row['Date'].date()
            if (current_date - entry_date).days == streak:
                streak += 1
                current_date = entry_date
            else:
                break
        
        return streak
    
    def create_mood_log_tab(self):
        """Create the mood logging tab."""
        self.mood_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.mood_tab, text="📝 Log Mood")
        
        # Main container
        container = ttk.Frame(self.mood_tab)
        container.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Today's date
        date_frame = ttk.Frame(container)
        date_frame.pack(fill=tk.X, pady=(0, 30))
        
        date_label = ttk.Label(date_frame,
                             text=f"Today: {datetime.now().strftime('%A, %B %d, %Y')}",
                             style='Heading.TLabel')
        date_label.pack()
        
        # Mood selection
        mood_frame = ttk.LabelFrame(container, text="How are you feeling today?", padding=20)
        mood_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.mood_var = tk.IntVar(value=3)
        
        # Create mood buttons in a grid
        mood_buttons_frame = ttk.Frame(mood_frame)
        mood_buttons_frame.pack()
        
        for score, label in self.mood_scale.items():
            btn = ttk.Radiobutton(mood_buttons_frame,
                                text=label,
                                variable=self.mood_var,
                                value=score,
                                command=self.on_mood_select)
            btn.grid(row=0, column=score-1, padx=10, pady=10, sticky='w')
        
        # Selected mood display
        self.mood_display = ttk.Label(mood_frame,
                                    text="Selected: Neutral 😐",
                                    font=('Helvetica', 14, 'bold'),
                                    background=self.colors['light'],
                                    foreground=self.colors['primary'])
        self.mood_display.pack(pady=(20, 0))
        
        # Note section
        note_frame = ttk.LabelFrame(container, text="Add a note (optional)", padding=20)
        note_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.note_text = scrolledtext.ScrolledText(note_frame, 
                                                 height=5,
                                                 font=('Helvetica', 11),
                                                 wrap=tk.WORD)
        self.note_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(container)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_btn = ttk.Button(button_frame,
                             text="💾 Save Mood Entry",
                             style='Custom.TButton',
                             command=self.save_mood_entry)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        generate_btn = ttk.Button(button_frame,
                                text="🧪 Generate Sample Data",
                                style='Custom.TButton',
                                command=self.generate_sample_data)
        generate_btn.pack(side=tk.LEFT)
        
        # Quick recommendation
        self.quick_rec_frame = ttk.LabelFrame(container, text="Quick Recommendation", padding=15)
        self.quick_rec_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.quick_rec_label = ttk.Label(self.quick_rec_frame,
                                       text="Select a mood to see personalized recommendations",
                                       font=('Helvetica', 11),
                                       background=self.colors['light'],
                                       wraplength=600)
        self.quick_rec_label.pack()
    
    def create_dashboard_tab(self):
        """Create the dashboard tab."""
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="📊 Dashboard")
        
        # Create scrollable frame
        canvas = tk.Canvas(self.dashboard_tab, bg=self.colors['light'])
        scrollbar = ttk.Scrollbar(self.dashboard_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.dashboard_frame = scrollable_frame
        
        # Recent entries section
        self.recent_frame = ttk.LabelFrame(self.dashboard_frame, text="Recent Mood Entries", padding=15)
        self.recent_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Statistics cards
        stats_container = ttk.Frame(self.dashboard_frame)
        stats_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Create statistics cards
        self.create_stat_cards(stats_container)
    
    def create_analytics_tab(self):
        """Create the analytics tab with charts."""
        self.analytics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analytics_tab, text="📈 Analytics")
        
        # Create notebook for different charts
        chart_notebook = ttk.Notebook(self.analytics_tab)
        chart_notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mood trends chart
        self.trends_frame = ttk.Frame(chart_notebook)
        chart_notebook.add(self.trends_frame, text="📈 Mood Trends")
        
        # Frequency chart
        self.frequency_frame = ttk.Frame(chart_notebook)
        chart_notebook.add(self.frequency_frame, text="🍕 Mood Distribution")
        
        # Weekday patterns
        self.weekday_frame = ttk.Frame(chart_notebook)
        chart_notebook.add(self.weekday_frame, text="📅 Weekday Patterns")
        
        # Create charts
        self.create_charts()
    
    def create_recommendations_tab(self):
        """Create the recommendations tab."""
        self.recommendations_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.recommendations_tab, text="💡 Recommendations")
        
        # Main container
        container = ttk.Frame(self.recommendations_tab)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Current mood status
        status_frame = ttk.LabelFrame(container, text="Current Status", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = ttk.Label(status_frame,
                                    text="No mood data available",
                                    font=('Helvetica', 12),
                                    background=self.colors['light'])
        self.status_label.pack()
        
        # Recommendations list
        rec_frame = ttk.LabelFrame(container, text="Personalized Recommendations", padding=15)
        rec_frame.pack(fill=tk.BOTH, expand=True)
        
        self.recommendations_text = scrolledtext.ScrolledText(rec_frame,
                                                            height=15,
                                                            font=('Helvetica', 11),
                                                            wrap=tk.WORD,
                                                            state=tk.DISABLED)
        self.recommendations_text.pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        refresh_btn = ttk.Button(container,
                               text="🔄 Refresh Recommendations",
                               style='Custom.TButton',
                               command=self.update_recommendations)
        refresh_btn.pack(pady=(20, 0))
    
    def create_stat_cards(self, parent):
        """Create statistics display cards."""
        # Average mood card
        avg_frame = ttk.LabelFrame(parent, text="Average Mood", padding=15)
        avg_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        if len(self.df) > 0:
            avg_mood = self.df['Mood_Score'].mean()
            avg_text = f"{avg_mood:.1f}"
            avg_emoji = self.get_mood_emoji(avg_mood)
        else:
            avg_text = "N/A"
            avg_emoji = "😐"
        
        ttk.Label(avg_frame, 
                 text=f"{avg_text} {avg_emoji}",
                 font=('Helvetica', 20, 'bold'),
                 background=self.colors['light']).pack()
        
        # Total entries card
        total_frame = ttk.LabelFrame(parent, text="Total Entries", padding=15)
        total_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        ttk.Label(total_frame,
                 text=str(len(self.df)),
                 font=('Helvetica', 20, 'bold'),
                 background=self.colors['light']).pack()
        
        # Current streak card
        streak_frame = ttk.LabelFrame(parent, text="Current Streak", padding=15)
        streak_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        ttk.Label(streak_frame,
                 text=f"{self.calculate_streak()} days",
                 font=('Helvetica', 20, 'bold'),
                 background=self.colors['light']).pack()
    
    def create_charts(self):
        """Create all the analytics charts."""
        if len(self.df) < 2:
            # Show message if not enough data
            for frame in [self.trends_frame, self.frequency_frame, self.weekday_frame]:
                ttk.Label(frame,
                         text="Generate sample data to view charts",
                         font=('Helvetica', 14),
                         background=self.colors['light']).pack(expand=True)
            return
        
        # Mood trends chart
        self.create_trends_chart()
        
        # Frequency chart
        self.create_frequency_chart()
        
        # Weekday patterns
        if len(self.df) >= 7:
            self.create_weekday_chart()
        else:
            ttk.Label(self.weekday_frame,
                     text="Need at least 7 entries for weekday analysis",
                     font=('Helvetica', 14),
                     background=self.colors['light']).pack(expand=True)
    
    def create_trends_chart(self):
        """Create mood trends line chart."""
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        
        sorted_df = self.df.sort_values('Date')
        dates = sorted_df['Date']
        moods = sorted_df['Mood_Score']
        
        ax.plot(dates, moods, marker='o', linewidth=3, markersize=8, 
                color=self.colors['primary'], markerfacecolor='white', 
                markeredgecolor=self.colors['primary'], markeredgewidth=2)
        ax.fill_between(dates, moods, alpha=0.3, color=self.colors['primary'])
        
        ax.set_title('Your Mood Trends Over Time', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Mood Score', fontsize=12)
        ax.set_ylim(0.5, 5.5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['Very Sad', 'Sad', 'Neutral', 'Happy', 'Very Happy'])
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        canvas = FigureCanvasTkAgg(fig, self.trends_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def create_frequency_chart(self):
        """Create mood frequency pie chart."""
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor('white')
        
        mood_counts = self.df['Mood_Label'].value_counts()
        colors = ['#FF6B6B', '#FFA07A', '#FFD700', '#98FB98', '#87CEEB']
        
        wedges, texts, autotexts = ax.pie(mood_counts.values, 
                                         labels=mood_counts.index, 
                                         autopct='%1.1f%%',
                                         colors=colors, 
                                         startangle=90,
                                         textprops={'fontsize': 12})
        
        ax.set_title('Your Mood Distribution', fontsize=16, fontweight='bold', pad=20)
        
        canvas = FigureCanvasTkAgg(fig, self.frequency_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def create_weekday_chart(self):
        """Create weekday patterns bar chart."""
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        
        df_copy = self.df.copy()
        df_copy['Weekday'] = df_copy['Date'].dt.day_name()
        weekday_moods = df_copy.groupby('Weekday')['Mood_Score'].mean()
        
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        available_days = [day for day in weekday_order if day in weekday_moods.index]
        weekday_moods = weekday_moods.reindex(available_days)
        
        colors_list = ['#FF6B6B', '#FFA07A', '#FFD700', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C']
        bars = ax.bar(weekday_moods.index, weekday_moods.values, 
                     color=colors_list[:len(weekday_moods)])
        
        ax.set_title('Average Mood by Day of Week', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Day of Week', fontsize=12)
        ax.set_ylabel('Average Mood Score', fontsize=12)
        ax.set_ylim(1, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['Very Sad', 'Sad', 'Neutral', 'Happy', 'Very Happy'])
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                   f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        canvas = FigureCanvasTkAgg(fig, self.weekday_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def on_mood_select(self):
        """Handle mood selection."""
        selected_mood = self.mood_var.get()
        mood_label = self.mood_scale[selected_mood]
        self.mood_display.config(text=f"Selected: {mood_label}")
        
        # Update quick recommendation
        recommendations = self.generate_mood_based_recommendations(selected_mood, selected_mood)
        if recommendations:
            self.quick_rec_label.config(text=f"💡 {recommendations[0]}")
    
    def save_mood_entry(self):
        """Save the mood entry."""
        mood_score = self.mood_var.get()
        mood_label = self.mood_scale[mood_score]
        note = self.note_text.get("1.0", tk.END).strip()
        
        # Analyze sentiment
        sentiment_score, sentiment_label = self.analyze_sentiment(note)
        
        # Check for duplicate (simplified - allow updates)
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        mood_entry = [current_date, mood_score, mood_label, note, sentiment_score, sentiment_label, current_timestamp]
        
        try:
            with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(mood_entry)
            
            messagebox.showinfo("Success", f"Mood entry saved!\n\nMood: {mood_label}\nSentiment: {sentiment_label}")
            
            # Clear form
            self.mood_var.set(3)
            self.note_text.delete("1.0", tk.END)
            self.mood_display.config(text="Selected: Neutral 😐")
            self.quick_rec_label.config(text="Select a mood to see personalized recommendations")
            
            # Reload data and update displays
            self.load_data()
            self.update_dashboard()
            self.update_recommendations()
            
            # Recreate charts
            for widget in self.trends_frame.winfo_children():
                widget.destroy()
            for widget in self.frequency_frame.winfo_children():
                widget.destroy()
            for widget in self.weekday_frame.winfo_children():
                widget.destroy()
            
            self.create_charts()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save mood entry: {str(e)}")
    
    def generate_sample_data(self):
        """Generate sample data for testing."""
        if messagebox.askyesno("Generate Sample Data", 
                              "This will replace existing data with 21 days of sample entries. Continue?"):
            
            # Clear existing data
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            self.initialize_csv_file()
            
            sample_notes = [
                "Had a great morning workout", "Stressful day at work", "Enjoyed time with friends",
                "Feeling overwhelmed with tasks", "Accomplished a lot today", "Weather was beautiful",
                "Didn't sleep well last night", "Great coffee this morning", "Challenging project at work",
                "Relaxing weekend vibes", "Productive meeting today", "Feeling a bit under the weather",
                "Excited about weekend plans", "Long day but satisfying", "Meditation helped my mood",
                "Traffic was terrible today", "Good news from family", "Deadline pressure building up",
                "Nice walk in the park", "Feeling grateful today"
            ]
            
            base_date = datetime.now() - timedelta(days=20)
            
            for i in range(21):
                date = base_date + timedelta(days=i)
                
                if date.weekday() >= 5:  # Weekend
                    mood_score = random.choices([3, 4, 5], weights=[2, 4, 3])[0]
                else:  # Weekday
                    mood_score = random.choices([2, 3, 4, 5], weights=[1, 4, 3, 2])[0]
                
                mood_label = self.mood_scale[mood_score]
                note = random.choice(sample_notes)
                sentiment_score, sentiment_label = self.analyze_sentiment(note)
                
                date_str = date.strftime('%Y-%m-%d')
                timestamp = date.strftime('%Y-%m-%d %H:%M:%S')
                
                mood_entry = [date_str, mood_score, mood_label, note, sentiment_score, sentiment_label, timestamp]
                
                with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(mood_entry)
            
            # Reload and update everything
            self.load_data()
            self.update_dashboard()
            self.update_recommendations()
            
            # Recreate charts
            for widget in self.trends_frame.winfo_children():
                widget.destroy()
            for widget in self.frequency_frame.winfo_children():
                widget.destroy()
            for widget in self.weekday_frame.winfo_children():
                widget.destroy()
            
            self.create_charts()
            
            messagebox.showinfo("Success", "Generated 21 days of sample data!")
    
    def update_dashboard(self):
        """Update the dashboard with recent entries."""
        # Clear existing content
        for widget in self.recent_frame.winfo_children():
            widget.destroy()
        
        if len(self.df) == 0:
            ttk.Label(self.recent_frame,
                     text="No mood entries yet. Start by logging your first mood!",
                     font=('Helvetica', 12),
                     background=self.colors['light']).pack()
            return
        
        # Show recent entries
        recent_df = self.df.sort_values('Date', ascending=False).head(5)
        
        for _, row in recent_df.iterrows():
            entry_frame = ttk.Frame(self.recent_frame)
            entry_frame.pack(fill=tk.X, pady=5)
            
            date_str = row['Date'].strftime('%Y-%m-%d (%A)')
            mood_str = f"{row['Mood_Score']} - {row['Mood_Label']}"
            note_str = row['Note'] if pd.notna(row['Note']) and row['Note'] else "No note"
            
            ttk.Label(entry_frame,
                     text=f"📅 {date_str}",
                     font=('Helvetica', 10, 'bold'),
                     background=self.colors['light']).pack(anchor='w')
            
            ttk.Label(entry_frame,
                     text=f"Mood: {mood_str}",
                     font=('Helvetica', 10),
                     background=self.colors['light']).pack(anchor='w')
            
            ttk.Label(entry_frame,
                     text=f"Note: {note_str}",
                     font=('Helvetica', 10),
                     background=self.colors['light'],
                     foreground=self.colors['gray']).pack(anchor='w')
            
            ttk.Separator(entry_frame, orient='horizontal').pack(fill=tk.X, pady=(5, 0))
        
        # Update stats in header
        self.stats_label.config(text=f"Total Entries: {len(self.df)} | Current Streak: {self.calculate_streak()} days")
    
    def update_recommendations(self):
        """Update the recommendations tab."""
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete(1.0, tk.END)
        
        if len(self.df) == 0:
            self.status_label.config(text="No mood data available")
            self.recommendations_text.insert(tk.END, "Log your first mood to get personalized recommendations!")
            self.recommendations_text.config(state=tk.DISABLED)
            return
        
        # Update status
        recent_mood = self.df.tail(1)['Mood_Score'].iloc[0]
        recent_mood_label = self.mood_scale[recent_mood]
        avg_mood = self.df['Mood_Score'].mean()
        
        status_text = f"Current Mood: {recent_mood_label} | 7-day Average: {avg_mood:.1f}"
        self.status_label.config(text=status_text)
        
        # Generate recommendations
        recommendations = self.generate_mood_based_recommendations(recent_mood, avg_mood)
        
        rec_text = "🎯 RECOMMENDATIONS FOR TODAY:\n\n"
        for i, rec in enumerate(recommendations, 1):
            rec_text += f"{i}. {rec}\n\n"
        
        # Add weekday insights if available
        if len(self.df) >= 7:
            df_copy = self.df.copy()
            df_copy['Weekday'] = df_copy['Date'].dt.day_name()
            weekday_moods = df_copy.groupby('Weekday')['Mood_Score'].mean()
            
            today_weekday = datetime.now().strftime('%A')
            if today_weekday in weekday_moods:
                typical_mood = weekday_moods[today_weekday]
                rec_text += f"📅 WEEKDAY INSIGHTS:\n\n"
                rec_text += f"Typical {today_weekday} mood: {typical_mood:.1f}\n\n"
                
                if recent_mood > typical_mood + 0.5:
                    rec_text += f"🌟 You're having a better {today_weekday} than usual!\n"
                    rec_text += f"🚀 Great day for challenging tasks and important decisions\n\n"
                elif recent_mood < typical_mood - 0.5:
                    rec_text += f"💙 You're having a tougher {today_weekday} than usual\n"
                    rec_text += f"🧘 Focus on self-care and easier, familiar tasks\n\n"
        
        # Add mood statistics
        if len(self.df) >= 7:
            recent_avg = self.df.tail(7)['Mood_Score'].mean()
            overall_avg = self.df['Mood_Score'].mean()
            
            rec_text += f"📈 TREND ANALYSIS:\n\n"
            rec_text += f"Last 7 days average: {recent_avg:.2f}\n"
            rec_text += f"Overall average: {overall_avg:.2f}\n\n"
            
            if recent_avg > overall_avg + 0.2:
                rec_text += f"🌟 You're on an upward trend! Keep it up!\n"
            elif recent_avg < overall_avg - 0.2:
                rec_text += f"💙 Recent mood is below your average - consider self-care activities\n"
            else:
                rec_text += f"⚖️ Recent mood is consistent with your overall pattern\n"
        
        self.recommendations_text.insert(tk.END, rec_text)
        self.recommendations_text.config(state=tk.DISABLED)
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text using TextBlob."""
        if not text or text.strip() == "":
            return 0.0, "Neutral"
        
        try:
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            
            if sentiment_score > 0.1:
                sentiment_label = "Positive"
            elif sentiment_score < -0.1:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
            
            return round(sentiment_score, 3), sentiment_label
            
        except Exception as e:
            return 0.0, "Neutral"
    
    def generate_mood_based_recommendations(self, mood_score, avg_mood):
        """Generate specific recommendations based on mood score."""
        recommendations = []
        
        if mood_score == 5:  # Very Happy
            recommendations.extend([
                "🚀 Perfect time for creative projects and brainstorming",
                "📞 Reach out to colleagues for collaboration opportunities",
                "🎯 Tackle your most challenging task while energy is high",
                "📝 Document your current strategies - you're in a great headspace!"
            ])
        elif mood_score == 4:  # Happy
            recommendations.extend([
                "⚡ Great energy for productive work sessions",
                "🤝 Schedule important meetings or presentations",
                "📚 Learn something new - you're in a receptive mindset",
                "🎨 Balance focused work with creative activities"
            ])
        elif mood_score == 3:  # Neutral
            recommendations.extend([
                "⚖️ Perfect for routine tasks and organization",
                "📋 Create to-do lists and plan upcoming projects",
                "🔄 Review and refine existing work",
                "💪 Gradually build momentum with small wins"
            ])
        elif mood_score == 2:  # Sad
            recommendations.extend([
                "🧘 Focus on self-care and stress management",
                "🍃 Take regular breaks and get some fresh air",
                "📞 Connect with supportive friends or colleagues",
                "✅ Stick to simple, achievable tasks today"
            ])
        else:  # Very Sad
            recommendations.extend([
                "💙 Prioritize mental health and well-being",
                "🤗 Reach out to someone you trust for support",
                "🌱 Focus on very basic, nurturing activities",
                "⏰ Consider postponing major decisions until you feel better"
            ])
        
        return recommendations[:4]
    
    def get_mood_emoji(self, mood_score):
        """Convert mood score to emoji."""
        if mood_score >= 4.5:
            return "😄"
        elif mood_score >= 3.5:
            return "😊"
        elif mood_score >= 2.5:
            return "😐"
        elif mood_score >= 1.5:
            return "😞"
        else:
            return "😢"
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def main():
    """Main function to run the GUI application."""
    try:
        # Check for required libraries
        required_libs = ['matplotlib', 'pandas', 'textblob']
        missing_libs = []
        
        for lib in required_libs:
            try:
                __import__(lib)
            except ImportError:
                missing_libs.append(lib)
        
        if missing_libs:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            error_msg = "Missing required libraries:\n\n"
            for lib in missing_libs:
                error_msg += f"pip3 install {lib}\n"
            error_msg += "\nPlease install them and run again!"
            
            messagebox.showerror("Missing Libraries", error_msg)
            return
        
        # Run the application
        app = MoodTrackerGUI()
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()