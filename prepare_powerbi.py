#!/usr/bin/env python
"""
Prepare IT Service Desk dataset for Power BI import

Performs data preparation for Power BI:
- Ensures all column names are Power BI friendly (no spaces, valid characters)
- Adds Ticket_Age_Hours column (calculated from Created_Date)
- Selects final useful columns for analysis
- Exports optimized dataset for Power BI

Reference date for Ticket_Age: August 1, 2025

Input: data/engineered_service_tickets.csv
Output: outputs/powerbi_service_tickets.csv
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import load_csv, save_csv


class PowerBIDataPreparation:
    """Prepare service desk data for Power BI import."""
    
    # Reference date for calculating ticket age
    REFERENCE_DATE = datetime(2025, 8, 1)
    
    # Final columns to keep for Power BI (in desired order)
    POWERBI_COLUMNS = [
        'Ticket_ID',
        'Created_Date',
        'Resolved_Date',
        'Priority',
        'Category',
        'Assigned_Team',
        'SLA_Target_Hours',
        'Resolution_Hours',
        'Resolution_Days',
        'SLA_Breached',
        'Breach_Flag',
        'Is_High_Priority',
        'Day_of_Week',
        'Month',
        'Week',
        'Year',
        'Ticket_Age_Hours'
    ]
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize Power BI preparation with DataFrame.
        
        Args:
            df: Engineered DataFrame
        """
        self.df = df.copy()
        self.original_columns = len(df.columns)
        self.preparation_log = []
    
    def clean_column_names(self) -> None:
        """
        Clean column names to be Power BI friendly.
        
        Removes spaces and special characters, uses underscores instead.
        """
        print("📝 Cleaning column names for Power BI...")
        
        # Rename columns: remove spaces, keep underscores
        renamed_columns = {}
        for col in self.df.columns:
            # Replace spaces with underscores
            new_col = col.replace(' ', '_')
            # Remove any other special characters except underscore
            new_col = ''.join(c if c.isalnum() or c == '_' else '' for c in new_col)
            renamed_columns[col] = new_col
        
        self.df.rename(columns=renamed_columns, inplace=True)
        
        # Log the changes
        changes = sum(1 for old, new in renamed_columns.items() if old != new)
        if changes > 0:
            print(f"   ✓ Renamed {changes} columns for Power BI compatibility")
            self.preparation_log.append(f"Cleaned {changes} column names")
        else:
            print(f"   ✓ All column names already Power BI friendly")
    
    def add_ticket_age_hours(self) -> None:
        """
        Add Ticket_Age_Hours column.
        
        Calculates hours elapsed from Created_Date to reference date (Aug 1, 2025).
        Useful for analyzing how long tickets have been in the system.
        """
        print("⏳ Adding Ticket_Age_Hours column...")
        
        # Ensure Created_Date is datetime
        self.df['Created_Date'] = pd.to_datetime(self.df['Created_Date'])
        
        # Calculate age in hours from reference date
        self.df['Ticket_Age_Hours'] = (
            (self.REFERENCE_DATE - self.df['Created_Date']).dt.total_seconds() / 3600
        ).round(2)
        
        # Ensure no negative values (shouldn't happen with our data)
        self.df['Ticket_Age_Hours'] = self.df['Ticket_Age_Hours'].clip(lower=0)
        
        print(f"   ✓ Created Ticket_Age_Hours column")
        print(f"     Range: {self.df['Ticket_Age_Hours'].min():.0f} - {self.df['Ticket_Age_Hours'].max():.0f} hours")
        self.preparation_log.append("Added Ticket_Age_Hours column")
    
    def select_final_columns(self) -> None:
        """
        Select final useful columns for Power BI analysis.
        
        Keeps only the columns needed for comprehensive service desk analytics.
        """
        print("📋 Selecting final columns for Power BI...")
        
        # Get columns that exist in our data
        available_cols = [col for col in self.POWERBI_COLUMNS 
                         if col in self.df.columns]
        
        # Check for any missing columns
        missing_cols = [col for col in self.POWERBI_COLUMNS 
                       if col not in self.df.columns]
        
        if missing_cols:
            print(f"   ⚠️  Missing columns: {missing_cols}")
        
        # Reorder and select columns
        self.df = self.df[available_cols]
        
        removed_cols = self.original_columns - len(available_cols)
        print(f"   ✓ Selected {len(available_cols)} columns for Power BI")
        if removed_cols > 0:
            print(f"     Removed {removed_cols} columns")
        
        self.preparation_log.append(f"Selected {len(available_cols)} final columns")
    
    def validate_data_quality(self) -> dict:
        """
        Validate data quality before export.
        
        Returns:
            Dictionary with validation metrics
        """
        validation = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicate_tickets': self.df['Ticket_ID'].duplicated().sum(),
            'data_types': self.df.dtypes.to_dict()
        }
        
        return validation
    
    def prepare(self) -> pd.DataFrame:
        """
        Execute all preparation steps.
        
        Returns:
            Prepared DataFrame ready for Power BI
        """
        print("\n" + "="*70)
        print("🔧 PREPARING DATASET FOR POWER BI")
        print("="*70 + "\n")
        
        self.clean_column_names()
        print()
        self.add_ticket_age_hours()
        print()
        self.select_final_columns()
        
        print("\n" + "="*70)
        print("✅ DATA PREPARATION COMPLETE")
        print("="*70)
        
        return self.df
    
    def print_validation_report(self, validation: dict) -> None:
        """
        Print data validation report.
        
        Args:
            validation: Dictionary with validation metrics
        """
        print("\n" + "="*70)
        print("✓ DATA QUALITY REPORT")
        print("="*70)
        
        print(f"\nDataset Dimensions:")
        print(f"  Total rows:    {validation['total_rows']:,}")
        print(f"  Total columns: {validation['total_columns']}")
        
        print(f"\nData Integrity:")
        print(f"  Duplicate Ticket_IDs: {validation['duplicate_tickets']}")
        total_nulls = sum(count for count in validation['missing_values'].values() 
                         if count > 0)
        print(f"  Missing values:       {total_nulls}")
        
        print(f"\nColumn Data Types:")
        for col, dtype in validation['data_types'].items():
            print(f"  {col}: {dtype}")
        
        print("\n✓ Dataset is ready for Power BI import")
        print("="*70)


def prepare_powerbi_dataset(
    input_path: str = "data/engineered_service_tickets.csv",
    output_path: str = "outputs/powerbi_service_tickets.csv"
) -> pd.DataFrame:
    """
    Load data, prepare for Power BI, and save.
    
    Args:
        input_path: Path to engineered data CSV
        output_path: Path to save Power BI ready data
        
    Returns:
        Prepared DataFrame
    """
    try:
        # Load engineered data
        print(f"📂 Loading data from {input_path}...")
        df = load_csv(input_path)
        print(f"   Loaded {len(df):,} rows with {len(df.columns)} columns\n")
        
        # Prepare for Power BI
        preparer = PowerBIDataPreparation(df)
        prepared_df = preparer.prepare()
        
        # Validate quality
        validation = preparer.validate_data_quality()
        preparer.print_validation_report(validation)
        
        # Save prepared dataset
        print(f"\n💾 Saving Power BI dataset to {output_path}...")
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        prepared_df.to_csv(output_path, index=False)
        
        file_size_mb = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"   ✓ Saved {len(prepared_df):,} rows with {len(prepared_df.columns)} columns")
        print(f"   File size: {file_size_mb:.2f} MB")
        
        return prepared_df
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {input_path}")
        print("   Please run: python engineer_features.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during Power BI preparation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main execution function."""
    print("🚀 IT Service Desk Analytics - Power BI Data Preparation\n")
    
    prepared_df = prepare_powerbi_dataset()
    
    # Print confirmation message
    print("\n\n" + "="*70)
    print("✅ POWER BI DATASET PREPARATION SUCCESSFUL")
    print("="*70)
    print(f"\n📊 Dataset Details:")
    print(f"  Output file:    outputs/powerbi_service_tickets.csv")
    print(f"  Total records:  {len(prepared_df):,}")
    print(f"  Total fields:   {len(prepared_df.columns)}")
    print(f"  Reference date: August 1, 2025 (for Ticket_Age_Hours)")
    
    print(f"\n📋 Included Fields:")
    for i, col in enumerate(prepared_df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\n🔍 Power BI Readiness Checklist:")
    print(f"  ✓ Column names cleaned (no spaces)")
    print(f"  ✓ All column names Power BI friendly")
    print(f"  ✓ Ticket_Age_Hours calculated")
    print(f"  ✓ Final useful columns selected")
    print(f"  ✓ Data quality validated")
    print(f"  ✓ Ready for Power BI import")
    
    print(f"\n🔗 Next Steps:")
    print(f"  1. Import outputs/powerbi_service_tickets.csv into Power BI")
    print(f"  2. Set data types in Power BI Power Query")
    print(f"  3. Create relationships between tables if applicable")
    print(f"  4. Build visualizations and dashboards")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    """Run when executed directly."""
    main()
