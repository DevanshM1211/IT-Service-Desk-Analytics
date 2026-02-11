# 📊 IT Service Desk Analytics Dashboard

> A comprehensive data analytics portfolio project demonstrating end-to-end data pipeline, exploratory analysis, and business intelligence capabilities using Python and Power BI.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)

---

## 🎯 Business Problem

IT Service Desk organizations struggle with:
- **Lack of visibility** into ticket resolution performance
- **SLA non-compliance** without clear visibility into root causes
- **Inefficient resource allocation** across teams and ticket categories
- **Reactive problem-solving** without trend analysis or forecasting
- **Missing KPIs** for executive reporting and decision-making

**Goal:** Build an analytics solution to monitor service desk performance, identify bottlenecks, and provide actionable insights for operational improvements.

---

## 📈 Project Overview

This end-to-end analytics project demonstrates:

✅ **Data Engineering:** Generating, cleaning, and transforming 2,000+ ticket records  
✅ **Feature Engineering:** Creating business-relevant derived features  
✅ **Exploratory Analysis:** Answering 4 key business questions with statistical rigor  
✅ **Data Visualization:** Professional matplotlib and Power BI visualizations  
✅ **Business Intelligence:** KPI calculation and executive dashboard design  

### Key Deliverables
- 📊 **Exploratory Analysis:** 4 CSV summary tables with business insights
- 📈 **Professional Charts:** 4 matplotlib visualizations for presentations
- 🔄 **Data Pipeline:** Complete ETL workflow from raw to Power BI-ready
- 📱 **Power BI Dataset:** Clean, optimized CSV for dashboard import
- 📋 **Dashboard Design:** Comprehensive specification for executive dashboard
- 🐍 **Production Code:** Reusable Python modules with clear documentation

---

## 📊 Dataset Overview

**Source:** Synthetic IT Service Desk ticket data (realistic simulation)  
**Time Period:** April 1 - August 1, 2025  
**Records:** 2,000 service desk tickets  
**Features:** 16 engineered features from original 9 columns

### Data Attributes
| Field | Type | Description |
|-------|------|-------------|
| Ticket_ID | String | Unique ticket identifier (TICKET-XXXXX) |
| Created_Date | DateTime | When ticket was created |
| Resolved_Date | DateTime | When ticket was resolved |
| Priority | Categorical | Critical, High, Medium, Low |
| Category | Categorical | Network, Hardware, Software, Access, Security, Email |
| Assigned_Team | Categorical | Infrastructure, ServiceDesk, CyberSecurity, Applications |
| Resolution_Hours | Float | Hours to resolve (0.5 - 168) |
| SLA_Breached | Boolean | Whether SLA target was exceeded |
| Ticket_Age_Hours | Float | Hours since creation (as of Aug 1, 2025) |

---

## 🎯 KPIs Tracked

### Primary KPIs
- **Total Tickets:** 2,000 (Apr-Jul 2025)
- **SLA Compliance Rate:** 72.3% (above industry average of 70%)
- **Average Resolution Time:** 57.9 hours (2.41 days)
- **Breached Tickets:** 554 (27.7% breach rate)
- **Critical Tickets:** 210 (10.5% of volume)

### Secondary Metrics by Dimension

**By Priority Level:**
- Critical: 3.03 avg hours, 32.86% breach rate
- High: 17.89 avg hours, 22.83% breach rate
- Medium: 61.87 avg hours, 31.95% breach rate
- Low: 99.27 avg hours, 23.48% breach rate

**By Category (Breach Rate):**
- Software: 30.42% (highest)
- Access: 28.91%
- Email: 28.01%
- Network: 27.81%
- Security: 26.04%
- Hardware: 25.41% (lowest)

**By Team (Avg Resolution):**
- ServiceDesk: 60.15 hours (slowest)
- CyberSecurity: 58.05 hours
- Infrastructure: 56.83 hours
- Applications: 56.32 hours (fastest)

---

## 🛠️ Tools & Technologies Used

### Data Processing & Analysis
- **Python 3.8+:** Core programming language
- **pandas:** Data manipulation, cleaning, aggregation
- **NumPy:** Numerical computations
- **datetime:** Time-based feature engineering

### Data Visualization
- **Matplotlib:** Professional business charts
- **Plotly:** Interactive visualizations (optional)

### Business Intelligence
- **Power BI:** Executive dashboard development
- **CSV Export:** Optimized data format for BI tools

### Development & Collaboration
- **Git/GitHub:** Version control and portfolio showcase
- **Virtual Environment:** Python dependency isolation
- **Jupyter Notebooks:** Interactive exploratory analysis

---

## 🔍 Key Insights & Findings

### 1. **SLA Compliance Gaps by Priority**
- Critical tickets have 32.86% breach rate (highest risk)
- Medium-priority tickets also breach frequently (31.95%)
- Suggests need for better resource allocation to critical tickets

### 2. **Category Performance Disparities**
- Software category requires significant improvement (30.42% breach)
- Hardware category performs best (25.41% breach)
- 5% difference suggests opportunity for process improvement transfer

### 3. **Team Performance Variation**
- ServiceDesk team 6.8% slower than Applications team
- Creates capacity planning opportunity
- Average resolution: 56-60 hours across all teams

### 4. **Monthly Trends**
- April peak: 516 tickets (highest volume month)
- May low: 471 tickets (lowest volume month)
- Consistent ~500 tickets/month with seasonal variation

### 5. **Priority Distribution Insights**
- Medium-priority tickets dominant (39.8% of volume)
- Only 10.5% critical, suggesting effective prioritization
- Low-priority tickets are 29.6% of workload

---

## 📊 Dashboard Preview

**Executive Summary Dashboard:**
```
┌─────────────────────────────────────────────────────────────┐
│  IT SERVICE DESK ANALYTICS DASHBOARD                         │
├─────────────────────────────────────────────────────────────┤
│  [Total: 2000]  [SLA: 72.3%] [Avg: 57.9h] [Breached: 554]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  SLA Compliance Trend    │  Priority Distribution           │
│  ████████░░  74%        │  🟡 Medium: 39.8%               │
│  May      Jun      Jul  │  🔴 Low: 29.6%                  │
│                         │  🟠 High: 20.2%                 │
│                         │  🔵 Critical: 10.5%             │
├──────────────────────────┼──────────────────────────────────┤
│  Resolution by Category  │  Team Performance                │
│  Software........30.4%   │  ServiceDesk.....60.15h ⚠️      │
│  Access..........28.9%   │  CyberSecurity...58.05h         │
│  Email...........28.0%   │  Infrastructure..56.83h         │
│  Hardware........25.4%   │  Applications....56.32h ✅      │
└─────────────────────────────────────────────────────────────┘
```

[Charts saved as PNG files in `outputs/charts/`]

---

## 🚀 How to Run the Project

### Prerequisites
```bash
Python 3.8+
pip / conda
Git
```

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/DevanshM1211/IT-Service-Desk-Analytics.git
cd "IT Service Desk Analytics"
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Pipeline

**Option A: Run Complete Pipeline (Sequential)**
```bash
# 1. Generate synthetic data
python generate_data.py

# 2. Clean data
python clean_data.py

# 3. Engineer features
python engineer_features.py

# 4. Exploratory analysis
python explore_data.py

# 5. Create visualizations
python visualize_charts.py

# 6. Prepare for Power BI
python prepare_powerbi.py
```

**Option B: Run Individual Steps**
```bash
# Just clean existing data
python clean_data.py

# Just engineering features
python engineer_features.py

# Just analysis
python explore_data.py

# Just charts
python visualize_charts.py
```

### Output Files
```
data/
├── raw_service_tickets.csv              # 2,000 synthetic tickets
├── cleaned_service_tickets.csv          # After cleaning
└── engineered_service_tickets.csv       # With 16 features

outputs/
├── priority_distribution.csv            # Analysis table
├── sla_breach_by_category.csv           # Analysis table
├── resolution_time_by_team.csv          # Analysis table
├── ticket_volume_trend.csv              # Analysis table
├── powerbi_service_tickets.csv          # Power BI ready dataset
└── charts/
    ├── monthly_tickets.png
    ├── sla_breach_by_category.png
    ├── resolution_time_by_team.png
    └── priority_distribution.png
```

---

## 📂 Project Structure

```
IT Service Desk Analytics/
├── src/                                 # Reusable Python modules
│   ├── __init__.py
│   ├── data_loader.py                  # CSV/Excel loading & saving
│   ├── data_cleaner.py                 # Data validation & cleaning
│   ├── data_generator.py                # Synthetic data generation
│   ├── metrics.py                       # KPI calculations
│   └── visualizations.py                # Chart generation
├── data/                                # Data files
│   ├── raw_service_tickets.csv          # Synthetic raw data
│   ├── cleaned_service_tickets.csv      # Cleaned data
│   └── engineered_service_tickets.csv   # With engineered features
├── outputs/                             # Analysis and visualization outputs
│   ├── charts/                          # PNG exports
│   ├── *.csv                            # Analysis summary tables
│   └── powerbi_service_tickets.csv      # Power BI import file
├── generate_data.py                     # Generate synthetic data
├── clean_data.py                        # Data cleaning pipeline
├── engineer_features.py                 # Feature engineering
├── explore_data.py                      # EDA & analysis
├── visualize_charts.py                  # Create matplotlib charts
├── prepare_powerbi.py                   # Power BI preparation
├── POWERBI_DASHBOARD_DESIGN_GUIDE.md   # Dashboard specification
├── requirements.txt                     # Python dependencies
├── .gitignore                           # Git configuration
└── README.md                            # This file
```

---

## 💡 Skills Demonstrated

### Data Engineering
✅ End-to-end ETL pipeline (Extract, Transform, Load)  
✅ Data validation and quality checks  
✅ Synthetic data generation with realistic distributions  
✅ Datetime handling and time-based feature engineering  
✅ Data de-duplication and integrity checks  

### Data Analysis
✅ Exploratory Data Analysis (EDA)  
✅ Descriptive statistics and distributions  
✅ KPI definition and calculation  
✅ Groupby aggregations and pivot analysis  
✅ Trend identification and monthly forecasting  

### Data Visualization
✅ Professional matplotlib charts  
✅ Conditional formatting and color coding  
✅ Multi-dimensional data representation  
✅ Executive-ready visualization design  
✅ Chart optimization for insights  

### Business Intelligence
✅ Power BI dataset preparation  
✅ Executive dashboard design specification  
✅ Business metric definition  
✅ KPI tracking and monitoring  
✅ Data storytelling for stakeholders  

### Software Engineering
✅ Object-oriented Python programming  
✅ Modular code design (src/ modules)  
✅ Reusable functions and classes  
✅ Clear documentation and comments  
✅ Git version control and best practices  

### Tools & Technologies
✅ Python (pandas, NumPy, matplotlib)  
✅ Git & GitHub  
✅ CSV data formats  
✅ Power BI (data import & design)  
✅ Virtual environments & dependency management  

---

## 📈 Metrics & Results

| Metric | Value | Status |
|--------|-------|--------|
| Data Quality (complete) | 100% | ✅ |
| Duplicate records | 0 | ✅ |
| Missing values | 0 | ✅ |
| SLA Compliance | 72.3% | ⚠️ |
| Avg resolution time | 57.9 hours | 📊 |
| Data completeness | 2,000 records | ✅ |
| Visualization count | 4 professional charts | ✅ |

---

## 🔐 Data & Privacy

- **Data Type:** Synthetically generated (no real customer data)
- **Privacy:** 100% anonymized and fictional
- **Sensitivity:** Portfolio project - suitable for public sharing
- **Compliance:** No GDPR/PII concerns

---

## 🤝 Contributing

Contributions welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Write clear commit messages
5. Push to the branch (`git push origin feature/improvement`)
6. Open a Pull Request

---

## 📚 Learning Resources

This project demonstrates:
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Visualization](https://matplotlib.org/stable/tutorials/)
- [Power BI Best Practices](https://docs.microsoft.com/en-us/power-bi/)
- [Data Analysis Fundamentals](https://www.coursera.org/learn/data-analysis-fundamentals)

---

## 📧 Contact & Support

**Author:** Devansh Mehrotra  
**Email:** [Your Email]  
**LinkedIn:** [Your LinkedIn Profile]  
**GitHub:** [Your GitHub Profile]

Questions or feedback? Feel free to open an issue or reach out!

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Data generation based on realistic IT Service Desk scenarios
- Chart design following Microsoft design principles
- Dashboard specification aligned with executive BI best practices
- Inspired by real-world service desk analytics needs

---

**Last Updated:** February 11, 2026  
**Status:** Complete & Production-Ready ✅

---

### ⭐ If you found this project helpful, please consider giving it a star!


