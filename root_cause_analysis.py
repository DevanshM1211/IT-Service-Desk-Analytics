#!/usr/bin/env python
"""
Root Cause & Recurring Issue Analysis for IT Service Desk Analytics

Identifies:
- Categories with highest repeat incident rates
- Most frequent recurring issues
- Teams contributing most to escalations

Input: data/engineered_service_tickets.csv
Output: CSV files in outputs/
"""

import sys
from pathlib import Path
from typing import Dict
import pandas as pd

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import load_csv
from root_cause import ServiceDeskRootCauseAnalyzer


def save_root_cause_results(analyses: Dict[str, pd.DataFrame], output_dir: str = "outputs") -> None:
    """Save root-cause analysis tables to CSV files."""
    print("\n" + "=" * 70)
    print("💾 SAVING ROOT-CAUSE ANALYSIS RESULTS")
    print("=" * 70 + "\n")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_mapping = {
        "repeat_incident_rate_by_category": "repeat_incident_rate_by_category.csv",
        "most_frequent_recurring_issues": "most_frequent_recurring_issues.csv",
        "escalations_by_team": "escalations_by_team.csv",
    }

    for analysis_key, filename in file_mapping.items():
        if analysis_key in analyses:
            df = analyses[analysis_key]
            filepath = output_path / filename
            df.to_csv(filepath, index=False)
            print(f"✓ Saved {filename}")
            print(f"  Location: {filepath}")
            print(f"  Rows: {len(df)}, Columns: {len(df.columns)}\n")


def print_root_cause_summary(analyses: Dict[str, pd.DataFrame]) -> None:
    """Print business-friendly summary insights."""
    print("\n" + "=" * 70)
    print("📋 ROOT-CAUSE ANALYSIS SUMMARY")
    print("=" * 70)

    category_df = analyses.get("repeat_incident_rate_by_category", pd.DataFrame())
    if not category_df.empty:
        top_category = category_df.iloc[0]
        print("\n1️⃣  Repeat Incident Rate by Category")
        print("-" * 70)
        print(category_df.to_string(index=False))
        print("\n   💡 Insight:")
        print(
            f"      • Highest repeat incident concentration: {top_category['Category']} "
            f"({top_category['repeat_incident_rate_percent']:.2f}%)"
        )

    recurring_df = analyses.get("most_frequent_recurring_issues", pd.DataFrame())
    if not recurring_df.empty:
        top_issue = recurring_df.iloc[0]
        print("\n\n2️⃣  Most Frequent Recurring Issues")
        print("-" * 70)
        print(recurring_df.head(10).to_string(index=False))
        print("\n   💡 Insight:")
        print(
            f"      • Top recurring issue signature: {top_issue['Issue_Signature']} "
            f"({int(top_issue['incident_count'])} incidents, "
            f"{top_issue['breach_rate_percent']:.2f}% breach rate)"
        )

    team_df = analyses.get("escalations_by_team", pd.DataFrame())
    if not team_df.empty:
        top_team = team_df.iloc[0]
        print("\n\n3️⃣  Escalations by Team")
        print("-" * 70)
        print(team_df.to_string(index=False))
        print("\n   💡 Insight:")
        print(
            f"      • Largest escalation contributor: {top_team['Assigned_Team']} "
            f"({top_team['share_of_total_escalations_percent']:.2f}% of all escalations)"
        )


def perform_root_cause_analysis(
    input_path: str = "data/engineered_service_tickets.csv",
    output_dir: str = "outputs",
) -> Dict[str, pd.DataFrame]:
    """Execute end-to-end root-cause analysis."""
    try:
        print(f"📂 Loading data from {input_path}...")
        df = load_csv(input_path)
        print(f"   Loaded {len(df)} rows with {len(df.columns)} columns\n")

        analyzer = ServiceDeskRootCauseAnalyzer(df)
        analyses = analyzer.run_all_analyses(top_n_recurring=15)

        print_root_cause_summary(analyses)
        save_root_cause_results(analyses, output_dir=output_dir)
        return analyses

    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {input_path}")
        print("   Please run: python engineer_features.py")
        sys.exit(1)
    except Exception as exc:
        print(f"\n❌ Error during root-cause analysis: {exc}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def main() -> None:
    """Main execution function."""
    print("🚀 IT Service Desk Analytics - Root Cause & Recurring Issue Analysis\n")
    perform_root_cause_analysis()

    print("\n✅ Root-cause analysis completed successfully!")
    print("\nGenerated files in outputs/:")
    print("  • repeat_incident_rate_by_category.csv")
    print("  • most_frequent_recurring_issues.csv")
    print("  • escalations_by_team.csv")


if __name__ == "__main__":
    main()
