#!/usr/bin/env python
"""
Feature Engineering for IT Service Desk Analytics

Creates derived features from cleaned ticket data:
- Resolution_Days: Resolution time in days
- Day_of_Week: Day of ticket creation (Monday-Sunday)
- Is_High_Priority: Boolean flag for High/Critical priorities
- Breach_Flag: Integer flag (1/0) for SLA breach status

Also calculates key performance indicators (KPIs) for the ticket dataset.

Input: data/cleaned_service_tickets.csv
Output: data/engineered_service_tickets.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import load_csv, save_csv


class ServiceDeskFeatureEngineer:
    """Engineer features and calculate KPIs for service desk analytics."""
    
    # Day mapping
    DAY_NAMES = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize feature engineer with DataFrame.
        
        Args:
            df: Cleaned DataFrame with datetime columns
        """
        self.df = df.copy()
        self.original_columns = list(df.columns)
        self.feature_log = []
    
    def create_resolution_days(self) -> None:
        """
        Create Resolution_Days column from Resolution_Hours.
        
        Converts hours to days for easier interpretation of resolution times.
        """
        print("⏱️  Creating Resolution_Days feature...")
        
        self.df['Resolution_Days'] = self.df['Resolution_Hours'] / 24
        self.df['Resolution_Days'] = self.df['Resolution_Days'].round(2)
        
        self.feature_log.append("Created Resolution_Days from Resolution_Hours")
        print(f"   ✓ Resolution_Days range: {self.df['Resolution_Days'].min():.2f} - {self.df['Resolution_Days'].max():.2f} days")
    
    def create_day_of_week(self) -> None:
        """
        Create Day_of_Week column from Created_Date.
        
        Extracts the day of the week (Monday-Sunday) when the ticket was created.
        Useful for analyzing patterns in ticket volume by day of week.
        """
        print("📅 Creating Day_of_Week feature...")
        
        # Ensure Created_Date is datetime
        self.df['Created_Date'] = pd.to_datetime(self.df['Created_Date'])
        
        # Extract day of week (0=Monday, 6=Sunday)
        self.df['Day_of_Week'] = self.df['Created_Date'].dt.day_name()
        
        self.feature_log.append("Created Day_of_Week from Created_Date")
        print(f"   ✓ Days represented: {sorted(self.df['Day_of_Week'].unique())}")
    
    def create_high_priority_flag(self) -> None:
        """
        Create Is_High_Priority boolean column.
        
        True if Priority is High or Critical, False otherwise.
        Useful for segmenting analysis between high and low priority tickets.
        """
        print("🚨 Creating Is_High_Priority feature...")
        
        high_priorities = ['High', 'Critical']
        self.df['Is_High_Priority'] = self.df['Priority'].isin(high_priorities)
        
        self.feature_log.append("Created Is_High_Priority from Priority")
        high_count = self.df['Is_High_Priority'].sum()
        print(f"   ✓ High/Critical tickets: {high_count} ({high_count/len(self.df)*100:.1f}%)")
    
    def create_breach_flag(self) -> None:
        """
        Create Breach_Flag integer column from SLA_Breached.
        
        Converts boolean SLA_Breached to integer (1 = breached, 0 = compliant).
        Useful for numeric calculations and aggregations.
        """
        print("❌ Creating Breach_Flag feature...")
        
        self.df['Breach_Flag'] = self.df['SLA_Breached'].astype(int)
        
        self.feature_log.append("Created Breach_Flag from SLA_Breached")
        breach_count = self.df['Breach_Flag'].sum()
        print(f"   ✓ Breached tickets: {breach_count} ({breach_count/len(self.df)*100:.1f}%)")
    
    def engineer_features(self) -> pd.DataFrame:
        """
        Execute all feature engineering steps.
        
        Returns:
            DataFrame with engineered features
        """
        print("\n" + "="*60)
        print("🔧 STARTING FEATURE ENGINEERING")
        print("="*60 + "\n")
        
        self.create_resolution_days()
        print()
        self.create_day_of_week()
        print()
        self.create_high_priority_flag()
        print()
        self.create_breach_flag()
        
        print("\n" + "="*60)
        print("✅ FEATURE ENGINEERING COMPLETE")
        print("="*60)
        
        return self.df
    
    def get_feature_list(self) -> list:
        """Get list of newly created features."""
        return [col for col in self.df.columns if col not in self.original_columns]


class ServiceDeskKPICalculator:
    """Calculate key performance indicators for service desk operations."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize KPI calculator with DataFrame.
        
        Args:
            df: DataFrame with engineered features
        """
        self.df = df
        self.kpis = {}
    
    def calculate_total_tickets(self) -> int:
        """Calculate total number of tickets."""
        total = len(self.df)
        self.kpis['total_tickets'] = total
        return total
    
    def calculate_average_resolution_time(self) -> float:
        """
        Calculate average resolution time across all tickets.
        
        Returns:
            Average resolution time in hours
        """
        avg_hours = self.df['Resolution_Hours'].mean()
        self.kpis['avg_resolution_hours'] = round(avg_hours, 2)
        return avg_hours
    
    def calculate_sla_compliance(self) -> float:
        """
        Calculate SLA compliance rate.
        
        Returns:
            Percentage of tickets that met SLA (0-100)
        """
        total = len(self.df)
        compliant = (~self.df['SLA_Breached']).sum()
        compliance_rate = (compliant / total * 100) if total > 0 else 0
        self.kpis['sla_compliance_percent'] = round(compliance_rate, 2)
        return compliance_rate
    
    def calculate_breached_tickets(self) -> int:
        """
        Calculate number of tickets that breached SLA.
        
        Returns:
            Count of breached tickets
        """
        breached = self.df['SLA_Breached'].sum()
        self.kpis['breached_tickets'] = int(breached)
        return int(breached)
    
    def calculate_metrics_by_priority(self) -> pd.DataFrame:
        """
        Calculate resolution metrics grouped by priority level.
        
        Returns:
            DataFrame with metrics by priority
        """
        metrics = self.df.groupby('Priority').agg({
            'Ticket_ID': 'count',
            'Resolution_Hours': ['mean', 'median', 'min', 'max'],
            'SLA_Breached': lambda x: (x.sum() / len(x) * 100)
        }).round(2)
        
        metrics.columns = ['Count', 'Avg_Hours', 'Median_Hours', 'Min_Hours', 'Max_Hours', 'Breach_Percent']
        return metrics.reset_index()
    
    def calculate_metrics_by_category(self) -> pd.DataFrame:
        """
        Calculate resolution metrics grouped by category.
        
        Returns:
            DataFrame with metrics by category
        """
        metrics = self.df.groupby('Category').agg({
            'Ticket_ID': 'count',
            'Resolution_Hours': 'mean',
            'SLA_Breached': lambda x: (x.sum() / len(x) * 100)
        }).round(2)
        
        metrics.columns = ['Count', 'Avg_Resolution_Hours', 'Breach_Percent']
        return metrics.reset_index().sort_values('Count', ascending=False)
    
    def calculate_metrics_by_day_of_week(self) -> pd.DataFrame:
        """
        Calculate metrics grouped by day of week.
        
        Returns:
            DataFrame with metrics by day of week
        """
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        metrics = self.df.groupby('Day_of_Week').agg({
            'Ticket_ID': 'count',
            'Resolution_Hours': 'mean',
            'SLA_Breached': lambda x: (x.sum() / len(x) * 100)
        }).round(2)
        
        metrics.columns = ['Count', 'Avg_Resolution_Hours', 'Breach_Percent']
        metrics = metrics.reindex([day for day in day_order if day in metrics.index])
        return metrics.reset_index()
    
    def calculate_kpis(self) -> Dict:
        """
        Calculate all primary KPIs.
        
        Returns:
            Dictionary with KPI values
        """
        self.calculate_total_tickets()
        self.calculate_average_resolution_time()
        self.calculate_sla_compliance()
        self.calculate_breached_tickets()
        return self.kpis
    
    def print_kpi_summary(self) -> None:
        """Print formatted KPI summary to console."""
        print("\n" + "="*60)
        print("📊 SERVICE DESK KPI SUMMARY")
        print("="*60)
        
        print(f"\n📈 Volume Metrics:")
        print(f"  Total Tickets:        {self.kpis['total_tickets']:,}")
        print(f"  Breached Tickets:     {self.kpis['breached_tickets']:,}")
        print(f"  Compliant Tickets:    {self.kpis['total_tickets'] - self.kpis['breached_tickets']:,}")
        
        print(f"\n⏱️  Time Metrics:")
        avg_hours = self.kpis['avg_resolution_hours']
        avg_days = avg_hours / 24
        print(f"  Avg Resolution Time:  {avg_hours:.2f} hours ({avg_days:.2f} days)")
        
        print(f"\n✅ SLA Metrics:")
        print(f"  SLA Compliance:       {self.kpis['sla_compliance_percent']:.1f}%")
        print(f"  SLA Breach Rate:      {100 - self.kpis['sla_compliance_percent']:.1f}%")
        
        print("\n" + "="*60)
    
    def print_detailed_metrics(self) -> None:
        """Print detailed metrics by category, priority, and day of week."""
        print("\n" + "="*60)
        print("📋 DETAILED METRICS BY DIMENSION")
        print("="*60)
        
        print("\n📊 Metrics by Priority Level:")
        print(self.calculate_metrics_by_priority().to_string(index=False))
        
        print("\n\n📂 Metrics by Category (Top 10):")
        print(self.calculate_metrics_by_category().head(10).to_string(index=False))
        
        print("\n\n📅 Metrics by Day of Week:")
        print(self.calculate_metrics_by_day_of_week().to_string(index=False))
        
        print("\n" + "="*60)


def engineer_features_and_calculate_kpis(
    input_path: str = "data/cleaned_service_tickets.csv",
    output_path: str = "data/engineered_service_tickets.csv"
) -> tuple:
    """
    Load data, engineer features, calculate KPIs, and save results.
    
    Args:
        input_path: Path to cleaned data CSV
        output_path: Path to save engineered data
        
    Returns:
        Tuple of (DataFrame, KPIs dictionary)
    """
    try:
        # Load cleaned data
        print(f"📂 Loading data from {input_path}...")
        df = load_csv(input_path)
        print(f"   Loaded {len(df)} rows with {len(df.columns)} columns\n")
        
        # Engineer features
        engineer = ServiceDeskFeatureEngineer(df)
        engineered_df = engineer.engineer_features()
        new_features = engineer.get_feature_list()
        
        print(f"\n✨ New features created: {new_features}")
        print(f"   Total columns: {len(df.columns)} → {len(engineered_df.columns)}")
        
        # Calculate KPIs
        print("\n")
        calculator = ServiceDeskKPICalculator(engineered_df)
        kpis = calculator.calculate_kpis()
        
        # Print summaries
        calculator.print_kpi_summary()
        calculator.print_detailed_metrics()
        
        # Save engineered data
        print(f"\n💾 Saving engineered data to {output_path}...")
        save_csv(engineered_df, output_path)
        print(f"   ✓ Saved {len(engineered_df)} rows with {len(engineered_df.columns)} columns")
        
        return engineered_df, kpis
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {input_path}")
        print("   Please run: python clean_data.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during feature engineering: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """Run when executed directly."""
    print("🚀 IT Service Desk Analytics - Feature Engineering & KPI Calculation\n")
    
    df, kpis = engineer_features_and_calculate_kpis()
    
    print("\n✅ Feature engineering completed successfully!")
    print("\nNext steps:")
    print("  1. Load engineered data: df = pd.read_csv('data/engineered_service_tickets.csv')")
    print("  2. Explore visualizations: jupyter notebook")
    print("  3. Create dashboards: notebooks/02_analytics_dashboard.ipynb")
