#!/usr/bin/env python
"""
Create business-style charts for IT Service Desk Analytics

Generates 4 publication-ready charts:
1. Tickets per month (line chart)
2. SLA breach rate by category (bar chart)
3. Average resolution time by team (bar chart)
4. Ticket count by priority (bar chart)

Uses matplotlib with default styling for professional appearance.

Input: CSV files from outputs/
Output: PNG charts in outputs/charts/
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import load_csv


class ServiceDeskChartGenerator:
    """Generate professional business charts for service desk analytics."""
    
    # Chart display settings
    FIGURE_SIZE = (10, 6)
    DPI = 100
    FONT_SIZE = 11
    
    def __init__(self, output_dir: str = "outputs/charts"):
        """
        Initialize chart generator.
        
        Args:
            output_dir: Directory to save charts
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_monthly_tickets_chart(self, df: pd.DataFrame) -> None:
        """
        Create line chart showing ticket volume trend by month.
        
        Args:
            df: DataFrame with ticket_volume_trend.csv data
        """
        print("📈 Creating monthly tickets chart...")
        
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE, dpi=self.DPI)
        
        # Convert Month to datetime for proper sorting
        df['Month'] = pd.to_datetime(df['Month'])
        df = df.sort_values('Month')
        
        # Create line chart
        ax.plot(df['Month'], df['tickets_created'], 
               marker='o', linewidth=2, markersize=8, color='#1f77b4')
        
        # Format x-axis to show month names
        import matplotlib.dates as mdates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # Labels and title
        ax.set_xlabel('Month', fontsize=self.FONT_SIZE, fontweight='bold')
        ax.set_ylabel('Number of Tickets', fontsize=self.FONT_SIZE, fontweight='bold')
        ax.set_title('Service Desk Ticket Volume Trend', 
                    fontsize=13, fontweight='bold', pad=20)
        
        # Add grid for readability
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Add value labels on points
        for x, y in zip(df['Month'], df['tickets_created']):
            ax.text(x, y + 5, f'{int(y)}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        # Save figure
        filepath = self.output_dir / 'monthly_tickets.png'
        plt.savefig(filepath, dpi=self.DPI, bbox_inches='tight')
        print(f"   ✓ Saved: {filepath}")
        plt.close()
    
    def create_sla_breach_by_category_chart(self, df: pd.DataFrame) -> None:
        """
        Create bar chart showing SLA breach rate by category.
        
        Args:
            df: DataFrame with sla_breach_by_category.csv data
        """
        print("📊 Creating SLA breach by category chart...")
        
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE, dpi=self.DPI)
        
        # Sort by breach rate descending
        df = df.sort_values('breach_rate_percent', ascending=False)
        
        # Create bar chart
        bars = ax.bar(df['Category'], df['breach_rate_percent'], 
                      color='#ff7f0e', edgecolor='black', linewidth=1.2)
        
        # Labels and title
        ax.set_xlabel('Category', fontsize=self.FONT_SIZE, fontweight='bold')
        ax.set_ylabel('SLA Breach Rate (%)', fontsize=self.FONT_SIZE, fontweight='bold')
        ax.set_title('SLA Breach Rate by Ticket Category', 
                    fontsize=13, fontweight='bold', pad=20)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Set y-axis limit with padding
        ax.set_ylim(0, max(df['breach_rate_percent']) * 1.15)
        
        # Add grid for readability
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_axisbelow(True)
        
        # Rotate x-axis labels if needed
        fig.autofmt_xdate(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save figure
        filepath = self.output_dir / 'sla_breach_by_category.png'
        plt.savefig(filepath, dpi=self.DPI, bbox_inches='tight')
        print(f"   ✓ Saved: {filepath}")
        plt.close()
    
    def create_resolution_time_by_team_chart(self, df: pd.DataFrame) -> None:
        """
        Create bar chart showing average resolution time by team.
        
        Args:
            df: DataFrame with resolution_time_by_team.csv data
        """
        print("📊 Creating resolution time by team chart...")
        
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE, dpi=self.DPI)
        
        # Sort by resolution time descending
        df = df.sort_values('avg_resolution_hours', ascending=False)
        
        # Create bar chart
        bars = ax.bar(df['Assigned_Team'], df['avg_resolution_hours'],
                      color='#2ca02c', edgecolor='black', linewidth=1.2)
        
        # Labels and title
        ax.set_xlabel('Assigned Team', fontsize=self.FONT_SIZE, fontweight='bold')
        ax.set_ylabel('Average Resolution Time (Hours)', fontsize=self.FONT_SIZE, fontweight='bold')
        ax.set_title('Average Resolution Time by Assigned Team', 
                    fontsize=13, fontweight='bold', pad=20)
        
        # Add value labels on bars showing hours and days
        for bar in bars:
            height = bar.get_height()
            days = height / 24
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}h\n({days:.2f}d)', ha='center', va='bottom', 
                   fontsize=9, fontweight='bold')
        
        # Set y-axis limit with padding
        ax.set_ylim(0, max(df['avg_resolution_hours']) * 1.2)
        
        # Add grid for readability
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_axisbelow(True)
        
        # Rotate x-axis labels if needed
        fig.autofmt_xdate(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save figure
        filepath = self.output_dir / 'resolution_time_by_team.png'
        plt.savefig(filepath, dpi=self.DPI, bbox_inches='tight')
        print(f"   ✓ Saved: {filepath}")
        plt.close()
    
    def create_priority_distribution_chart(self, df: pd.DataFrame) -> None:
        """
        Create bar chart showing ticket count by priority.
        
        Args:
            df: DataFrame with priority_distribution.csv data
        """
        print("📊 Creating priority distribution chart...")
        
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE, dpi=self.DPI)
        
        # Sort by priority order (Critical -> High -> Medium -> Low)
        priority_order = ['Critical', 'High', 'Medium', 'Low']
        df['Priority'] = pd.Categorical(df['Priority'], 
                                       categories=priority_order, 
                                       ordered=True)
        df = df.sort_values('Priority')
        
        # Create bar chart
        bars = ax.bar(df['Priority'], df['ticket_count'],
                      color='#d62728', edgecolor='black', linewidth=1.2)
        
        # Labels and title
        ax.set_xlabel('Priority Level', fontsize=self.FONT_SIZE, fontweight='bold')
        ax.set_ylabel('Number of Tickets', fontsize=self.FONT_SIZE, fontweight='bold')
        ax.set_title('Ticket Count by Priority Level', 
                    fontsize=13, fontweight='bold', pad=20)
        
        # Add value labels on bars showing count and percentage
        for bar, (_, row) in zip(bars, df.iterrows()):
            height = bar.get_height()
            pct = row['percentage']
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}\n({pct:.1f}%)', ha='center', va='bottom',
                   fontsize=10, fontweight='bold')
        
        # Set y-axis limit with padding
        ax.set_ylim(0, max(df['ticket_count']) * 1.15)
        
        # Add grid for readability
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        
        # Save figure
        filepath = self.output_dir / 'priority_distribution.png'
        plt.savefig(filepath, dpi=self.DPI, bbox_inches='tight')
        print(f"   ✓ Saved: {filepath}")
        plt.close()
    
    def generate_all_charts(self, analysis_dir: str = "outputs") -> None:
        """
        Generate all charts from analysis CSV files.
        
        Args:
            analysis_dir: Directory containing analysis CSV files
        """
        try:
            print(f"\n📂 Loading analysis data from {analysis_dir}/...\n")
            
            # Load data files
            ticket_volume = load_csv(f"{analysis_dir}/ticket_volume_trend.csv")
            sla_breach = load_csv(f"{analysis_dir}/sla_breach_by_category.csv")
            resolution_time = load_csv(f"{analysis_dir}/resolution_time_by_team.csv")
            priority = load_csv(f"{analysis_dir}/priority_distribution.csv")
            
            print("✓ All data files loaded successfully\n")
            
            # Generate charts
            print("="*70)
            print("📊 GENERATING CHARTS")
            print("="*70 + "\n")
            
            self.create_monthly_tickets_chart(ticket_volume)
            self.create_sla_breach_by_category_chart(sla_breach)
            self.create_resolution_time_by_team_chart(resolution_time)
            self.create_priority_distribution_chart(priority)
            
            print("\n" + "="*70)
            print("✅ CHART GENERATION COMPLETE")
            print("="*70)
            
        except FileNotFoundError as e:
            print(f"\n❌ Error: Could not find analysis file: {e}")
            print("   Please run: python explore_data.py")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error during chart generation: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main execution function."""
    print("🚀 IT Service Desk Analytics - Chart Generation\n")
    
    generator = ServiceDeskChartGenerator()
    generator.generate_all_charts()
    
    # Print summary
    print(f"\n📊 Generated Charts Summary:")
    print(f"Location: {generator.output_dir}/")
    print(f"\nGenerated files:")
    print(f"  1. monthly_tickets.png - Ticket volume trend by month")
    print(f"  2. sla_breach_by_category.png - SLA breach rates by category")
    print(f"  3. resolution_time_by_team.png - Avg resolution time by team")
    print(f"  4. priority_distribution.png - Ticket count by priority")
    
    print(f"\n✨ All charts saved to: {generator.output_dir}/")
    print(f"\nNext steps:")
    print(f"  1. Review charts in outputs/charts/")
    print(f"  2. Use charts for presentations and reports")
    print(f"  3. Create interactive dashboard: jupyter notebook")


if __name__ == "__main__":
    """Run when executed directly."""
    main()
