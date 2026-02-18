#!/usr/bin/env python
"""
Exploratory Data Analysis for IT Service Desk Analytics

Answers key business questions about service desk operations:
1. Which categories have the highest SLA breach rate?
2. Which assigned team has the longest average resolution time?
3. Ticket volume trend per month
4. Priority distribution

Generates summary tables and saves as CSV files in outputs/

Input: data/engineered_service_tickets.csv
Output: CSV files in outputs/ directory
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import load_csv, save_csv


class ServiceDeskExploratoryAnalysis:
    """Perform exploratory analysis on service desk ticket data."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analysis with DataFrame.
        
        Args:
            df: Engineered DataFrame with all features
        """
        self.df = df.copy()
        self.ensure_datetime_columns()
        self.analysis_results = {}
    
    def ensure_datetime_columns(self) -> None:
        """Ensure date columns are in datetime format."""
        if 'Created_Date' in self.df.columns:
            self.df['Created_Date'] = pd.to_datetime(self.df['Created_Date'])
        if 'Resolved_Date' in self.df.columns:
            self.df['Resolved_Date'] = pd.to_datetime(self.df['Resolved_Date'])
    
    def analyze_sla_breach_by_category(self) -> pd.DataFrame:
        """
        Question 1: Which categories have the highest SLA breach rate?
        
        Returns:
            DataFrame with SLA breach statistics by category
        """
        print("📊 Analyzing SLA Breach Rates by Category...")
        
        analysis = self.df.groupby('Category').agg(
            total_tickets=('Ticket_ID', 'count'),
            breached_tickets=('SLA_Breached', 'sum'),
            avg_resolution_hours=('Resolution_Hours', 'mean'),
            median_resolution_hours=('Resolution_Hours', 'median'),
            max_resolution_hours=('Resolution_Hours', 'max')
        ).reset_index()
        
        # Calculate breach rate
        analysis['breach_rate_percent'] = (
            analysis['breached_tickets'] / analysis['total_tickets'] * 100
        ).round(2)
        
        # Calculate compliant tickets
        analysis['compliant_tickets'] = analysis['total_tickets'] - analysis['breached_tickets']
        
        # Round numeric columns
        analysis['avg_resolution_hours'] = analysis['avg_resolution_hours'].round(2)
        analysis['median_resolution_hours'] = analysis['median_resolution_hours'].round(2)
        analysis['max_resolution_hours'] = analysis['max_resolution_hours'].round(2)
        
        # Sort by breach rate descending
        analysis = analysis.sort_values('breach_rate_percent', ascending=False)
        
        # Reorder columns
        analysis = analysis[[
            'Category', 'total_tickets', 'breached_tickets', 'compliant_tickets',
            'breach_rate_percent', 'avg_resolution_hours', 'median_resolution_hours',
            'max_resolution_hours'
        ]]
        
        self.analysis_results['sla_breach_by_category'] = analysis
        
        print(f"   ✓ Analyzed {len(analysis)} categories")
        return analysis
    
    def analyze_resolution_time_by_team(self) -> pd.DataFrame:
        """
        Question 2: Which assigned team has the longest average resolution time?
        
        Returns:
            DataFrame with resolution time statistics by team
        """
        print("📊 Analyzing Resolution Time by Assigned Team...")
        
        analysis = self.df.groupby('Assigned_Team').agg(
            total_tickets=('Ticket_ID', 'count'),
            avg_resolution_hours=('Resolution_Hours', 'mean'),
            median_resolution_hours=('Resolution_Hours', 'median'),
            min_resolution_hours=('Resolution_Hours', 'min'),
            max_resolution_hours=('Resolution_Hours', 'max'),
            std_resolution_hours=('Resolution_Hours', 'std'),
            breached_tickets=('SLA_Breached', 'sum')
        ).reset_index()
        
        # Calculate breach rate
        analysis['breach_rate_percent'] = (
            analysis['breached_tickets'] / analysis['total_tickets'] * 100
        ).round(2)
        
        # Convert hours to days for easier interpretation
        analysis['avg_resolution_days'] = (analysis['avg_resolution_hours'] / 24).round(2)
        
        # Round numeric columns
        numeric_cols = ['avg_resolution_hours', 'median_resolution_hours', 
                       'min_resolution_hours', 'max_resolution_hours', 'std_resolution_hours']
        for col in numeric_cols:
            analysis[col] = analysis[col].round(2)
        
        # Sort by average resolution time descending
        analysis = analysis.sort_values('avg_resolution_hours', ascending=False)
        
        # Reorder columns
        analysis = analysis[[
            'Assigned_Team', 'total_tickets', 'avg_resolution_hours', 'avg_resolution_days',
            'median_resolution_hours', 'min_resolution_hours', 'max_resolution_hours',
            'std_resolution_hours', 'breached_tickets', 'breach_rate_percent'
        ]]
        
        self.analysis_results['resolution_time_by_team'] = analysis
        
        print(f"   ✓ Analyzed {len(analysis)} teams")
        return analysis
    
    def analyze_ticket_volume_by_month(self) -> pd.DataFrame:
        """
        Question 3: Ticket volume trend per month
        
        Returns:
            DataFrame with ticket volume and metrics by month
        """
        print("📊 Analyzing Ticket Volume Trend by Month...")
        
        # Create month column if not exists
        if 'Month' not in self.df.columns:
            self.df['Month'] = self.df['Created_Date'].dt.to_period('M').astype(str)
        
        analysis = self.df.groupby('Month').agg(
            tickets_created=('Ticket_ID', 'count'),
            avg_resolution_hours=('Resolution_Hours', 'mean'),
            breached_tickets=('SLA_Breached', 'sum'),
            high_priority_tickets=('Is_High_Priority', 'sum')
        ).reset_index()
        
        # Calculate metrics
        analysis['breach_rate_percent'] = (
            analysis['breached_tickets'] / analysis['tickets_created'] * 100
        ).round(2)
        
        analysis['high_priority_percent'] = (
            analysis['high_priority_tickets'] / analysis['tickets_created'] * 100
        ).round(2)
        
        analysis['avg_resolution_hours'] = analysis['avg_resolution_hours'].round(2)
        
        # Ensure chronological order
        analysis['Month'] = pd.to_datetime(analysis['Month'])
        analysis = analysis.sort_values('Month')
        analysis['Month'] = analysis['Month'].astype(str)
        
        self.analysis_results['ticket_volume_by_month'] = analysis
        
        print(f"   ✓ Analyzed ticket volume across {len(analysis)} months")
        return analysis
    
    def analyze_priority_distribution(self) -> pd.DataFrame:
        """
        Question 4: Priority distribution
        
        Returns:
            DataFrame with priority distribution analysis
        """
        print("📊 Analyzing Priority Distribution...")
        
        analysis = self.df.groupby('Priority').agg(
            ticket_count=('Ticket_ID', 'count'),
            avg_resolution_hours=('Resolution_Hours', 'mean'),
            breached_tickets=('SLA_Breached', 'sum'),
            sla_target_hours=('SLA_Target_Hours', 'first')
        ).reset_index()
        
        # Calculate percentages
        total_tickets = analysis['ticket_count'].sum()
        analysis['percentage'] = (analysis['ticket_count'] / total_tickets * 100).round(2)
        analysis['breach_rate_percent'] = (
            analysis['breached_tickets'] / analysis['ticket_count'] * 100
        ).round(2)
        
        # Round numeric columns
        analysis['avg_resolution_hours'] = analysis['avg_resolution_hours'].round(2)
        
        # Define priority order for meaningful sorting
        priority_order = ['Critical', 'High', 'Medium', 'Low']
        analysis['Priority'] = pd.Categorical(
            analysis['Priority'], 
            categories=priority_order, 
            ordered=True
        )
        analysis = analysis.sort_values('Priority')
        
        # Reorder columns
        analysis = analysis[[
            'Priority', 'ticket_count', 'percentage', 'avg_resolution_hours',
            'sla_target_hours', 'breached_tickets', 'breach_rate_percent'
        ]]
        
        self.analysis_results['priority_distribution'] = analysis
        
        print(f"   ✓ Analyzed {len(analysis)} priority levels")
        return analysis
    
    def run_all_analyses(self) -> Dict[str, pd.DataFrame]:
        """
        Run all exploratory analyses.
        
        Returns:
            Dictionary with all analysis results
        """
        print("\n" + "="*70)
        print("🔍 STARTING EXPLORATORY DATA ANALYSIS")
        print("="*70 + "\n")
        
        self.analyze_priority_distribution()
        print()
        self.analyze_sla_breach_by_category()
        print()
        self.analyze_resolution_time_by_team()
        print()
        self.analyze_ticket_volume_by_month()
        
        print("\n" + "="*70)
        print("✅ EXPLORATORY ANALYSIS COMPLETE")
        print("="*70)
        
        return self.analysis_results


def print_analysis_summary(analyses: Dict[str, pd.DataFrame]) -> None:
    """
    Print formatted analysis summaries.
    
    Args:
        analyses: Dictionary with analysis results
    """
    
    print("\n\n" + "="*70)
    print("📋 EXPLORATORY ANALYSIS RESULTS")
    print("="*70)
    
    # Priority Distribution
    print("\n\n1️⃣  PRIORITY DISTRIBUTION")
    print("-" * 70)
    df = analyses.get('priority_distribution', pd.DataFrame())
    if not df.empty:
        print(df.to_string(index=False))
        
        # Add insights
        print("\n   💡 Insights:")
        medium_pct = df[df['Priority'] == 'Medium']['percentage'].values[0] if 'Priority' in df.columns else 0
        print(f"      • Medium priority tickets dominate at {medium_pct:.1f}% of volume")
        
        critical_breach = df[df['Priority'] == 'Critical']['breach_rate_percent'].values[0] if 'Priority' in df.columns else 0
        print(f"      • Critical tickets have {critical_breach:.1f}% breach rate")
    
    # SLA Breach by Category
    print("\n\n2️⃣  SLA BREACH RATE BY CATEGORY")
    print("-" * 70)
    df = analyses.get('sla_breach_by_category', pd.DataFrame())
    if not df.empty:
        print(df.to_string(index=False))
        
        # Add insights
        print("\n   💡 Insights:")
        if len(df) > 0:
            highest_breach = df.iloc[0]
            print(f"      • {highest_breach['Category']} has highest breach rate at {highest_breach['breach_rate_percent']:.1f}%")
            lowest_breach = df.iloc[-1]
            print(f"      • {lowest_breach['Category']} has lowest breach rate at {lowest_breach['breach_rate_percent']:.1f}%")
    
    # Resolution Time by Team
    print("\n\n3️⃣  AVERAGE RESOLUTION TIME BY ASSIGNED TEAM")
    print("-" * 70)
    df = analyses.get('resolution_time_by_team', pd.DataFrame())
    if not df.empty:
        print(df.to_string(index=False))
        
        # Add insights
        print("\n   💡 Insights:")
        if len(df) > 0:
            slowest = df.iloc[0]
            fastest = df.iloc[-1]
            print(f"      • {slowest['Assigned_Team']} slowest: {slowest['avg_resolution_hours']:.2f} hours ({slowest['avg_resolution_days']:.2f} days)")
            print(f"      • {fastest['Assigned_Team']} fastest: {fastest['avg_resolution_hours']:.2f} hours ({fastest['avg_resolution_days']:.2f} days)")
    
    # Ticket Volume by Month
    print("\n\n4️⃣  TICKET VOLUME TREND BY MONTH")
    print("-" * 70)
    df = analyses.get('ticket_volume_by_month', pd.DataFrame())
    if not df.empty:
        print(df.to_string(index=False))
        
        # Add insights
        print("\n   💡 Insights:")
        if len(df) > 0:
            peak_month = df.loc[df['tickets_created'].idxmax()]
            print(f"      • Peak volume in {peak_month['Month']}: {int(peak_month['tickets_created'])} tickets")
            low_month = df.loc[df['tickets_created'].idxmin()]
            print(f"      • Low volume in {low_month['Month']}: {int(low_month['tickets_created'])} tickets")


def save_analysis_results(analyses: Dict[str, pd.DataFrame], output_dir: str = "outputs") -> None:
    """
    Save analysis results as CSV files.
    
    Args:
        analyses: Dictionary with analysis results
        output_dir: Directory to save CSV files
    """
    print("\n\n" + "="*70)
    print("💾 SAVING ANALYSIS RESULTS")
    print("="*70 + "\n")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    file_mapping = {
        'priority_distribution': 'priority_distribution.csv',
        'sla_breach_by_category': 'sla_breach_by_category.csv',
        'resolution_time_by_team': 'resolution_time_by_team.csv',
        'ticket_volume_by_month': 'ticket_volume_trend.csv'
    }
    
    for analysis_key, filename in file_mapping.items():
        if analysis_key in analyses:
            df = analyses[analysis_key]
            filepath = output_path / filename
            
            # Convert DataFrame to save it
            df_to_save = df.copy()
            df_to_save.to_csv(filepath, index=False)
            
            print(f"✓ Saved {filename}")
            print(f"  Location: {filepath}")
            print(f"  Rows: {len(df_to_save)}, Columns: {len(df_to_save.columns)}\n")


def perform_exploratory_analysis(
    input_path: str = "data/engineered_service_tickets.csv",
    output_dir: str = "outputs"
) -> Dict[str, pd.DataFrame]:
    """
    Load data and perform complete exploratory analysis.
    
    Args:
        input_path: Path to engineered data CSV
        output_dir: Directory to save analysis results
        
    Returns:
        Dictionary with all analysis DataFrames
    """
    try:
        # Load engineered data
        print(f"📂 Loading data from {input_path}...")
        df = load_csv(input_path)
        print(f"   Loaded {len(df)} rows with {len(df.columns)} columns\n")
        
        # Run analyses
        analyzer = ServiceDeskExploratoryAnalysis(df)
        analyses = analyzer.run_all_analyses()
        
        # Print summaries
        print_analysis_summary(analyses)
        
        # Save results
        save_analysis_results(analyses, output_dir)
        
        return analyses
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {input_path}")
        print("   Please run: python engineer_features.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """Run when executed directly."""
    print("🚀 IT Service Desk Analytics - Exploratory Data Analysis\n")
    
    analyses = perform_exploratory_analysis()
    
    print("\n✅ Exploratory analysis completed successfully!")
    print("\nGenerated files in outputs/:")
    print("  • priority_distribution.csv")
    print("  • sla_breach_by_category.csv")
    print("  • resolution_time_by_team.csv")
    print("  • ticket_volume_trend.csv")
    print("\nNext steps:")
    print("  1. Review the CSV files in outputs/")
    print("  2. Create visualizations: python visualize_charts.py")
    print("  3. Build interactive dashboard: jupyter notebook")
