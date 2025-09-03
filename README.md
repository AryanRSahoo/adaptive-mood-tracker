# Adaptive Emotion-Based Productivity Assistant

> An AI-powered mood tracking and productivity optimization system that analyzes emotional patterns to provide personalized recommendations for enhanced daily performance.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Versions](#project-versions)
- [AI & ML Components](#ai--ml-components)
- [Data Analytics](#data-analytics)
- [Screenshots](#screenshots)
- [Architecture](#architecture)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Overview

The **Adaptive Emotion-Based Productivity Assistant** is a comprehensive Python application that combines emotional intelligence with data science to help users optimize their daily productivity. By tracking mood patterns and analyzing emotional trends, the system provides AI-powered insights and personalized recommendations.

### Project Goals

- **Data-Driven Insights**: Transform subjective emotional data into actionable analytics
- **AI Integration**: Leverage natural language processing for sentiment analysis
- **Pattern Recognition**: Identify correlations between emotions and productivity
- **User Experience**: Provide multiple interfaces (CLI, GUI, PDF reports) for different use cases
- **Professional Development**: Demonstrate full-stack development capabilities

## Features

### Core Functionality
- **Daily Mood Logging** with sentiment analysis
- **Intelligent Pattern Detection** across time periods
- **Personalized Productivity Recommendations** based on emotional state
- **Automated Daily Reminders** with customizable scheduling
- **Comprehensive Analytics Dashboard** with multiple visualization types
- **Professional PDF Report Generation** with embedded charts

### Advanced Analytics
- **Temporal Trend Analysis** - Track mood changes over time
- **Weekday Pattern Recognition** - Identify which days are typically better/worse
- **Sentiment Analysis Integration** - NLP-powered emotion classification
- **Statistical Insights** - Mean, standard deviation, distribution analysis
- **Streak Tracking** - Motivation through consistent logging habits

### Multiple Interface Options
1. **Command Line Interface** - Full-featured analytics and data management
2. **Light Theme GUI** - Professional desktop application
3. **Dark Theme GUI** - Modern, high-contrast interface
4. **PDF Reports** - Exportable insights for sharing and archiving

## Technology Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Data visualization and charting
- **NumPy** - Numerical computing

### AI & Machine Learning
- **TextBlob** - Natural language processing and sentiment analysis

### User Interface & Experience
- **Tkinter** - Desktop GUI development
- **Schedule** - Automated task scheduling
- **FPDF2** - PDF generation and reporting

### Data Management
- **CSV** - Lightweight data storage
- **JSON** - Configuration management
- **datetime** - Temporal data handling

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/[YOUR_USERNAME]/adaptive-mood-tracker.git
cd adaptive-mood-tracker

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/mood_tracker_professional.py
```

### Dependencies

```
pandas>=1.5.0
matplotlib>=3.6.0
textblob>=0.17.1
fpdf2>=2.7.0
schedule>=1.2.0
numpy>=1.24.0
Pillow>=9.5.0
```

## Usage

### Command Line Interface
```bash
python src/mood_tracker.py
```
Features: Complete analytics, data export, advanced pattern analysis

### GUI Applications
```bash
# Light theme professional GUI
python src/mood_tracker_gui.py

# Dark theme modern GUI  
python src/mood_tracker_professional.py
```

### Quick Start Example
```python
from mood_tracker import MoodTracker

# Initialize tracker
tracker = MoodTracker()

# Generate sample data for testing
tracker.generate_sample_data()

# View analytics
tracker.view_statistics()
tracker.create_mood_trends_graph()
```

## Project Versions

### 1. Command Line Interface (`src/mood_tracker.py`)
**Purpose**: Maximum functionality and data analysis capabilities
- Comprehensive menu system
- Advanced statistical analysis
- Testing mode for development
- Text report generation
- Full terminal-based workflow

### 2. Professional Light GUI (`src/mood_tracker_gui.py`)
**Purpose**: Clean, professional presentation
- Tab-based navigation interface
- Real-time chart updates
- Integrated analytics dashboard
- Perfect for demonstrations and portfolios

### 3. Modern Dark GUI (`src/mood_tracker_professional.py`)
**Purpose**: Enhanced user experience
- High-contrast dark theme design
- Professional enterprise appearance
- Advanced visual hierarchy
- Optimized for daily use

## AI & ML Components

### Sentiment Analysis Pipeline
```python
def analyze_sentiment(self, text):
    """
    Analyzes emotional tone of user notes using TextBlob NLP.
    
    Returns:
        sentiment_score (float): Polarity score (-1 to 1)
        sentiment_label (str): Positive/Negative/Neutral classification
    """
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    
    if sentiment_score > 0.1:
        return sentiment_score, "Positive"
    elif sentiment_score < -0.1:
        return sentiment_score, "Negative"
    else:
        return sentiment_score, "Neutral"
```

### Pattern Recognition
- **Temporal Correlation Analysis**: Identifies mood patterns across different time periods
- **Weekday Classification**: Approach to categorize optimal/challenging days
- **Trend Detection**: Statistical analysis of mood trajectories over time

### Recommendation Engine
Algorithms generate context-aware productivity advice based on:
- Current emotional state
- Historical mood patterns
- Weekday analysis
- Recent trend direction

## Data Analytics

### Statistical Measures
- **Central Tendency**: Mean, median mood scores
- **Variability**: Standard deviation, mood range analysis
- **Distribution**: Frequency analysis across mood categories
- **Temporal**: Streak calculation, trend analysis

### Visualization Types
1. **Line Charts**: Mood trends over time with trend lines
2. **Pie Charts**: Mood distribution percentages
3. **Bar Charts**: Weekday pattern analysis
4. **Statistical Dashboards**: Key metrics and KPIs

### Data Storage Schema
```csv
Date,Mood_Score,Mood_Label,Note,Sentiment_Score,Sentiment_Label,Timestamp
2024-08-31,4,Happy,Great productive day!,0.6,Positive,2024-08-31 20:15:30
```

## Screenshots

### Dark Theme GUI
![Dark GUI Overview](docs/screenshots/dark_gui_overview.png)

### Analytics Dashboard
![Analytics Charts](docs/screenshots/analytics_dashboard.png)

### Light GUI Interface
![Light GUI Interface](docs/screenshots/light_gui_interface.png)

### Command Line Interface
![CLI Interface](docs/screenshots/cli_interface.png)

## Architecture

### System Design
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │────│  Data Processing │────│   AI Analysis   │
│  (Mood + Note)  │    │   (Validation)   │    │ (Sentiment+ML)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Storage  │    │   Visualization  │    │ Recommendations │
│   (CSV + JSON)  │    │ (Charts + GUI)   │    │   (ML-driven)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Design Patterns
- **MVC Architecture**: Clean separation of data, logic, and presentation
- **Observer Pattern**: Real-time UI updates when data changes
- **Strategy Pattern**: Multiple interface implementations
- **Factory Pattern**: Chart generation system

### Data Flow
1. **Input Layer**: Multiple interfaces collect mood data
2. **Processing Layer**: Data validation, sentiment analysis, pattern detection
3. **Storage Layer**: CSV for mood data, JSON for configuration
4. **Analysis Layer**: Statistical computation, AI-powered insights
5. **Presentation Layer**: GUI, CLI, and PDF output

## Future Enhancements

### Planned Features
- **Spotify API Integration** - Mood-based playlist recommendations
- **Machine Learning Models** - Advanced pattern prediction
- **Web Application** - Flask/Django implementation
- **Mobile App** - Cross-platform mood tracking
- **Cloud Sync** - Multi-device data synchronization
- **Advanced Analytics** - Correlation with external factors

### Technical Improvements
- **Database Integration** - PostgreSQL/SQLite migration
- **RESTful API** - Backend service architecture
- **Real-time Notifications** - System-level reminder integration
- **Data Export Options** - JSON, Excel, CSV formats
- **Backup & Recovery** - Automated data protection

## Development & Testing

### Testing the Application
```bash
# Generate sample data for testing
python src/mood_tracker.py
# Choose option 8: Generate sample data

# Test all visualization features
python src/mood_tracker_gui.py
# Navigate through all tabs to verify functionality
```

### Code Quality
- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Robust exception management
- **Code Organization**: Modular, reusable components

## Educational Value

### Computer Science Concepts Demonstrated
- **Data Structures**: Efficient data manipulation with pandas
- **Algorithms**: Pattern recognition and statistical analysis
- **Human-Computer Interaction**: Multiple interface paradigms
- **Software Engineering**: Clean architecture and design patterns
- **Machine Learning**: NLP integration and sentiment analysis
- **Data Visualization**: Professional chart generation and presentation

### Skills Showcased
- Full-stack Python development
- AI/ML integration and deployment
- Data science and analytics
- User interface design (CLI and GUI)
- Software architecture and design patterns
- Technical documentation and presentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**[ARYAN_RYAN_SAHOO]**
- GitHub: [@[AryanRSahoo]](https://github.com/[YOUR_GITHUB_USERNAME])
- LinkedIn: [Aryan Sahoo](https://linkedin.com/in/[YOUR_LINKEDIN])
- Email: [aryansahoouni@gmailcom]

## Acknowledgments

- **TextBlob** for natural language processing capabilities
- **Matplotlib** for powerful data visualization
- **Pandas** for efficient data manipulation
- **Python Community** for excellent libraries and documentation

---

**Built for emotional intelligence and productivity optimization**

**## 📘 Project Article
I’ve written a detailed technical + personal write-up about this project on Medium.  
👉 [Read the full story here](https://medium.com/@aryansahoouni/building-an-ai-powered-emotion-aware-productivity-assistant-d8b86f16d46d)**
