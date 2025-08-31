# MoodWise Dark Theme - Complete Working Version with Charts
# Dark blue background with high contrast interactive elements

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

class MoodWiseDark:
    def __init__(self):
        self.data_file = 'data/mood_data.csv'
        self.mood_scale = {
            1: {"label": "Very Low", "emoji": "😢"},
            2: {"label": "Low", "emoji": "😞"}, 
            3: {"label": "Neutral", "emoji": "😐"},
            4: {"label": "High", "emoji": "😊"},
            5: {"label": "Very High", "emoji": "😄"}
        }
        
        # Dark professional theme colors
        self.colors = {
            # Dark backgrounds
            'primary_bg': '#0F1419',        # Very dark blue-black
            'secondary_bg': '#1A1F2E',     # Dark blue
            'surface': '#242B3D',          # Lighter dark surface
            'surface_light': '#2D3748',    # Even lighter surface
            'card': '#1E2532',             # Card background
            
            # Accent colors - bright and visible
            'accent': '#00D9FF',           # Bright cyan
            'accent_hover': '#33E1FF',     # Lighter cyan for hover
            'accent_pressed': '#0099CC',   # Darker cyan for pressed
            
            # Status colors - vibrant
            'success': '#00FF88',          # Bright green
            'warning': '#FFB800',          # Bright orange
            'danger': '#FF4757',           # Bright red
            'info': '#7C3AED',             # Purple
            
            # Text colors - high contrast
            'text_primary': '#FFFFFF',     # Pure white
            'text_secondary': '#E2E8F0',   # Light gray
            'text_muted': '#A0AEC0',       # Medium gray
            'text_accent': '#00D9FF',      # Accent text color
            
            # Interactive element colors
            'button_bg': '#00D9FF',        # Bright button background
            'button_hover': '#33E1FF',     # Button hover
            'button_text': '#0F1419',      # Dark text on bright button
            'input_bg': '#2D3748',         # Input background
            'input_border': '#4A5568',     # Input border
            'input_focus': '#00D9FF',      # Focus border
            
            # Border and separator colors
            'border': '#4A5568',           # Visible border
            'border_light': '#2D3748',     # Subtle border
            'separator': '#4A5568'         # Separator lines
        }
        
        # Enhanced fonts for better visibility
        self.fonts = {
            'brand': ('Helvetica', 32, 'bold'),        # Larger brand
            'title': ('Helvetica', 26, 'bold'),        # Larger titles
            'heading': ('Helvetica', 20, 'bold'),      # Larger headings
            'subheading': ('Helvetica', 16, 'bold'),   # Enhanced subheadings
            'body': ('Helvetica', 13, 'normal'),       # Larger body text
            'body_medium': ('Helvetica', 13, 'bold'),  # Bold body text
            'small': ('Helvetica', 12, 'normal'),      # Larger small text
            'small_medium': ('Helvetica', 12, 'bold'), # Bold small text
            'caption': ('Helvetica', 11, 'normal'),    # Captions
            'mood_button': ('Helvetica', 16, 'bold')   # Special for mood buttons
        }
        
        self.setup_data()
        self.create_dark_gui()
        
    def setup_data(self):
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
        
        self.load_data()
    
    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_file)
            if len(self.df) > 0:
                self.df['Date'] = pd.to_datetime(self.df['Date'])
            else:
                self.df = pd.DataFrame(columns=['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
        except Exception as e:
            self.df = pd.DataFrame(columns=['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
    
    def create_dark_gui(self):
        self.root = tk.Tk()
        self.root.title("MoodWise Enterprise - Dark Theme")
        self.root.geometry("1440x900")
        self.root.configure(bg=self.colors['primary_bg'])
        self.root.minsize(1200, 700)
        
        # Configure matplotlib for dark theme
        plt.style.use('dark_background')
        
        self.create_dark_layout()
    
    def create_dark_layout(self):
        # Main container with dark theme
        main_container = tk.Frame(self.root, bg=self.colors['primary_bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        
        # Header
        self.create_dark_header(main_container)
        
        # Navigation
        self.create_dark_navigation(main_container)
        
        # Content area
        self.create_dark_content_area(main_container)
    
    def create_dark_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['primary_bg'], height=90)
        header_frame.pack(fill=tk.X, pady=(0, 32))
        header_frame.pack_propagate(False)
        
        # Left side - branding
        left_header = tk.Frame(header_frame, bg=self.colors['primary_bg'])
        left_header.pack(side=tk.LEFT, fill=tk.Y)
        
        # Brand with glow effect
        brand_label = tk.Label(left_header,
                              text="MoodWise",
                              font=self.fonts['brand'],
                              fg=self.colors['accent'],
                              bg=self.colors['primary_bg'])
        brand_label.pack(anchor='w')
        
        # Enhanced subtitle
        subtitle_label = tk.Label(left_header,
                                 text="Enterprise Mood Analytics Platform",
                                 font=self.fonts['body_medium'],
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['primary_bg'])
        subtitle_label.pack(anchor='w', pady=(6, 0))
        
        # Right side - enhanced stats
        right_header = tk.Frame(header_frame, bg=self.colors['primary_bg'])
        right_header.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.header_stats = tk.Label(right_header,
                                   text=f"Sessions: {len(self.df)} | Streak: {self.calculate_streak()}d",
                                   font=self.fonts['body_medium'],
                                   fg=self.colors['text_accent'],
                                   bg=self.colors['primary_bg'])
        self.header_stats.pack(anchor='e', pady=(35, 0))
    
    def create_dark_navigation(self, parent):
        # Navigation with enhanced dark styling
        nav_frame = tk.Frame(parent, bg=self.colors['surface'], height=64, relief='solid', bd=1)
        nav_frame.configure(highlightbackground=self.colors['border'])
        nav_frame.pack(fill=tk.X, pady=(0, 24))
        nav_frame.pack_propagate(False)
        
        # Navigation container with padding
        nav_container = tk.Frame(nav_frame, bg=self.colors['surface'])
        nav_container.pack(fill=tk.BOTH, expand=True, padx=28, pady=8)
        
        self.nav_buttons = {}
        nav_items = [
            ("Overview", "overview"),
            ("Analytics", "analytics"),
            ("AI Insights", "insights"),
            ("Settings", "settings")
        ]
        
        for text, key in nav_items:
            # Enhanced navigation buttons
            btn = tk.Button(nav_container,
                          text=text,
                          font=self.fonts['body_medium'],
                          fg=self.colors['text_secondary'],
                          bg=self.colors['surface'],
                          activeforeground=self.colors['text_primary'],
                          activebackground=self.colors['surface_light'],
                          relief='flat',
                          border=0,
                          padx=28,
                          pady=18,
                          cursor='hand2',
                          command=lambda k=key: self.switch_view(k))
            btn.pack(side=tk.LEFT)
            self.nav_buttons[key] = btn
            
            # Enhanced hover effects
            btn.bind("<Enter>", lambda e, b=btn: self.on_nav_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.on_nav_hover(b, False))
        
        # Prominent action button
        action_btn = tk.Button(nav_container,
                             text="+ New Entry",
                             font=self.fonts['body_medium'],
                             fg=self.colors['button_text'],
                             bg=self.colors['button_bg'],
                             activeforeground=self.colors['button_text'],
                             activebackground=self.colors['button_hover'],
                             relief='flat',
                             border=0,
                             padx=24,
                             pady=14,
                             cursor='hand2',
                             command=self.quick_mood_entry)
        action_btn.pack(side=tk.RIGHT, pady=6)
        
        # Enhanced button hover
        action_btn.bind("<Enter>", lambda e: action_btn.config(bg=self.colors['button_hover']))
        action_btn.bind("<Leave>", lambda e: action_btn.config(bg=self.colors['button_bg']))
    
    def create_dark_content_area(self, parent):
        # Dark content container
        self.content_container = tk.Frame(parent, bg=self.colors['secondary_bg'])
        self.content_container.pack(fill=tk.BOTH, expand=True)
        
        # Create views
        self.views = {}
        self.create_dark_overview_view()
        self.create_dark_analytics_view()
        self.create_dark_insights_view()
        self.create_dark_settings_view()
        
        # Show overview by default
        self.current_view = None
        self.switch_view("overview")
    
    def create_dark_overview_view(self):
        overview = tk.Frame(self.content_container, bg=self.colors['secondary_bg'])
        
        # Scrollable dark content
        canvas = tk.Canvas(overview, bg=self.colors['secondary_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(overview, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['secondary_bg'])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_frame, width=event.width)
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Dark content area
        content_area = tk.Frame(scrollable_frame, bg=self.colors['secondary_bg'])
        content_area.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        
        # Sections with enhanced dark styling
        self.create_dark_metrics_section(content_area)
        self.create_enhanced_quick_entry_section(content_area)
        self.create_dark_recent_activity_section(content_area)
        
        self.views["overview"] = overview
    
    def create_dark_metrics_section(self, parent):
        metrics_section = tk.Frame(parent, bg=self.colors['secondary_bg'])
        metrics_section.pack(fill=tk.X, pady=(0, 40))
        
        # Enhanced section title
        title_label = tk.Label(metrics_section,
                             text="Key Metrics",
                             font=self.fonts['heading'],
                             fg=self.colors['text_primary'],
                             bg=self.colors['secondary_bg'])
        title_label.pack(anchor='w', pady=(0, 24))
        
        # Metrics container
        metrics_container = tk.Frame(metrics_section, bg=self.colors['secondary_bg'])
        metrics_container.pack(fill=tk.X)
        
        # Enhanced metric cards with dark theme
        self.create_dark_metric_card(metrics_container, "Total Sessions", str(len(self.df)), self.colors['accent'], 0)
        self.create_dark_metric_card(metrics_container, "Average Score", self.get_avg_mood_display(), self.colors['success'], 1)
        self.create_dark_metric_card(metrics_container, "Current Streak", f"{self.calculate_streak()} days", self.colors['warning'], 2)
        self.create_dark_metric_card(metrics_container, "This Week", self.get_week_summary(), self.colors['danger'], 3)
    
    def create_dark_metric_card(self, parent, title, value, accent_color, col):
        # Enhanced dark card with better visibility
        card = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=2)
        card.configure(highlightbackground=self.colors['border'], highlightthickness=1)
        card.grid(row=0, column=col, padx=(0, 20) if col < 3 else (0, 0), pady=0, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        # Card content with better spacing
        card_content = tk.Frame(card, bg=self.colors['surface'])
        card_content.pack(fill=tk.BOTH, expand=True, padx=28, pady=24)
        
        # Prominent accent bar
        accent_bar = tk.Frame(card_content, bg=accent_color, height=4)
        accent_bar.pack(fill=tk.X, pady=(0, 18))
        
        # Large, visible value
        value_label = tk.Label(card_content,
                             text=value,
                             font=('Helvetica', 28, 'bold'),
                             fg=self.colors['text_primary'],
                             bg=self.colors['surface'])
        value_label.pack(anchor='w')
        
        # Clear title with accent color
        title_label = tk.Label(card_content,
                             text=title,
                             font=self.fonts['body_medium'],
                             fg=accent_color,
                             bg=self.colors['surface'])
        title_label.pack(anchor='w', pady=(6, 0))
    
    def create_enhanced_quick_entry_section(self, parent):
        entry_section = tk.Frame(parent, bg=self.colors['secondary_bg'])
        entry_section.pack(fill=tk.X, pady=(0, 40))
        
        # Enhanced section title
        title_label = tk.Label(entry_section,
                             text="Quick Mood Entry",
                             font=self.fonts['heading'],
                             fg=self.colors['text_primary'],
                             bg=self.colors['secondary_bg'])
        title_label.pack(anchor='w', pady=(0, 24))
        
        # Enhanced entry card
        entry_card = tk.Frame(entry_section, bg=self.colors['surface'], relief='solid', bd=2)
        entry_card.configure(highlightbackground=self.colors['border'])
        entry_card.pack(fill=tk.X)
        
        entry_content = tk.Frame(entry_card, bg=self.colors['surface'])
        entry_content.pack(fill=tk.X, padx=36, pady=32)
        
        # Prominent question
        question_label = tk.Label(entry_content,
                                text="How's your mood today?",
                                font=self.fonts['subheading'],
                                fg=self.colors['text_primary'],
                                bg=self.colors['surface'])
        question_label.pack(anchor='w', pady=(0, 24))
        
        # Enhanced mood buttons with emojis
        mood_frame = tk.Frame(entry_content, bg=self.colors['surface'])
        mood_frame.pack(fill=tk.X, pady=(0, 28))
        
        self.mood_var = tk.IntVar(value=3)
        self.mood_buttons = {}
        
        for score, mood_data in self.mood_scale.items():
            # Create prominent mood button with emoji
            btn_frame = tk.Frame(mood_frame, bg=self.colors['surface'])
            btn_frame.pack(side=tk.LEFT, padx=(0, 16), expand=True, fill=tk.X)
            
            mood_btn = tk.Button(btn_frame,
                               text=f"{mood_data['emoji']}\n{score}",
                               font=self.fonts['mood_button'],
                               fg=self.colors['text_secondary'],
                               bg=self.colors['surface_light'],
                               activeforeground=self.colors['text_primary'],
                               activebackground=self.colors['accent'],
                               relief='solid',
                               bd=2,
                               width=6,
                               height=3,
                               cursor='hand2',
                               command=lambda s=score: self.select_enhanced_mood(s))
            mood_btn.pack(expand=True, fill=tk.BOTH)
            self.mood_buttons[score] = mood_btn
            
            # Enhanced hover effects
            mood_btn.bind("<Enter>", lambda e, b=mood_btn: b.config(
                bg=self.colors['accent'], 
                fg=self.colors['button_text'],
                relief='solid'
            ))
            mood_btn.bind("<Leave>", lambda e, b=mood_btn, s=score: self.update_mood_button_state(b, s))
        
        # Selected mood display with better visibility
        self.quick_mood_label = tk.Label(entry_content,
                                       text="Selected: 😐 Neutral",
                                       font=self.fonts['body_medium'],
                                       fg=self.colors['text_accent'],
                                       bg=self.colors['surface'])
        self.quick_mood_label.pack(anchor='w', pady=(0, 24))
        
        # Enhanced note input
        note_label = tk.Label(entry_content,
                            text="Add a note (optional)",
                            font=self.fonts['body_medium'],
                            fg=self.colors['text_primary'],
                            bg=self.colors['surface'])
        note_label.pack(anchor='w', pady=(0, 12))
        
        self.quick_note_entry = tk.Text(entry_content,
                                      height=4,
                                      font=self.fonts['body'],
                                      fg=self.colors['text_primary'],
                                      bg=self.colors['input_bg'],
                                      insertbackground=self.colors['text_primary'],
                                      selectbackground=self.colors['accent'],
                                      relief='solid',
                                      bd=2,
                                      padx=16,
                                      pady=12)
        self.quick_note_entry.pack(fill=tk.X, pady=(0, 32))
        
        # Bind focus events for input highlighting
        self.quick_note_entry.bind("<FocusIn>", lambda e: self.quick_note_entry.config(
            highlightbackground=self.colors['input_focus'],
            highlightcolor=self.colors['input_focus'],
            highlightthickness=2
        ))
        self.quick_note_entry.bind("<FocusOut>", lambda e: self.quick_note_entry.config(
            highlightthickness=0
        ))
        
        # Prominent save button
        button_frame = tk.Frame(entry_content, bg=self.colors['surface'])
        button_frame.pack(fill=tk.X)
        
        save_btn = tk.Button(button_frame,
                           text="💾 Save Entry",
                           font=('Helvetica', 16, 'bold'),
                           fg=self.colors['button_text'],
                           bg=self.colors['accent'],
                           activeforeground=self.colors['button_text'],
                           activebackground=self.colors['accent_hover'],
                           relief='flat',
                           border=0,
                           padx=32,
                           pady=16,
                           cursor='hand2',
                           command=self.save_quick_mood)
        save_btn.pack(side=tk.LEFT)
        
        # Enhanced save button effects
        save_btn.bind("<Enter>", lambda e: save_btn.config(
            bg=self.colors['accent_hover'],
            relief='solid',
            bd=2
        ))
        save_btn.bind("<Leave>", lambda e: save_btn.config(
            bg=self.colors['accent'],
            relief='flat',
            bd=0
        ))
        
        # Sample data button
        sample_btn = tk.Button(button_frame,
                             text="🧪 Generate Sample Data",
                             font=self.fonts['body_medium'],
                             fg=self.colors['text_secondary'],
                             bg=self.colors['surface_light'],
                             activeforeground=self.colors['text_primary'],
                             activebackground=self.colors['info'],
                             relief='solid',
                             bd=1,
                             padx=24,
                             pady=12,
                             cursor='hand2',
                             command=self.generate_sample_data)
        sample_btn.pack(side=tk.RIGHT)
        
        sample_btn.bind("<Enter>", lambda e: sample_btn.config(bg=self.colors['info']))
        sample_btn.bind("<Leave>", lambda e: sample_btn.config(bg=self.colors['surface_light']))
    
    def select_enhanced_mood(self, score):
        self.mood_var.set(score)
        mood_data = self.mood_scale[score]
        self.quick_mood_label.config(text=f"Selected: {mood_data['emoji']} {mood_data['label']}")
        
        # Update all button states
        for btn_score, button in self.mood_buttons.items():
            self.update_mood_button_state(button, btn_score)
    
    def update_mood_button_state(self, button, score):
        if self.mood_var.get() == score:
            # Selected state
            button.config(
                bg=self.colors['accent'],
                fg=self.colors['button_text'],
                relief='solid',
                bd=3
            )
        else:
            # Normal state
            button.config(
                bg=self.colors['surface_light'],
                fg=self.colors['text_secondary'],
                relief='solid',
                bd=2
            )
    
    def create_dark_recent_activity_section(self, parent):
        activity_section = tk.Frame(parent, bg=self.colors['secondary_bg'])
        activity_section.pack(fill=tk.BOTH, expand=True)
        
        # Enhanced header
        header_frame = tk.Frame(activity_section, bg=self.colors['secondary_bg'])
        header_frame.pack(fill=tk.X, pady=(0, 24))
        
        title_label = tk.Label(header_frame,
                             text="Recent Activity",
                             font=self.fonts['heading'],
                             fg=self.colors['text_primary'],
                             bg=self.colors['secondary_bg'])
        title_label.pack(side=tk.LEFT)
        
        # Enhanced activity container
        self.activity_container = tk.Frame(activity_section, bg=self.colors['surface'], relief='solid', bd=2)
        self.activity_container.configure(highlightbackground=self.colors['border'])
        self.activity_container.pack(fill=tk.BOTH, expand=True)
        
        self.update_dark_recent_activity()
    
    def create_dark_analytics_view(self):
        analytics = tk.Frame(self.content_container, bg=self.colors['secondary_bg'])
        
        content_area = tk.Frame(analytics, bg=self.colors['secondary_bg'])
        content_area.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        
        title_label = tk.Label(content_area,
                             text="Analytics Dashboard",
                             font=self.fonts['title'],
                             fg=self.colors['text_primary'],
                             bg=self.colors['secondary_bg'])
        title_label.pack(anchor='w', pady=(0, 32))
        
        chart_frame = tk.Frame(content_area, bg=self.colors['secondary_bg'])
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dark themed notebook
        style = ttk.Style()
        style.configure('Dark.TNotebook', background=self.colors['surface'])
        style.configure('Dark.TNotebook.Tab', 
                       background=self.colors['surface_light'],
                       foreground=self.colors['text_secondary'],
                       padding=[20, 12],
                       font=self.fonts['body_medium'])
        style.map('Dark.TNotebook.Tab',
                 background=[('selected', self.colors['accent']),
                           ('active', self.colors['surface_light'])],
                 foreground=[('selected', self.colors['button_text']),
                           ('active', self.colors['text_primary'])])
        
        self.chart_notebook = ttk.Notebook(chart_frame, style='Dark.TNotebook')
        self.chart_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dark chart frames
        self.trends_frame = tk.Frame(self.chart_notebook, bg=self.colors['surface'])
        self.frequency_frame = tk.Frame(self.chart_notebook, bg=self.colors['surface'])
        self.patterns_frame = tk.Frame(self.chart_notebook, bg=self.colors['surface'])
        
        self.chart_notebook.add(self.trends_frame, text="📈 Trends")
        self.chart_notebook.add(self.frequency_frame, text="🍕 Distribution")
        self.chart_notebook.add(self.patterns_frame, text="📅 Patterns")
        
        self.views["analytics"] = analytics
    
    def create_dark_insights_view(self):
        insights = tk.Frame(self.content_container, bg=self.colors['secondary_bg'])
        
        content_area = tk.Frame(insights, bg=self.colors['secondary_bg'])
        content_area.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        
        title_label = tk.Label(content_area,
                             text="AI Insights",
                             font=self.fonts['title'],
                             fg=self.colors['text_primary'],
                             bg=self.colors['secondary_bg'])
        title_label.pack(anchor='w', pady=(0, 32))
        
        self.insights_container = tk.Frame(content_area, bg=self.colors['secondary_bg'])
        self.insights_container.pack(fill=tk.BOTH, expand=True)
        
        self.views["insights"] = insights
    
    def create_dark_settings_view(self):
        settings = tk.Frame(self.content_container, bg=self.colors['secondary_bg'])
        
        content_area = tk.Frame(settings, bg=self.colors['secondary_bg'])
        content_area.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        
        title_label = tk.Label(content_area,
                             text="Settings",
                             font=self.fonts['title'],
                             fg=self.colors['text_primary'],
                             bg=self.colors['secondary_bg'])
        title_label.pack(anchor='w', pady=(0, 32))
        
        settings_content = tk.Label(content_area,
                                   text="Settings and preferences will be available here.",
                                   font=self.fonts['body'],
                                   fg=self.colors['text_muted'],
                                   bg=self.colors['secondary_bg'])
        settings_content.pack(pady=100)
        
        self.views["settings"] = settings
    
    def on_nav_hover(self, button, is_enter):
        if is_enter:
            button.config(
                fg=self.colors['text_primary'],
                bg=self.colors['accent'],
                relief='solid',
                bd=1
            )
        else:
            button.config(
                fg=self.colors['text_secondary'],
                bg=self.colors['surface'],
                relief='flat',
                bd=0
            )
    
    def switch_view(self, view_name):
        if self.current_view:
            self.views[self.current_view].pack_forget()
        
        self.views[view_name].pack(fill=tk.BOTH, expand=True)
        self.current_view = view_name
        
        # Enhanced navigation state
        for key, btn in self.nav_buttons.items():
            if key == view_name:
                btn.config(
                    fg=self.colors['button_text'],
                    bg=self.colors['accent'],
                    relief='solid',
                    bd=2
                )
            else:
                btn.config(
                    fg=self.colors['text_secondary'],
                    bg=self.colors['surface'],
                    relief='flat',
                    bd=0
                )
        
        if view_name == "analytics":
            self.update_dark_analytics()
        elif view_name == "insights":
            self.update_dark_insights()
    
    def quick_mood_entry(self):
        self.switch_view("overview")
    
    def save_quick_mood(self):
        mood_score = self.mood_var.get()
        mood_data = self.mood_scale[mood_score]
        note = self.quick_note_entry.get("1.0", tk.END).strip()
        
        sentiment_score, sentiment_label = self.analyze_sentiment(note)
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        mood_entry = [current_date, mood_score, mood_data['label'], note, sentiment_score, sentiment_label, current_timestamp]
        
        try:
            with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(mood_entry)
            
            # Enhanced success message with dark theme
            msg = tk.Toplevel(self.root)
            msg.title("Success")
            msg.geometry("400x200")
            msg.configure(bg=self.colors['surface'])
            msg.transient(self.root)
            msg.grab_set()
            
            tk.Label(msg, 
                    text="✅ Entry Saved Successfully!",
                    font=self.fonts['subheading'],
                    fg=self.colors['success'],
                    bg=self.colors['surface']).pack(pady=20)
            
            tk.Label(msg,
                    text=f"Mood: {mood_data['emoji']} {mood_data['label']}\nSentiment: {sentiment_label}",
                    font=self.fonts['body'],
                    fg=self.colors['text_primary'],
                    bg=self.colors['surface']).pack(pady=10)
            
            ok_btn = tk.Button(msg,
                             text="OK",
                             font=self.fonts['body_medium'],
                             fg=self.colors['button_text'],
                             bg=self.colors['accent'],
                             padx=30, pady=10,
                             command=msg.destroy)
            ok_btn.pack(pady=20)
            
            # Clear and refresh
            self.mood_var.set(3)
            self.quick_note_entry.delete("1.0", tk.END)
            self.select_enhanced_mood(3)
            
            self.load_data()
            self.update_header_stats()
            self.update_dark_recent_activity()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entry: {str(e)}")
    
    def get_avg_mood_display(self):
        if len(self.df) == 0:
            return "—"
        return f"{self.df['Mood_Score'].mean():.1f}"
    
    def get_week_summary(self):
        if len(self.df) == 0:
            return "—"
        
        week_ago = datetime.now() - timedelta(days=7)
        recent_data = self.df[self.df['Date'] >= week_ago]
        return f"{len(recent_data)} entries" if len(recent_data) > 0 else "—"
    
    def calculate_streak(self):
        if len(self.df) == 0:
            return 0
        
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
    
    def update_header_stats(self):
        self.header_stats.config(text=f"Sessions: {len(self.df)} | Streak: {self.calculate_streak()}d")
    
    def update_dark_recent_activity(self):
        # Clear existing content
        for widget in self.activity_container.winfo_children():
            widget.destroy()
        
        if len(self.df) == 0:
            empty_frame = tk.Frame(self.activity_container, bg=self.colors['surface'])
            empty_frame.pack(expand=True, fill=tk.BOTH, pady=80)
            
            tk.Label(empty_frame,
                    text="🌟 No activity yet",
                    font=self.fonts['subheading'],
                    fg=self.colors['text_muted'],
                    bg=self.colors['surface']).pack()
            
            tk.Label(empty_frame,
                    text="Start tracking your mood to see activity here",
                    font=self.fonts['body'],
                    fg=self.colors['text_muted'],
                    bg=self.colors['surface']).pack(pady=(12, 0))
            return
        
        # Show recent entries with dark theme
        recent_df = self.df.sort_values('Date', ascending=False).head(8)
        
        for i, (_, row) in enumerate(recent_df.iterrows()):
            self.create_dark_activity_row(self.activity_container, row, i)
    
    def create_dark_activity_row(self, parent, row, index):
        # Enhanced dark activity rows
        bg_color = self.colors['surface_light'] if index % 2 == 0 else self.colors['surface']
        
        row_frame = tk.Frame(parent, bg=bg_color)
        row_frame.pack(fill=tk.X, padx=2, pady=1)
        
        content_frame = tk.Frame(row_frame, bg=bg_color)
        content_frame.pack(fill=tk.X, pady=16, padx=24)
        
        # Date with better visibility
        date_str = row['Date'].strftime('%b %d, %Y')
        date_label = tk.Label(content_frame,
                            text=date_str,
                            font=self.fonts['small_medium'],
                            fg=self.colors['text_primary'],
                            bg=bg_color,
                            width=15)
        date_label.pack(side=tk.LEFT, anchor='w')
        
        # Mood with emoji and color
        mood_score = row['Mood_Score']
        mood_data = self.mood_scale[mood_score]
        
        mood_frame = tk.Frame(content_frame, bg=bg_color)
        mood_frame.pack(side=tk.LEFT, padx=(24, 0))
        
        tk.Label(mood_frame,
                text=f"{mood_data['emoji']} {mood_data['label']}",
                font=self.fonts['small_medium'],
                fg=self.colors['text_primary'],
                bg=bg_color).pack(side=tk.LEFT)
        
        # Note preview
        note = row['Note'] if pd.notna(row['Note']) and row['Note'] else ""
        if note:
            if len(note) > 45:
                note = note[:45] + "..."
            
            note_label = tk.Label(content_frame,
                                text=note,
                                font=self.fonts['caption'],
                                fg=self.colors['text_muted'],
                                bg=bg_color)
            note_label.pack(side=tk.RIGHT, padx=(24, 0))
    
    def update_dark_analytics(self):
        """Update analytics charts with dark theme"""
        if len(self.df) == 0:
            # Show "no data" message in each tab
            for frame in [self.trends_frame, self.frequency_frame, self.patterns_frame]:
                for widget in frame.winfo_children():
                    widget.destroy()
                tk.Label(frame, 
                        text="📊 No data available\nGenerate sample data to see charts",
                        font=self.fonts['body'],
                        fg=self.colors['text_muted'],
                        bg=self.colors['surface']).pack(expand=True)
            return
        
        self.create_trends_chart()
        self.create_frequency_chart() 
        self.create_patterns_chart()
    
    def create_trends_chart(self):
        """Create mood trends over time chart"""
        # Clear existing content
        for widget in self.trends_frame.winfo_children():
            widget.destroy()
        
        # Prepare data
        chart_df = self.df.copy()
        chart_df = chart_df.sort_values('Date')
        
        # Create matplotlib figure with dark theme
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.colors['surface'])
        fig.patch.set_facecolor(self.colors['surface'])
        ax.set_facecolor(self.colors['surface'])
        
        # Plot trend line
        ax.plot(chart_df['Date'], chart_df['Mood_Score'], 
               color=self.colors['accent'], linewidth=3, marker='o', markersize=6)
        
        # Style the chart
        ax.set_title('Mood Trends Over Time', 
                    color=self.colors['text_primary'], 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', color=self.colors['text_secondary'], fontsize=12)
        ax.set_ylabel('Mood Score', color=self.colors['text_secondary'], fontsize=12)
        
        # Customize grid and ticks
        ax.grid(True, color=self.colors['border'], alpha=0.3)
        ax.tick_params(colors=self.colors['text_secondary'])
        ax.set_ylim(0.5, 5.5)
        
        # Format dates on x-axis
        fig.autofmt_xdate()
        
        plt.tight_layout()
        
        # Add to tkinter
        canvas = FigureCanvasTkAgg(fig, self.trends_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def create_frequency_chart(self):
        """Create mood frequency distribution chart"""
        # Clear existing content
        for widget in self.frequency_frame.winfo_children():
            widget.destroy()
        
        # Prepare data
        mood_counts = self.df['Mood_Score'].value_counts().sort_index()
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=self.colors['surface'])
        fig.patch.set_facecolor(self.colors['surface'])
        ax.set_facecolor(self.colors['surface'])
        
        # Create bar chart
        bars = ax.bar(mood_counts.index, mood_counts.values, 
                     color=self.colors['accent'], alpha=0.8, width=0.6)
        
        # Add mood labels
        labels = [self.mood_scale[score]['label'] for score in mood_counts.index]
        ax.set_xticks(mood_counts.index)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        
        # Style the chart
        ax.set_title('Mood Distribution', 
                    color=self.colors['text_primary'], 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Mood Level', color=self.colors['text_secondary'], fontsize=12)
        ax.set_ylabel('Frequency', color=self.colors['text_secondary'], fontsize=12)
        
        # Customize
        ax.grid(True, axis='y', color=self.colors['border'], alpha=0.3)
        ax.tick_params(colors=self.colors['text_secondary'])
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(height)}', ha='center', va='bottom',
                   color=self.colors['text_primary'], fontweight='bold')
        
        plt.tight_layout()
        
        # Add to tkinter
        canvas = FigureCanvasTkAgg(fig, self.frequency_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def create_patterns_chart(self):
        """Create weekly patterns chart"""
        # Clear existing content
        for widget in self.patterns_frame.winfo_children():
            widget.destroy()
        
        if len(self.df) == 0:
            return
        
        # Prepare data - group by day of week
        df_copy = self.df.copy()
        df_copy['DayOfWeek'] = df_copy['Date'].dt.day_name()
        df_copy['DayNum'] = df_copy['Date'].dt.dayofweek
        
        # Calculate average mood by day of week
        day_avg = df_copy.groupby(['DayNum', 'DayOfWeek'])['Mood_Score'].mean().reset_index()
        day_avg = day_avg.sort_values('DayNum')
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.colors['surface'])
        fig.patch.set_facecolor(self.colors['surface'])
        ax.set_facecolor(self.colors['surface'])
        
        # Create line chart
        ax.plot(day_avg['DayOfWeek'], day_avg['Mood_Score'], 
               color=self.colors['accent'], linewidth=4, marker='o', markersize=8)
        
        # Style the chart
        ax.set_title('Weekly Mood Patterns', 
                    color=self.colors['text_primary'], 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Day of Week', color=self.colors['text_secondary'], fontsize=12)
        ax.set_ylabel('Average Mood Score', color=self.colors['text_secondary'], fontsize=12)
        
        # Customize
        ax.grid(True, color=self.colors['border'], alpha=0.3)
        ax.tick_params(colors=self.colors['text_secondary'])
        ax.set_ylim(1, 5)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Add to tkinter
        canvas = FigureCanvasTkAgg(fig, self.patterns_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def update_dark_insights(self):
        # Clear existing content
        for widget in self.insights_container.winfo_children():
            widget.destroy()
        
        if len(self.df) == 0:
            empty_frame = tk.Frame(self.insights_container, bg=self.colors['secondary_bg'])
            empty_frame.pack(expand=True, fill=tk.BOTH, pady=100)
            
            tk.Label(empty_frame,
                    text="🤖 No insights available yet",
                    font=self.fonts['subheading'],
                    fg=self.colors['text_muted'],
                    bg=self.colors['secondary_bg']).pack()
            
            tk.Label(empty_frame,
                    text="Add some mood entries to see AI-powered insights",
                    font=self.fonts['body'],
                    fg=self.colors['text_muted'],
                    bg=self.colors['secondary_bg']).pack(pady=(12, 0))
            return
        
        # Create insights content
        insights_content = tk.Frame(self.insights_container, bg=self.colors['secondary_bg'])
        insights_content.pack(fill=tk.BOTH, expand=True, padx=32, pady=24)
        
        # Sample insights based on data
        avg_mood = self.df['Mood_Score'].mean()
        total_entries = len(self.df)
        
        insights = [
            f"📈 Your average mood score is {avg_mood:.1f}/5.0",
            f"📊 You've logged {total_entries} mood entries",
            f"🎯 Most common mood: {self.df['Mood_Score'].mode().iloc[0]}/5 ({self.mood_scale[self.df['Mood_Score'].mode().iloc[0]]['label']})",
        ]
        
        for i, insight in enumerate(insights):
            insight_card = tk.Frame(insights_content, bg=self.colors['surface'], relief='solid', bd=1)
            insight_card.pack(fill=tk.X, pady=(0, 16))
            
            tk.Label(insight_card,
                    text=insight,
                    font=self.fonts['body_medium'],
                    fg=self.colors['text_primary'],
                    bg=self.colors['surface']).pack(pady=20, padx=24, anchor='w')
    
    def generate_sample_data(self):
        """Generate sample mood data for testing"""
        if messagebox.askyesno("Generate Sample Data", 
                              "This will add 30 days of sample mood data.\n\nContinue?"):
            
            sample_notes = [
                "Productive morning session", "Challenging but rewarding day", "Great collaboration",
                "Focused and motivated", "Problem-solving breakthrough", "Positive feedback received",
                "Project milestone reached", "Creative inspiration", "Effective time management",
                "Strong accomplishment feeling", "Good work-life balance", "Meaningful progress made"
            ]
            
            base_date = datetime.now() - timedelta(days=29)
            
            try:
                for i in range(30):
                    date = base_date + timedelta(days=i)
                    
                    if date.weekday() >= 5:  # Weekend
                        mood_score = random.choices([3, 4, 5], weights=[1, 3, 2])[0]
                    else:  # Weekday
                        mood_score = random.choices([2, 3, 4, 5], weights=[1, 3, 3, 1])[0]
                    
                    mood_data = self.mood_scale[mood_score]
                    note = random.choice(sample_notes)
                    sentiment_score, sentiment_label = self.analyze_sentiment(note)
                    
                    date_str = date.strftime('%Y-%m-%d')
                    timestamp = date.strftime('%Y-%m-%d %H:%M:%S')
                    
                    mood_entry = [date_str, mood_score, mood_data['label'], note, sentiment_score, sentiment_label, timestamp]
                    
                    with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(mood_entry)
                
                self.load_data()
                self.update_header_stats()
                self.update_dark_recent_activity()
                
                messagebox.showinfo("Success", "Generated 30 days of sample data!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate sample data: {str(e)}")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text input"""
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
        except:
            return 0.0, "Neutral"
    
    def run(self):
        """Start the application"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

def main():
    """Main function to start the application"""
    try:
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
            root.withdraw()
            
            error_msg = "Missing Required Libraries\n\n"
            error_msg += "Install the following:\n\n"
            for lib in missing_libs:
                error_msg += f"pip3 install {lib}\n"
            error_msg += "\nRestart after installation."
            
            messagebox.showerror("Installation Required", error_msg)
            return
        
        app = MoodWiseDark()
        app.run()
        
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        messagebox.showerror("Application Error", 
                           f"Failed to start MoodWise:\n\n{str(e)}")

if __name__ == "__main__":
    main()