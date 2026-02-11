#!/usr/bin/env python
"""
Clean and process IT Service Desk ticket data

Performs data cleaning tasks:
- Convert date columns to datetime
- Handle missing values
- Remove duplicate records
- Validate categorical values
- Create time-based features (Month, Week)

Input: data/raw_service_tickets.csv
Output: data/cleaned_service_tickets.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import load_csv, save_csv


class ServiceDeskDataCleaner:
    """Clean and validate IT Service Desk ticket data."""
    
    # Valid values for categorical columns
    VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
    VALID_CATEGORIES = ["Network", "Hardware", "Software", "Access", "Security", "Email"]
    VALID_TEAMS = ["Infrastructure", "ServiceDesk", "CyberSecurity", "Applications"]
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize cleaner with DataFrame.
        
        Args:
            df: DataFrame to clean
        """
        self.df = df.copy()
        self.initial_rows = len(df)
        self.cleaning_log = []
    
    def convert_datetime_columns(self) -> None:
        """
        Convert Created_Date and Resolved_Date to datetime objects.
        """
        print("📅 Converting date columns to datetime...")
        
        date_columns = ["Created_Date", "Resolved_Date"]
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                self.cleaning_log.append(f"Converted {col} to datetime")
    
    def handle_missing_values(self) -> None:
        """
        Identify and handle missing values appropriately.
        """
        print("🔍 Checking for missing values...")
        
        missing_summary = self.df.isnull().sum()
        missing_cols = missing_summary[missing_summary > 0]
        
        if len(missing_cols) > 0:
            print(f"  Found missing values in {len(missing_cols)} columns:")
            for col, count in missing_cols.items():
                print(f"    - {col}: {count} missing values ({count/len(self.df)*100:.2f}%)")
                self.cleaning_log.append(f"{col}: {count} missing values detected")
            
            # Drop rows with missing values (appropriate for service desk data)
            rows_before = len(self.df)
            self.df = self.df.dropna()
            rows_dropped = rows_before - len(self.df)
            print(f"  ✓ Dropped {rows_dropped} rows with missing values")
            self.cleaning_log.append(f"Dropped {rows_dropped} rows with missing values")
        else:
            print("  ✓ No missing values found")
    
    def remove_duplicate_tickets(self) -> None:
        """
        Remove duplicate Ticket_IDs, keeping the first occurrence.
        """
        print("🔄 Checking for duplicate Ticket_IDs...")
        
        if "Ticket_ID" in self.df.columns:
            duplicates = self.df["Ticket_ID"].duplicated().sum()
            
            if duplicates > 0:
                self.df = self.df.drop_duplicates(subset=["Ticket_ID"], keep="first")
                print(f"  ✓ Removed {duplicates} duplicate Ticket_IDs")
                self.cleaning_log.append(f"Removed {duplicates} duplicate Ticket_IDs")
            else:
                print("  ✓ No duplicate Ticket_IDs found")
    
    def validate_categorical_values(self) -> None:
        """
        Validate Priority and Category values, fix invalid entries.
        """
        print("✅ Validating categorical columns...")
        
        categorical_validations = {
            "Priority": self.VALID_PRIORITIES,
            "Category": self.VALID_CATEGORIES,
            "Assigned_Team": self.VALID_TEAMS
        }
        
        for col, valid_values in categorical_validations.items():
            if col in self.df.columns:
                invalid_count = (~self.df[col].isin(valid_values)).sum()
                
                if invalid_count > 0:
                    print(f"  ⚠️  {col}: Found {invalid_count} invalid values")
                    invalid_vals = self.df[~self.df[col].isin(valid_values)][col].unique()
                    print(f"      Invalid values: {invalid_vals}")
                    
                    # Remove rows with invalid categorical values
                    self.df = self.df[self.df[col].isin(valid_values)]
                    self.cleaning_log.append(f"Removed {invalid_count} rows with invalid {col} values")
                    print(f"  ✓ Removed rows with invalid {col} values")
                else:
                    print(f"  ✓ {col}: All values valid")
    
    def create_time_features(self) -> None:
        """
        Create Month and Week columns from Created_Date.
        """
        print("📆 Creating time-based features...")
        
        if "Created_Date" in self.df.columns:
            # Create Month (YYYY-MM format)
            self.df["Month"] = self.df["Created_Date"].dt.to_period("M").astype(str)
            
            # Create Week (ISO week number)
            self.df["Week"] = self.df["Created_Date"].dt.isocalendar().week.astype(int)
            
            # Create Year
            self.df["Year"] = self.df["Created_Date"].dt.year
            
            print("  ✓ Created Month, Week, and Year columns")
            self.cleaning_log.append("Created Month, Week, Year columns from Created_Date")
    
    def clean(self) -> pd.DataFrame:
        """
        Execute all cleaning steps.
        
        Returns:
            Cleaned DataFrame
        """
        print("\n" + "="*60)
        print("🧹 STARTING DATA CLEANING PROCESS")
        print("="*60 + "\n")
        
        self.convert_datetime_columns()
        print()
        self.handle_missing_values()
        print()
        self.remove_duplicate_tickets()
        print()
        self.validate_categorical_values()
        print()
        self.create_time_features()
        
        print("\n" + "="*60)
        print("✅ CLEANING COMPLETE")
        print("="*60)
        
        return self.df
    
    def get_summary(self) -> dict:
        """
        Generate cleaning summary statistics.
        
        Returns:
            Dictionary with summary statistics
        """
        final_rows = len(self.df)
        rows_removed = self.initial_rows - final_rows
        
        summary = {
            "initial_rows": self.initial_rows,
            "final_rows": final_rows,
            "rows_removed": rows_removed,
            "removal_percentage": (rows_removed / self.initial_rows * 100) if self.initial_rows > 0 else 0,
            "columns": len(self.df.columns),
            "missing_values": self.df.isnull().sum().sum(),
            "cleaning_log": self.cleaning_log
        }
        
        return summary
    
    def print_summary(self) -> None:
        """Print cleaning summary to console."""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("📊 CLEANING SUMMARY")
        print("="*60)
        print(f"Initial rows:       {summary['initial_rows']:,}")
        print(f"Final rows:         {summary['final_rows']:,}")
        print(f"Rows removed:       {summary['rows_removed']:,} ({summary['removal_percentage']:.2f}%)")
        print(f"Total columns:      {summary['columns']}")
        print(f"Remaining nulls:    {summary['missing_values']}")
        
        print("\nColumn Information:")
        print(f"  Data types:")
        for col, dtype in self.df.dtypes.items():
            print(f"    - {col}: {dtype}")
        
        print(f"\nMissing Values per Column:")
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) == 0:
            print("    None")
        else:
            for col, count in missing.items():
                print(f"    - {col}: {count} ({count/len(self.df)*100:.2f}%)")
        
        print(f"\nValue Counts (samples):")
        print(f"  Priority:")
        print(self.df["Priority"].value_counts().to_string().replace("\n", "\n    "))
        print(f"  Category:")
        print(self.df["Category"].value_counts().to_string().replace("\n", "\n    "))
        print(f"  Assigned_Team:")
        print(self.df["Assigned_Team"].value_counts().to_string().replace("\n", "\n    "))
        
        print("\nDate Range:")
        print(f"  Created:  {self.df['Created_Date'].min()} to {self.df['Created_Date'].max()}")
        print(f"  Resolved: {self.df['Resolved_Date'].min()} to {self.df['Resolved_Date'].max()}")
        
        print("\n" + "="*60)


def clean_service_desk_data(input_path: str = "data/raw_service_tickets.csv",
                            output_path: str = "data/cleaned_service_tickets.csv") -> pd.DataFrame:
    """
    Load raw data, clean it, and save cleaned version.
    
    Args:
        input_path: Path to raw data CSV
        output_path: Path to save cleaned data
        
    Returns:
        Cleaned DataFrame
    """
    try:
        # Load raw data
        print(f"📂 Loading data from {input_path}...")
        df = load_csv(input_path)
        print(f"   Loaded {len(df)} rows with {len(df.columns)} columns\n")
        
        # Clean data
        cleaner = ServiceDeskDataCleaner(df)
        cleaned_df = cleaner.clean()
        cleaner.print_summary()
        
        # Save cleaned data
        print(f"\n💾 Saving cleaned data to {output_path}...")
        save_csv(cleaned_df, output_path)
        print(f"   ✓ Saved {len(cleaned_df)} rows")
        
        return cleaned_df
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {input_path}")
        print("   Please run: python3 generate_data.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during cleaning: {e}")
        sys.exit(1)


if __name__ == "__main__":
    """Run when executed directly."""
    print("🚀 IT Service Desk Analytics - Data Cleaning Script\n")
    
    df = clean_service_desk_data()
    
    print("\n✅ Data cleaning completed successfully!")
    print("\nNext steps:")
    print("  1. Verify cleaned data: df = pd.read_csv('data/cleaned_service_tickets.csv')")
    print("  2. Explore in notebooks: jupyter notebook")
    print("  3. Start analysis: notebooks/01_data_exploration.ipynb")
