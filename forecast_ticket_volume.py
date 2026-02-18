#!/usr/bin/env python
"""
Ticket Volume Forecasting for IT Service Desk Analytics

Forecasts ticket volume for the next 4 weeks using a simple moving average
baseline suitable for operational staffing and workload planning.

Input: data/engineered_service_tickets.csv
Output: CSV files in outputs/
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import load_csv
from forecasting import WeeklyTicketVolumeForecaster


def save_forecast_outputs(
    historical_weekly: pd.DataFrame,
    forecast_df: pd.DataFrame,
    output_dir: str = "outputs",
) -> None:
    """Save historical weekly volume and 4-week forecast outputs."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    historical_file = output_path / "weekly_ticket_volume_actuals.csv"
    forecast_file = output_path / "ticket_volume_forecast_4_weeks.csv"

    historical_weekly.to_csv(historical_file, index=False)
    forecast_df.to_csv(forecast_file, index=False)

    print("\n" + "=" * 70)
    print("💾 SAVING FORECAST OUTPUTS")
    print("=" * 70)
    print(f"✓ Saved weekly actuals: {historical_file}")
    print(f"✓ Saved 4-week forecast: {forecast_file}")


def print_forecast_interpretation(
    historical_weekly: pd.DataFrame,
    forecast_df: pd.DataFrame,
) -> None:
    """Print concise business interpretation for operations planning."""
    baseline = forecast_df["baseline_last_4_week_avg"].iloc[0]
    min_fcst = int(forecast_df["lower_bound"].min())
    max_fcst = int(forecast_df["upper_bound"].max())
    last_actual = int(historical_weekly["actual_tickets"].iloc[-1])

    print("\n" + "=" * 70)
    print("📈 4-WEEK TICKET VOLUME FORECAST")
    print("=" * 70)
    print(f"Method: {forecast_df['method'].iloc[0]}")
    print(f"Baseline (last 4-week average): {baseline:.2f} tickets/week")
    print(f"Most recent actual week volume: {last_actual} tickets")
    print(f"Forecast range (next 4 weeks): {min_fcst} - {max_fcst} tickets/week")

    print("\n💡 Business Interpretation:")
    print("  • Near-term demand appears stable; plan staffing around baseline weekly volume.")
    print("  • Use upper bound for peak-week scheduling and lower bound for minimum coverage.")
    print("  • Recompute this forecast weekly as new ticket data arrives.")


def perform_ticket_volume_forecast(
    input_path: str = "data/engineered_service_tickets.csv",
    output_dir: str = "outputs",
) -> pd.DataFrame:
    """Execute end-to-end weekly ticket volume forecast."""
    try:
        print(f"📂 Loading data from {input_path}...")
        df = load_csv(input_path)
        print(f"   Loaded {len(df)} rows with {len(df.columns)} columns\n")

        forecaster = WeeklyTicketVolumeForecaster(df)
        historical_weekly = forecaster.prepare_weekly_volume()
        forecast_df = forecaster.forecast_next_4_weeks(historical_weekly, window=4)

        print_forecast_interpretation(historical_weekly, forecast_df)
        save_forecast_outputs(historical_weekly, forecast_df, output_dir=output_dir)

        return forecast_df

    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {input_path}")
        print("   Please run: python engineer_features.py")
        sys.exit(1)
    except Exception as exc:
        print(f"\n❌ Error during forecasting: {exc}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def main() -> None:
    """Main execution function."""
    print("🚀 IT Service Desk Analytics - Weekly Ticket Volume Forecasting\n")
    perform_ticket_volume_forecast()

    print("\n✅ Forecasting completed successfully!")
    print("\nGenerated files in outputs/:")
    print("  • weekly_ticket_volume_actuals.csv")
    print("  • ticket_volume_forecast_4_weeks.csv")


if __name__ == "__main__":
    main()
