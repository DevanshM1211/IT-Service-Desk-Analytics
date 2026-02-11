# IT Service Desk Analytics Dashboard

A professional analytics dashboard for IT Service Desk operations and performance tracking.

## 📋 Project Overview

This project analyzes IT Service Desk ticket data to provide insights into:
- Ticket volume trends
- Resolution time distributions
- Priority and severity breakdowns
- Technician performance metrics
- SLA compliance monitoring

## 📁 Project Structure

```
IT Service Desk Analytics/
├── data/                          # Raw and processed data files
│   ├── raw/                       # Original unprocessed data (CSVs, exports)
│   └── processed/                 # Cleaned, transformed data ready for analysis
├── notebooks/                     # Jupyter notebooks for exploration & analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_analysis_metrics.ipynb
├── src/                           # Reusable Python modules
│   ├── __init__.py
│   ├── data_loader.py             # Data loading and I/O functions
│   ├── data_cleaner.py            # Data cleaning and validation
│   ├── metrics.py                 # Metric calculations & aggregations
│   └── visualizations.py          # Plotting and chart generation
├── outputs/                       # Generated charts, exports, dashboards
│   ├── charts/                    # PNG, SVG exports from visualization
│   ├── exports/                   # CSV, Excel exports for reporting
│   └── reports/                   # Final HTML/PDF reports
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file

```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "IT Service Desk Analytics"
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📊 Usage

### Data Processing
1. Place raw ticket export files in `data/raw/`
2. Run data cleaning notebooks in `notebooks/`
3. Cleaned data is saved to `data/processed/`

### Analysis & Visualization
1. Explore data using Jupyter notebooks in `notebooks/`
2. Use reusable functions from `src/` modules
3. Export charts and reports to `outputs/`

### Example Python Usage
```python
from src.data_loader import load_data
from src.metrics import calculate_metrics
from src.visualizations import plot_metrics

# Load processed data
df = load_data('data/processed/tickets.csv')

# Calculate metrics
metrics = calculate_metrics(df)

# Generate visualizations
plot_metrics(metrics, save_path='outputs/charts/')
```

## 📦 Dependencies

Key libraries (see `requirements.txt` for complete list):
- **pandas**: Data manipulation and analysis
- **plotly/matplotlib**: Data visualization
- **jupyter**: Interactive notebooks
- **numpy**: Numerical computations

## 📝 Workflow

1. **Data Ingestion** → Load raw ticket data from Service Desk exports
2. **Data Cleaning** → Validate, standardize, and clean data
3. **Analysis** → Calculate KPIs and performance metrics
4. **Visualization** → Create charts and dashboards
5. **Reporting** → Generate insights and export reports

## 🎯 Key Metrics Tracked

- Average Resolution Time (ART)
- First Contact Resolution (FCR)
- SLA Compliance Rate
- Average Wait Time
- Customer Satisfaction (CSAT)
- Ticket Volume Trends
- Technician Productivity

## 🤝 Contributing

When contributing to this project:
1. Create a new branch for features (`git checkout -b feature/your-feature`)
2. Use meaningful commit messages
3. Update notebooks with clear documentation
4. Add reusable functions to `src/` modules
5. Test code before pushing

## 📄 License

Add your license information here.

## 👤 Author

Your Name / Team

## 📧 Contact

Add contact information here.

---

**Last Updated**: February 2026
