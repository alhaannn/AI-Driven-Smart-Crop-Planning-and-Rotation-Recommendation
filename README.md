# 🌾 AI-Driven Smart Crop Planning and Rotation Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> An intelligent agricultural management platform that leverages AI to optimize crop planning, rotation strategies, and farm management based on soil health, historical data, and climate patterns.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## 🌟 Overview

The **Smart Crop Planning System** is a comprehensive web-based agricultural management platform designed specifically for Indian farmers and agricultural professionals. It combines traditional farming knowledge with modern AI/ML techniques to provide data-driven insights for sustainable and profitable farming.

### Why This Project?

- **🎯 Problem:** Farmers often struggle with crop rotation planning, soil health management, and financial tracking
- **💡 Solution:** AI-powered recommendations based on scientific data and historical performance
- **🌍 Impact:** Increased yields, improved soil health, reduced costs, and sustainable farming practices

### Target Users

- 👨‍🌾 **Farmers** - Individual farmers managing small to medium-sized farms
- 🏢 **Agricultural Consultants** - Professionals advising multiple clients
- 🎓 **Agricultural Students** - Learning crop management best practices
- 🏛️ **Government Agencies** - Monitoring and supporting agricultural development

---

## ✨ Key Features

### 🌾 Field Management
- **Multi-field tracking** - Manage unlimited farm fields
- **Detailed field profiles** - Location, size (acres), soil type, irrigation method
- **Crop history** - Complete historical records with yields and dates
- **Visual analytics** - Charts and graphs for quick insights

### 🧪 Soil Analysis & Health Monitoring
- **NPK tracking** - Monitor Nitrogen, Phosphorus, Potassium levels
- **pH monitoring** - Track soil acidity/alkalinity
- **Organic matter analysis** - Measure soil organic content
- **Automated recommendations** - AI-generated fertilizer suggestions
- **Trend analysis** - Historical soil health patterns

### 🤖 AI-Powered Crop Rotation
- **Intelligent recommendations** - ML-based crop succession planning
- **Multi-year planning** - 2-10 year rotation cycles
- **Goal-oriented optimization** - Maximize yield, soil health, pest control, or profit
- **Compatibility scoring** - Scientific crop compatibility analysis
- **Benefit tracking** - Expected vs. actual improvement monitoring
- **Nitrogen management** - Automatic legume inclusion for soil health

### 📅 Agricultural Calendar
- **Activity scheduling** - Plan planting, fertilizing, harvesting
- **Reminders** - Upcoming and overdue task tracking
- **Weather integration** - Log and track weather patterns
- **Season management** - Kharif, Rabi, Zaid season support

### 📊 Analytics & Insights
- **Financial tracking** - Income, expenses, subsidies, loans
- **Profit/loss analysis** - Detailed financial reports
- **Yield predictions** - AI-based harvest forecasting
- **Performance metrics** - KPIs and trend analysis
- **Visual dashboards** - Interactive charts using Chart.js

### 📄 Reports & Export
- **PDF reports** - Professional field and financial reports
- **CSV/Excel export** - Data portability for analysis
- **Bulk exports** - All data types in one click
- **Print-friendly** - Optimized for physical documentation
- **Bank-ready formats** - Loan application support

### 🇮🇳 India-Specific Features
- **Indian crops** - Rice, Wheat, Cotton, Sugarcane, etc.
- **Indian seasons** - Kharif, Rabi, Zaid
- **Currency in INR (₹)** - All financial data in Indian Rupees
- **Local soil types** - Clay, Loam, Sandy, Black Cotton
- **Acres measurement** - Field sizes in acres
- **Government schemes** - Subsidy tracking support

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Django 6.0.2
- **Language:** Python 3.8+
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **PDF Generation:** ReportLab
- **Excel Export:** openpyxl, xlsxwriter
- **AI/ML:** Scikit-learn (planned)

### Frontend
- **Template Engine:** Django Templates
- **CSS Framework:** Custom CSS (Vanilla)
- **Charts:** Chart.js
- **Icons:** Emoji-based (lightweight)
- **Responsive:** Mobile-friendly design

### Development Tools
- **Version Control:** Git
- **Package Management:** pip
- **Code Style:** PEP 8
- **Documentation:** Markdown

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
*Main dashboard with field statistics and quick actions*

### AI Rotation Generator
![Rotation](docs/screenshots/rotation.png)
*AI-powered crop rotation planning interface*

### Soil Analysis
![Soil](docs/screenshots/soil.png)
*Soil health monitoring and NPK tracking*

### Analytics
![Analytics](docs/screenshots/analytics.png)
*Financial insights and performance metrics*

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Virtual environment tool (venv/virtualenv)

### Step 1: Clone the Repository

```bash
git clone https://github.com/alhaannn/AI-Driven-Smart-Crop-Planning-and-Rotation-Recommendation.git
cd AI-Driven-Smart-Crop-Planning-and-Rotation-Recommendation
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Main Dependencies:**
```
Django==6.0.2
reportlab==4.0.9
openpyxl==3.1.2
xlsxwriter==3.1.9
Pillow==10.2.0
python-dotenv==1.0.0
```

### Step 4: Configure Environment Variables

**⚠️ IMPORTANT: You must set up your environment variables before running the project.**

1. Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. Open `.env` file and configure your settings:

```env
# Required: Generate a new secret key (Never use the default in production!)
SECRET_KEY=your-unique-secret-key-here

# Development settings
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: Configure other settings as needed
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

**🔐 Security Notes:**
- **Never commit your `.env` file to Git** (already in `.gitignore`)
- **Generate a strong SECRET_KEY** - You can use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- For production, set `DEBUG=False` and configure proper `ALLOWED_HOSTS`

### Step 5: Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### Step 7: Load Demo Data (Optional)

```bash
python manage.py populate_demo
```

This creates sample fields, soil analyses, and crop histories for testing.

---

## 🎯 Quick Start

### Start Development Server

```bash
python manage.py runserver
```

Access the application at: **http://localhost:8000/**

### Default Admin Access

- **URL:** http://localhost:8000/admin/
- **Username:** (created during superuser setup)
- **Password:** (created during superuser setup)

### First Steps

1. **Add a Field** - Go to Fields → Add Field
2. **Record Soil Analysis** - Soil → Add Analysis
3. **Generate AI Plan** - Rotation → Generate AI Plan
4. **View Analytics** - Analytics → Dashboard

---

## 📖 Usage Guide

### For Farmers

#### 1. Managing Fields

```
Navigate to: Fields → All Fields → Add Field

Required Information:
- Field name (e.g., "North Field")
- Size in acres
- Location (village/district)
- Soil type (Clay/Loam/Sandy/Black Cotton)
- Irrigation method (Drip/Sprinkler/Flood/Rain-fed)
```

#### 2. Recording Soil Analysis

```
Navigate to: Soil Analysis → Add Analysis

Required Values:
- Select field
- Analysis date
- pH level (5.0 - 9.0)
- Nitrogen (PPM)
- Phosphorus (PPM)
- Potassium (PPM)
- Organic matter (%)
```

**The system automatically generates fertilizer recommendations!**

#### 3. Generating Rotation Plans

```
Navigate to: Rotation → Generate AI Plan

Configuration:
- Select field
- Duration (2-10 years)
- Primary goal:
  • Yield Maximization
  • Soil Health
  • Pest Control
  • Profit Maximization

AI analyzes:
✓ Field history
✓ Soil conditions
✓ Crop compatibility
✓ Seasonal factors
✓ Nitrogen management
```

#### 4. Tracking Finances

```
Navigate to: Analytics → Financial Records

Track:
- Income (crop sales)
- Expenses (seeds, fertilizer, labor)
- Subsidies
- Loans
- Other transactions

View:
- Profit/Loss statements
- Category-wise breakdown
- Trend analysis
```

#### 5. Exporting Data

```
Navigate to: Reports → Dashboard

Available Exports:
📄 PDF Reports:
  - Field summary
  - Financial report
  - Farm overview

📊 Excel/CSV:
  - All fields data
  - Crop history
  - Soil analyses
  - Financial records
```

### For Developers

#### Project Structure

```
smart-crop-planner/
│
├── smart_crop_planner/      # Main project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Root URL routing
│   └── views.py              # Homepage view
│
├── fields/                   # Field management app
│   ├── models.py             # Field, CropHistory models
│   ├── views.py              # CRUD views
│   ├── forms.py              # Django forms
│   └── management/commands/  # Demo data scripts
│
├── soil/                     # Soil analysis app
│   ├── models.py             # SoilAnalysis, Recommendation
│   ├── views.py              # Analysis & recommendation views
│   └── utils.py              # Recommendation engine
│
├── calendar_weather/         # Calendar & weather app
│   ├── models.py             # CalendarEvent, WeatherData
│   └── views.py              # Calendar management
│
├── rotation/                 # Crop rotation app
│   ├── models.py             # RotationPlan, Sequence, Benefit
│   ├── views.py              # Plan CRUD operations
│   └── utils.py              # AI rotation engine
│
├── analytics/                # Analytics & financial app
│   ├── models.py             # FinancialRecord
│   ├── views.py              # Dashboard & insights
│   └── utils.py              # Calculation utilities
│
├── reports/                  # Reports & export app
│   ├── views.py              # Export endpoints
│   ├── pdf_utils.py          # PDF generation
│   └── csv_utils.py          # CSV/Excel generation
│
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   ├── home.html             # Dashboard
│   ├── fields/               # Field templates
│   ├── soil/                 # Soil templates
│   ├── rotation/             # Rotation templates
│   └── ...
│
├── static/                   # Static assets
│   └── css/style.css         # Main stylesheet
│
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

#### Database Models

**Field Model:**
```python
class Field(models.Model):
    name = CharField(max_length=200)
    location = CharField(max_length=300)
    size_acres = DecimalField(max_digits=10, decimal_places=2)
    soil_type = CharField(choices=SOIL_TYPES)
    irrigation_type = CharField(choices=IRRIGATION_TYPES)
    notes = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
```

**SoilAnalysis Model:**
```python
class SoilAnalysis(models.Model):
    field = ForeignKey(Field, related_name='soil_analyses')
    analysis_date = DateField()
    ph_level = DecimalField(max_digits=4, decimal_places=2)
    nitrogen_ppm = DecimalField(max_digits=8, decimal_places=2)
    phosphorus_ppm = DecimalField(max_digits=8, decimal_places=2)
    potassium_ppm = DecimalField(max_digits=8, decimal_places=2)
    organic_matter = DecimalField(max_digits=5, decimal_places=2)
```

**RotationPlan Model:**
```python
class RotationPlan(models.Model):
    field = ForeignKey(Field)
    name = CharField(max_length=200)
    start_year = IntegerField()
    duration_years = IntegerField()
    status = CharField(choices=STATUS_CHOICES)
    primary_goal = CharField(choices=GOAL_CHOICES)
    ai_generated = BooleanField(default=False)
    confidence_score = IntegerField()
```

#### Key Algorithms

**1. Crop Rotation Scoring Algorithm**

The AI engine scores each crop (0-100) based on:

```python
def calculate_crop_rotation_score(crop_name, crop_data, field, 
                                  last_crop, recent_crops, 
                                  soil_analysis, primary_goal):
    score = 50  # Base score
    
    # Factor 1: Rotation compatibility (30 points)
    if last_crop in crop_data['good_predecessors']:
        score += 20
    elif last_crop in crop_data['poor_predecessors']:
        score -= 25
    
    # Factor 2: Diversification (15 points)
    if crop_name not in recent_crops[:3]:
        score += 15
    
    # Factor 3: Soil compatibility (20 points)
    ph_min, ph_max = crop_data['ph_range']
    if ph_min <= soil_ph <= ph_max:
        score += 15
    
    # Factor 4: Goal alignment (20 points)
    if primary_goal == 'yield_max':
        if avg_yield > 5000:
            score += 15
    elif primary_goal == 'soil_health':
        if 'soil_health' in benefits:
            score += 20
    
    # Factor 5: Nitrogen fixing bonus (10 points)
    if crop_data['nitrogen_requirement'] == 'nitrogen_fixing':
        score += 10
    
    return max(10, min(95, score))
```

**2. Fertilizer Recommendation Engine**

```python
def generate_fertilizer_recommendations(soil_analysis):
    recommendations = []
    
    # Nitrogen recommendation
    if soil_analysis.nitrogen_ppm < 30:
        recommendations.append({
            'nutrient': 'Nitrogen',
            'recommendation': 'Apply urea 50-60 kg/acre',
            'priority': 'high'
        })
    
    # Phosphorus recommendation
    if soil_analysis.phosphorus_ppm < 20:
        recommendations.append({
            'nutrient': 'Phosphorus',
            'recommendation': 'Apply DAP 30-40 kg/acre',
            'priority': 'high'
        })
    
    # Similar logic for other nutrients...
    
    return recommendations
```

---

## 🔌 API Documentation

### REST Endpoints (If Implemented)

Currently, the system uses Django views. To add REST API:

```bash
pip install djangorestframework
```

Example API endpoints structure:

```
GET    /api/fields/              # List all fields
POST   /api/fields/              # Create field
GET    /api/fields/{id}/         # Get field details
PUT    /api/fields/{id}/         # Update field
DELETE /api/fields/{id}/         # Delete field

GET    /api/soil-analyses/       # List soil analyses
POST   /api/soil-analyses/       # Create analysis

GET    /api/rotation-plans/      # List rotation plans
POST   /api/rotation-plans/generate/  # Generate AI plan
```

---

## 👨‍💻 Development

### Running Tests

```bash
python manage.py test
```

### Code Style

Follow PEP 8 guidelines:

```bash
pip install flake8
flake8 .
```

### Adding a New Feature

1. Create a new Django app:
```bash
python manage.py startapp myfeature
```

2. Add to `INSTALLED_APPS` in `settings.py`

3. Create models in `models.py`

4. Create migrations:
```bash
python manage.py makemigrations myfeature
python manage.py migrate
```

5. Create views, URLs, and templates

6. Test thoroughly

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate app_name previous_migration_name
```

---

## 🌐 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure static file serving
- [ ] Set up HTTPS/SSL
- [ ] Configure email backend
- [ ] Set up backup system
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Enable security features

### Deploy to Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### Deploy to AWS/DigitalOcean

1. Set up Ubuntu server
2. Install Python, PostgreSQL, Nginx
3. Clone repository
4. Set up virtual environment
5. Configure Gunicorn
6. Configure Nginx as reverse proxy
7. Set up SSL with Let's Encrypt
8. Configure systemd for auto-restart

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Contribution Guidelines

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Code of Conduct

- Be respectful and inclusive
- Follow code style guidelines
- Write clear commit messages
- Add tests for new features
- Update documentation

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🌐 Translations (Hindi, regional languages)
- 🎨 UI/UX enhancements
- 🧪 Test coverage
- 📊 More crop data
- 🤖 ML model improvements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Smart Crop Planner Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
```

---

## 🆘 Support

### Getting Help

- 📧 **Email:** support@smartcropplanner.com
- 💬 **Discord:** [Join our community](https://discord.gg/smartcropplanner)
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/smart-crop-planner/issues)
- 📖 **Documentation:** [Wiki](https://github.com/yourusername/smart-crop-planner/wiki)

### FAQ

**Q: Can I use this for commercial purposes?**  
A: Yes, the MIT license allows commercial use.

**Q: Does it work offline?**  
A: The local version works offline. Cloud features require internet.

**Q: Is my data secure?**  
A: Yes, all data is stored locally. We don't collect or share your data.

**Q: Can I add custom crops?**  
A: Yes, you can extend the crop database in `rotation/utils.py`.

**Q: Does it support multiple languages?**  
A: Currently English. Hindi and regional languages are planned.

---

## 🙏 Acknowledgments

- **Indian Council of Agricultural Research (ICAR)** - Crop data
- **Chart.js** - Beautiful charts
- **Django Community** - Amazing framework
- **ReportLab** - PDF generation
- **All Contributors** - Thank you!

---

## 🗺️ Roadmap

### Version 2.0 (Planned)

- [ ] Mobile app (Android/iOS)
- [ ] Real-time weather API integration
- [ ] Advanced ML yield prediction
- [ ] Multi-user support with roles
- [ ] Marketplace integration
- [ ] Government scheme notifications
- [ ] Hindi & regional language support
- [ ] Crop disease detection (Image AI)
- [ ] Market price tracking
- [ ] Community forum

---

## 📊 Project Stats

- **Lines of Code:** ~15,000+
- **Django Apps:** 7
- **Models:** 20+
- **Views:** 80+
- **Templates:** 50+
- **Crops in Database:** 10+
- **Active Users:** Growing!

---

## 🌾 Happy Farming! 🇮🇳

**Made with ❤️ for Indian Farmers**

---

<p align="center">
  <a href="https://github.com/yourusername/smart-crop-planner">⭐ Star this repo</a> •
  <a href="https://github.com/yourusername/smart-crop-planner/issues">🐛 Report Bug</a> •
  <a href="https://github.com/yourusername/smart-crop-planner/issues">✨ Request Feature</a>
</p>

<p align="center">
  If this project helped you, please consider giving it a ⭐ on GitHub!
</p>
