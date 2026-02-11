#!/usr/bin/env python
"""
Generate Synthetic IT Service Desk Ticket Data

Run this script to create a realistic dataset with 2000 service desk tickets.
Output: data/raw_service_tickets.csv

Usage:
    python generate_data.py
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from data_generator import generate_sample_dataset


if __name__ == "__main__":
    print("🚀 IT Service Desk Analytics - Synthetic Data Generator\n")
    
    try:
        # Generate the dataset
        df = generate_sample_dataset(
            n_tickets=2000,
            output_path="data/raw_service_tickets.csv"
        )
        
        print("\n✅ Dataset generation completed successfully!")
        print("\nNext steps:")
        print("1. Load the data: df = pd.read_csv('data/raw_service_tickets.csv')")
        print("2. Explore in notebooks: jupyter notebook")
        print("3. Start analyzing in notebooks/01_data_exploration.ipynb")
        
    except Exception as e:
        print(f"\n❌ Error generating dataset: {e}")
        sys.exit(1)
