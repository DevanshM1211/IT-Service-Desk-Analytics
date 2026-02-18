"""
Root cause and recurring issue analysis for Service Desk Analytics
"""

import pandas as pd
from typing import Dict


class ServiceDeskRootCauseAnalyzer:
    """Analyze recurring incidents and escalation concentration."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._validate_required_columns()

    def _validate_required_columns(self) -> None:
        required = {
            "Ticket_ID",
            "Category",
            "Priority",
            "Assigned_Team",
            "SLA_Breached",
        }
        missing = required.difference(set(self.df.columns))
        if missing:
            raise ValueError(f"Missing required columns for root cause analysis: {sorted(missing)}")

    def _create_issue_signature(self) -> None:
        """Create a repeatable issue signature using available dimensions."""
        self.df["Issue_Signature"] = (
            self.df["Category"].astype(str)
            + " | "
            + self.df["Priority"].astype(str)
            + " | "
            + self.df["Assigned_Team"].astype(str)
        )

    def _create_escalation_flag(self) -> None:
        """Create an escalation proxy suitable for synthetic service desk data.

        Escalation_Flag is set to True when:
        - SLA is breached, or
        - Priority is Critical
        """
        self.df["Escalation_Flag"] = (
            self.df["SLA_Breached"].astype(bool)
            | (self.df["Priority"].astype(str) == "Critical")
        )

    def analyze_repeat_incident_rate_by_category(self) -> pd.DataFrame:
        """Calculate repeat-incident concentration per category."""
        issue_counts = (
            self.df.groupby(["Category", "Issue_Signature"], as_index=False)
            .agg(incident_count=("Ticket_ID", "count"))
        )

        issue_counts["is_recurring_issue"] = issue_counts["incident_count"] > 1

        recurring_tickets = issue_counts[issue_counts["is_recurring_issue"]].groupby(
            "Category", as_index=False
        ).agg(recurring_tickets=("incident_count", "sum"))

        category_totals = self.df.groupby("Category", as_index=False).agg(
            total_tickets=("Ticket_ID", "count")
        )

        category_issue_counts = issue_counts.groupby("Category", as_index=False).agg(
            unique_issue_signatures=("Issue_Signature", "nunique"),
            recurring_issue_signatures=("is_recurring_issue", "sum"),
        )

        result = (
            category_totals
            .merge(recurring_tickets, on="Category", how="left")
            .merge(category_issue_counts, on="Category", how="left")
            .fillna({"recurring_tickets": 0, "recurring_issue_signatures": 0})
        )

        result["recurring_tickets"] = result["recurring_tickets"].astype(int)
        result["recurring_issue_signatures"] = result["recurring_issue_signatures"].astype(int)
        result["repeat_incident_rate_percent"] = (
            result["recurring_tickets"] / result["total_tickets"] * 100
        ).round(2)

        return result.sort_values("repeat_incident_rate_percent", ascending=False)

    def analyze_most_frequent_recurring_issues(self, top_n: int = 15) -> pd.DataFrame:
        """Identify top recurring issue signatures."""
        issue_counts = (
            self.df.groupby(
                ["Issue_Signature", "Category", "Priority", "Assigned_Team"],
                as_index=False,
            )
            .agg(
                incident_count=("Ticket_ID", "count"),
                breached_count=("SLA_Breached", "sum"),
            )
        )

        recurring = issue_counts[issue_counts["incident_count"] > 1].copy()
        if recurring.empty:
            return recurring

        recurring["breach_rate_percent"] = (
            recurring["breached_count"] / recurring["incident_count"] * 100
        ).round(2)
        recurring["rank"] = recurring["incident_count"].rank(method="dense", ascending=False).astype(int)

        return recurring.sort_values(
            ["incident_count", "breach_rate_percent"], ascending=[False, False]
        ).head(top_n)

    def analyze_escalations_by_team(self) -> pd.DataFrame:
        """Quantify team contribution to escalations."""
        team = self.df.groupby("Assigned_Team", as_index=False).agg(
            total_tickets=("Ticket_ID", "count"),
            escalations=("Escalation_Flag", "sum"),
            sla_breaches=("SLA_Breached", "sum"),
        )

        team["escalation_rate_percent"] = (
            team["escalations"] / team["total_tickets"] * 100
        ).round(2)

        total_escalations = team["escalations"].sum()
        if total_escalations > 0:
            team["share_of_total_escalations_percent"] = (
                team["escalations"] / total_escalations * 100
            ).round(2)
        else:
            team["share_of_total_escalations_percent"] = 0.0

        return team.sort_values("share_of_total_escalations_percent", ascending=False)

    def run_all_analyses(self, top_n_recurring: int = 15) -> Dict[str, pd.DataFrame]:
        """Run all root-cause analyses and return result tables."""
        self._create_issue_signature()
        self._create_escalation_flag()

        return {
            "repeat_incident_rate_by_category": self.analyze_repeat_incident_rate_by_category(),
            "most_frequent_recurring_issues": self.analyze_most_frequent_recurring_issues(
                top_n=top_n_recurring
            ),
            "escalations_by_team": self.analyze_escalations_by_team(),
        }
