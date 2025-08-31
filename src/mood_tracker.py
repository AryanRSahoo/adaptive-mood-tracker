# Adaptive Emotion-Based Productivity Assistant with Daily Reminders
# Day 10: Adding daily reminder functionality with the schedule library

import csv
import os
from datetime import datetime, timedelta
import sys
import matplotlib.pyplot as plt
import pandas as pd
from textblob import TextBlob
from collections import Counter, defaultdict
import numpy as np
import random
import schedule
import time
import threading
import json
from pathlib import Path

class MoodTrackerWithReminders:
    """
    Enhanced Mood Tracker with daily reminder functionality.
    """
    
    def __init__(self, data_file='data/mood_data.csv'):
        self.data_file = data_file
        self.settings_file = 'data/settings.json'
        
        self.mood_scale = {
            1: "Very Sad 😢",
            2: "Sad 😞", 
            3: "Neutral 😐",
            4: "Happy 😊",
            5: "Very Happy 😄"
        }
        
        # Default reminder settings
        self.default_settings = {
            'reminder_enabled': True,
            'reminder_time': '20:00',  # 8 PM default
            'reminder_message': 'Time to log your daily mood! 📝',
            'last_reminder_date': None,
            'consecutive_days': 0
        }
        
        # Setup data directory and files
        self.setup_data_directory()
        self.initialize_csv_file()
        self.load_settings()
        self.load_data()
        
        # Start background reminder scheduler
        self.reminder_thread = None
        self.start_reminder_scheduler()
    
    def setup_data_directory(self):
        """Create data directory if it doesn't exist."""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"✅ Created data directory: {data_dir}")
        
        # Create reports directory
        reports_dir = "data/reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
    
    def initialize_csv_file(self):
        """Create CSV file with proper headers if it doesn't exist."""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
            print(f"✅ Created new mood data file: {self.data_file}")
    
    def load_settings(self):
        """Load user settings from JSON file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                print(f"📁 Loaded settings from {self.settings_file}")
            else:
                self.settings = self.default_settings.copy()
                self.save_settings()
                print(f"⚙️ Created default settings file")
        except Exception as e:
            print(f"⚠️ Error loading settings: {e}")
            self.settings = self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to JSON file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving settings: {e}")
    
    def load_data(self):
        """Load existing data from CSV into pandas DataFrame."""
        try:
            if os.path.exists(self.data_file):
                self.df = pd.read_csv(self.data_file)
                if len(self.df) > 0:
                    self.df['Date'] = pd.to_datetime(self.df['Date'])
                    print(f"📊 Loaded {len(self.df)} existing mood entries")
                else:
                    self.df = pd.DataFrame(columns=['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
            else:
                self.df = pd.DataFrame(columns=['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
        except Exception as e:
            print(f"⚠️ Error loading data: {e}")
            self.df = pd.DataFrame(columns=['Date', 'Mood_Score', 'Mood_Label', 'Note', 'Sentiment_Score', 'Sentiment_Label', 'Timestamp'])
    
    def start_reminder_scheduler(self):
        """Start the background scheduler for daily reminders."""
        if not self.settings['reminder_enabled']:
            return
        
        # Clear any existing scheduled jobs
        schedule.clear()
        
        # Schedule the daily reminder
        reminder_time = self.settings['reminder_time']
        schedule.every().day.at(reminder_time).do(self.send_daily_reminder)
        
        # Start the scheduler in a separate thread
        self.reminder_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.reminder_thread.start()
        
        print(f"⏰ Daily reminders scheduled for {reminder_time}")
    
    def run_scheduler(self):
        """Run the schedule checker in a background thread."""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def send_daily_reminder(self):
        """Send a daily reminder notification."""
        current_date = datetime.now().date()
        
        # Check if already logged today
        if self.has_logged_today():
            print(f"✅ Mood already logged for {current_date}")
            return
        
        # Check if this is a duplicate reminder for the same day
        last_reminder = self.settings.get('last_reminder_date')
        if last_reminder == str(current_date):
            return
        
        # Update last reminder date
        self.settings['last_reminder_date'] = str(current_date)
        self.save_settings()
        
        # Display reminder
        self.display_reminder_notification()
    
    def display_reminder_notification(self):
        """Display the reminder notification in terminal."""
        print("\n" + "="*60)
        print("🔔 DAILY MOOD REMINDER")
        print("="*60)
        print(f"📅 Date: {datetime.now().strftime('%A, %B %d, %Y')}")
        print(f"⏰ Time: {datetime.now().strftime('%I:%M %p')}")
        print(f"💭 {self.settings['reminder_message']}")
        
        # Show streak information
        streak = self.calculate_streak()
        if streak > 0:
            print(f"🔥 Current streak: {streak} days - Keep it going!")
        
        print("="*60)
        
        # Optional: Play a sound (cross-platform)
        try:
            if os.name == 'nt':  # Windows
                import winsound
                winsound.Beep(1000, 500)
            else:  # macOS/Linux
                print('\a')  # Terminal bell
        except:
            pass  # Silent if sound fails
    
    def has_logged_today(self):
        """Check if user has already logged mood today."""
        if len(self.df) == 0:
            return False
        
        today = datetime.now().date()
        today_entries = self.df[self.df['Date'].dt.date == today]
        return len(today_entries) > 0
    
    def calculate_streak(self):
        """Calculate current logging streak."""
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
    
    def configure_reminders(self):
        """Configure reminder settings through interactive menu."""
        print("\n⚙️ REMINDER SETTINGS")
        print("="*40)
        
        while True:
            print(f"\nCurrent Settings:")
            print(f"  1. Reminders: {'✅ Enabled' if self.settings['reminder_enabled'] else '❌ Disabled'}")
            print(f"  2. Time: {self.settings['reminder_time']}")
            print(f"  3. Message: {self.settings['reminder_message']}")
            print(f"  4. Last reminded: {self.settings.get('last_reminder_date', 'Never')}")
            print(f"\n  5. Test reminder now")
            print(f"  6. Back to main menu")
            
            choice = input("\nWhat would you like to change? (1-6): ").strip()
            
            if choice == '1':
                self.toggle_reminders()
            elif choice == '2':
                self.set_reminder_time()
            elif choice == '3':
                self.set_reminder_message()
            elif choice == '5':
                self.test_reminder()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
    
    def toggle_reminders(self):
        """Toggle reminders on/off."""
        self.settings['reminder_enabled'] = not self.settings['reminder_enabled']
        status = "enabled" if self.settings['reminder_enabled'] else "disabled"
        print(f"✅ Reminders {status}")
        
        if self.settings['reminder_enabled']:
            self.start_reminder_scheduler()
        else:
            schedule.clear()
            print("⏹️ Reminder scheduler stopped")
        
        self.save_settings()
    
    def set_reminder_time(self):
        """Set the daily reminder time."""
        print("\n⏰ SET REMINDER TIME")
        print("Enter time in 24-hour format (HH:MM)")
        print("Examples: 09:00, 20:30, 14:15")
        
        while True:
            time_input = input("Reminder time: ").strip()
            
            try:
                # Validate time format
                datetime.strptime(time_input, '%H:%M')
                self.settings['reminder_time'] = time_input
                print(f"✅ Reminder time set to {time_input}")
                
                # Restart scheduler with new time
                if self.settings['reminder_enabled']:
                    self.start_reminder_scheduler()
                
                self.save_settings()
                break
                
            except ValueError:
                print("❌ Invalid time format. Use HH:MM (24-hour format)")
    
    def set_reminder_message(self):
        """Set custom reminder message."""
        print("\n💭 SET REMINDER MESSAGE")
        print("Current message:", self.settings['reminder_message'])
        
        new_message = input("New reminder message: ").strip()
        
        if new_message:
            self.settings['reminder_message'] = new_message
            print(f"✅ Reminder message updated")
            self.save_settings()
        else:
            print("❌ Message cannot be empty")
    
    def test_reminder(self):
        """Test the reminder notification immediately."""
        print("\n🧪 TESTING REMINDER...")
        self.display_reminder_notification()
        print("✅ Test reminder sent!")
    
    def display_main_menu(self):
        """Display main menu options with reminder status."""
        print("\n" + "="*65)
        print("🌟 ADAPTIVE EMOTION-BASED PRODUCTIVITY ASSISTANT 🌟")
        
        # Show reminder status
        if self.settings['reminder_enabled']:
            print(f"                    [Reminders: ⏰ {self.settings['reminder_time']}]")
        else:
            print(f"                    [Reminders: ❌ Disabled]")
        
        print("="*65)
        print("Choose an option:")
        print("  1 - Log today's mood 📝")
        print("  2 - View mood history 📊")
        print("  3 - View mood trends (graph) 📈")
        print("  4 - View mood frequency chart 🍕")
        print("  5 - Analyze weekday patterns 📅")
        print("  6 - Get personalized recommendations 💡")
        print("  7 - View mood statistics 📊")
        print("  8 - Generate sample data 🧪")
        print("  9 - Configure reminders ⏰")
        print(" 10 - Export text report 📄")
        print("  Q - Quit")
        print("="*65)
        
        # Show streak and reminder info
        streak = self.calculate_streak()
        if streak > 0:
            print(f"🔥 Current streak: {streak} days")
        
        if self.has_logged_today():
            print("✅ You've logged your mood today!")
        else:
            print("❓ Haven't logged your mood today yet")
    
    # [Include all your existing methods from the command-line version here]
    # analyze_sentiment, generate_sample_data, log_mood, etc.
    # I'm showing just the new reminder functionality to keep this focused
    
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
            print(f"⚠️ Sentiment analysis error: {e}")
            return 0.0, "Neutral"
    
    def log_mood(self):
        """Main mood logging function."""
        current_date = datetime.now().date()
        
        # Check if already logged today
        if self.has_logged_today():
            print(f"\n⚠️ You already logged your mood for {current_date}")
            print("Each day allows only one mood entry to maintain data integrity.")
            
            while True:
                choice = input("Would you like to update today's entry? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    self.update_mood_entry(current_date)
                    return
                elif choice in ['n', 'no']:
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
            return
        
        # Continue with normal mood logging...
        self.display_mood_scale()
        mood_score, mood_label = self.get_mood_input()
        
        if mood_score is None:
            return
        
        note = self.get_note_input()
        sentiment_score, sentiment_label = self.analyze_sentiment(note)
        
        # Save the entry
        self.save_mood_entry(mood_score, mood_label, note, sentiment_score, sentiment_label)
        
        # Update streak counter
        streak = self.calculate_streak()
        print(f"\n🎉 Great job! Current streak: {streak} days")
        
        # Reload data to include new entry
        self.load_data()
    
    def display_mood_scale(self):
        """Display the mood scale options."""
        print("\n" + "="*50)
        print("🎯 MOOD SCALE")
        print("="*50)
        for score, label in self.mood_scale.items():
            print(f"  {score} - {label}")
        print("="*50)
    
    def get_mood_input(self):
        """Get and validate mood input from user."""
        while True:
            try:
                print("\nEnter your mood (1-5) or 'q' to go back:")
                user_input = input("Your choice: ").strip().lower()
                
                if user_input == 'q':
                    return None, None
                
                mood_score = int(user_input)
                
                if mood_score in self.mood_scale:
                    mood_label = self.mood_scale[mood_score]
                    return mood_score, mood_label
                else:
                    print("❌ Please enter a number between 1 and 5.")
                    
            except ValueError:
                print("❌ Please enter a valid number (1-5) or 'q' to go back.")
    
    def get_note_input(self):
        """Get optional note from user."""
        print("\n💭 Add a note about your mood (optional, press Enter to skip):")
        note = input("Note: ").strip()
        return note
    
    def save_mood_entry(self, mood_score, mood_label, note, sentiment_score, sentiment_label):
        """Save mood entry to CSV file."""
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        mood_entry = [current_date, mood_score, mood_label, note, sentiment_score, sentiment_label, current_timestamp]
        
        try:
            with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(mood_entry)
            
            print(f"\n✅ Mood entry saved successfully!")
            print(f"   Date: {current_date}")
            print(f"   Mood: {mood_label}")
            print(f"   Note: {note if note else 'No note added'}")
            
        except Exception as e:
            print(f"❌ Error saving mood entry: {e}")
    
    def update_mood_entry(self, date):
        """Update existing mood entry for a given date."""
        # Implementation similar to your existing code
        pass
    
    def run(self):
        """Main application loop with reminder functionality."""
        print("\n🌟 Welcome to your Adaptive Emotion-Based Productivity Assistant!")
        print("⏰ Daily reminders are now active to help you maintain your mood tracking habit!")
        
        while True:
            try:
                self.display_main_menu()
                choice = input("\nYour choice: ").strip().lower()
                
                if choice == '1':
                    self.log_mood()
                elif choice == '2':
                    # Add your existing view_history method
                    pass
                elif choice == '3':
                    # Add your existing create_mood_trends_graph method
                    pass
                elif choice == '4':
                    # Add your existing create_mood_frequency_chart method
                    pass
                elif choice == '5':
                    # Add your existing analyze_weekday_patterns method
                    pass
                elif choice == '6':
                    # Add your existing get_personalized_recommendations method
                    pass
                elif choice == '7':
                    # Add your existing view_statistics method
                    pass
                elif choice == '8':
                    # Add your existing generate_sample_data method
                    pass
                elif choice == '9':
                    self.configure_reminders()
                elif choice == '10':
                    # Add your existing export_text_report method
                    pass
                elif choice in ['q', 'quit']:
                    print("\n👋 Thank you for using the Mood Tracker!")
                    print("💡 Your daily reminders will continue running in the background!")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-10 or 'Q' to quit.")
                
                # Pause before showing menu again
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using the Mood Tracker! Have a great day!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again.")

def main():
    """Main function with dependency checking."""
    
    # Check for required libraries
    missing_libs = []
    
    required_imports = [
        ('matplotlib.pyplot', 'matplotlib'),
        ('pandas', 'pandas'),
        ('textblob', 'textblob'),
        ('schedule', 'schedule')
    ]
    
    for import_name, lib_name in required_imports:
        try:
            __import__(import_name)
        except ImportError:
            missing_libs.append(lib_name)
    
    if missing_libs:
        print("📦 Missing required libraries. Please install them:")
        for lib in missing_libs:
            print(f"   pip3 install {lib}")
        print("\nThen run the program again!")
        return
    
    # Run the application
    print("🚀 Starting Adaptive Emotion-Based Productivity Assistant with Reminders...")
    tracker = MoodTrackerWithReminders()
    tracker.run()

if __name__ == "__main__":
    main()