#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"

print_step() {
  echo
  echo "======================================================================"
  echo "$1"
  echo "======================================================================"
}

print_step "IT Service Desk Analytics - Full Pipeline"

echo "Project root: $PROJECT_ROOT"
echo "Python binary: $PYTHON_BIN"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "❌ Python not found: $PYTHON_BIN"
  exit 1
fi

print_step "1/8 Generate Synthetic Ticket Data"
"$PYTHON_BIN" generate_data.py

print_step "2/8 Clean and Validate Data"
"$PYTHON_BIN" clean_data.py

print_step "3/8 Feature Engineering + KPI Computation"
"$PYTHON_BIN" engineer_features.py

print_step "4/8 Exploratory Analysis"
"$PYTHON_BIN" explore_data.py

print_step "5/8 Root Cause / Recurring Issue Analysis"
"$PYTHON_BIN" root_cause_analysis.py

print_step "6/8 4-Week Ticket Volume Forecast"
"$PYTHON_BIN" forecast_ticket_volume.py

print_step "7/8 Chart Generation"
"$PYTHON_BIN" visualize_charts.py

print_step "8/8 Power BI Export Preparation"
"$PYTHON_BIN" prepare_powerbi.py

print_step "Pipeline Completed Successfully"

echo "✅ Enterprise analytics outputs generated."
echo ""
echo "Key artifacts:"
echo "  - data/cleaned_service_tickets.csv"
echo "  - data/engineered_service_tickets.csv"
echo "  - outputs/priority_distribution.csv"
echo "  - outputs/sla_breach_by_category.csv"
echo "  - outputs/repeat_incident_rate_by_category.csv"
echo "  - outputs/ticket_volume_forecast_4_weeks.csv"
echo "  - outputs/charts/*.png"
echo "  - outputs/powerbi_service_tickets.csv"
