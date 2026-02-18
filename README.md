# IT Service Desk Analytics (Portfolio Case Study)

End-to-end analytics project designed for an enterprise IT Operations / ServiceNow-style service desk context.  
This project demonstrates how raw ticket data is transformed into decision-ready KPI reporting, root-cause insights, forecasting, and Power BI outputs.

---

## Business Problem
IT service desk leaders need a reliable way to answer:
- Are we meeting SLA commitments consistently?
- Which categories and teams drive delays and escalations?
- Where are recurring incident patterns appearing?
- What ticket volume should we plan for in the next month?

Without a structured pipeline, reporting is reactive and operational risks are hard to prioritize.

---

## Solution Overview
This repository implements a modular analytics workflow:

1. **Data Generation** → synthetic but realistic IT ticket dataset  
2. **Data Cleaning & Validation** → quality controls for dates, nulls, duplicates, categorical values  
3. **Feature Engineering & KPI Computation** → SLA flags, priority indicators, resolution metrics  
4. **Exploratory Business Analysis** → category, team, priority, and trend breakdowns  
5. **Root Cause / Recurrence Diagnostics** → repeat incidents, recurring issue signatures, team escalation concentration  
6. **4-Week Forecasting** → simple moving-average baseline for near-term staffing planning  
7. **Visualization & BI Export** → chart outputs + Power BI-ready dataset

---

## Key KPIs Tracked
- **Total Ticket Volume**
- **SLA Compliance Rate / Breach Rate**
- **Average Resolution Time (hours, days)**
- **Priority Mix (Critical/High/Medium/Low)**
- **Category-Level Breach Concentration**
- **Team-Level Escalation Contribution**

---

## Outputs

### Core Data Outputs
- `data/raw_service_tickets.csv`
- `data/cleaned_service_tickets.csv`
- `data/engineered_service_tickets.csv`

### Business Analysis Outputs (`outputs/`)
- `priority_distribution.csv`
- `sla_breach_by_category.csv`
- `resolution_time_by_team.csv`
- `ticket_volume_trend.csv`
- `repeat_incident_rate_by_category.csv`
- `most_frequent_recurring_issues.csv`
- `escalations_by_team.csv`
- `weekly_ticket_volume_actuals.csv`
- `ticket_volume_forecast_4_weeks.csv`
- `powerbi_service_tickets.csv`

### Chart Outputs (`outputs/charts/`)
- `monthly_tickets.png`
- `sla_breach_by_category.png`
- `resolution_time_by_team.png`
- `priority_distribution.png`

### SQL Pack
- `sql/queries.sql` with KPI, SLA, category, team, trend, and outlier queries

---

## Tech Stack
- **Python** (pandas, numpy)
- **Visualization** (matplotlib, plotly)
- **Statistics / ML utilities** (scipy, scikit-learn)
- **SQL analytics** (T-SQL style query pack)
- **Testing** (pytest)
- **BI** (Power BI-ready export + dashboard design guide)

---

## How to Run

### 1) Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2) Run Full Pipeline (recommended)
```bash
bash run_full_pipeline.sh
```

### 3) Run Individual Steps (optional)
```bash
python generate_data.py
python clean_data.py
python engineer_features.py
python explore_data.py
python root_cause_analysis.py
python forecast_ticket_volume.py
python visualize_charts.py
python prepare_powerbi.py
```

---

## Project Structure

```text
src/
  data_loader.py
  data_cleaner.py
  data_generator.py
  metrics.py
  visualizations.py
  root_cause.py
  forecasting.py

scripts/
  generate_data.py
  clean_data.py
  engineer_features.py
  explore_data.py
  root_cause_analysis.py
  forecast_ticket_volume.py
  visualize_charts.py
  prepare_powerbi.py

outputs/
  *.csv
  charts/*.png

sql/
  queries.sql
```

---

## Interview Talking Points
- Built an **end-to-end analytics pipeline** from raw ticket data to BI-ready delivery.
- Combined **descriptive KPIs** with **diagnostic root-cause analysis** and **predictive planning**.
- Designed outputs for **enterprise operations reporting** (service desk leadership, team leads, and analysts).
- Added modular code and test coverage to keep the solution maintainable and production-style.

---

## Documentation
- `EXECUTIVE_SUMMARY.md` (consulting-style one-page brief)
- `POWERBI_DASHBOARD_DESIGN_GUIDE.md` (dashboard layout and UX recommendations)
- `sql/README.md` (query catalog and usage)
