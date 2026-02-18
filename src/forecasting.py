"""
Lightweight forecasting utilities for Service Desk Analytics
"""

import pandas as pd


class WeeklyTicketVolumeForecaster:
    """Forecast weekly ticket volume using a simple moving-average baseline."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._validate_required_columns()

    def _validate_required_columns(self) -> None:
        required = {"Ticket_ID", "Created_Date"}
        missing = required.difference(set(self.df.columns))
        if missing:
            raise ValueError(f"Missing required columns for forecasting: {sorted(missing)}")

    def prepare_weekly_volume(self) -> pd.DataFrame:
        """Aggregate ticket counts by ISO week (week starting Monday)."""
        self.df["Created_Date"] = pd.to_datetime(self.df["Created_Date"])

        weekly = (
            self.df.set_index("Created_Date")
            .resample("W-MON")
            .size()
            .reset_index(name="actual_tickets")
            .rename(columns={"Created_Date": "week_start_date"})
        )

        weekly = weekly.sort_values("week_start_date").reset_index(drop=True)
        return weekly

    def forecast_next_4_weeks(self, weekly_df: pd.DataFrame, window: int = 4) -> pd.DataFrame:
        """Forecast next 4 weeks using trailing moving average baseline."""
        if weekly_df.empty:
            raise ValueError("Weekly volume DataFrame is empty; cannot forecast.")

        recent_values = weekly_df["actual_tickets"].tail(window)
        baseline = float(recent_values.mean())

        variability_window = weekly_df["actual_tickets"].tail(max(8, window))
        variability = float(variability_window.std(ddof=0)) if len(variability_window) > 1 else 0.0

        last_week = weekly_df["week_start_date"].max()
        future_weeks = pd.date_range(start=last_week + pd.Timedelta(days=7), periods=4, freq="W-MON")

        forecast = pd.DataFrame({
            "week_start_date": future_weeks,
            "forecast_tickets": [round(baseline)] * 4,
            "lower_bound": [max(0, round(baseline - variability))] * 4,
            "upper_bound": [round(baseline + variability)] * 4,
            "method": [f"{window}-week moving average baseline"] * 4,
            "baseline_last_4_week_avg": [round(baseline, 2)] * 4,
        })

        return forecast
