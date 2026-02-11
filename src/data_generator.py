"""
Synthetic IT Service Desk Ticket Data Generator

Generates realistic ticket data for analysis and testing purposes.
Creates 2000 tickets with dependencies between priority, category, and resolution time.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple


class TicketDataGenerator:
    """Generate synthetic IT Service Desk ticket data."""
    
    # Configuration constants
    N_TICKETS = 2000
    START_DATE = datetime(2025, 4, 1)
    END_DATE = datetime(2025, 8, 1)
    
    # Ticket categories and attributes
    PRIORITIES = ["Low", "Medium", "High", "Critical"]
    CATEGORIES = ["Network", "Hardware", "Software", "Access", "Security", "Email"]
    TEAMS = ["Infrastructure", "ServiceDesk", "CyberSecurity", "Applications"]
    
    # SLA Target Hours by Priority
    SLA_TARGETS = {
        "Critical": 4,
        "High": 24,
        "Medium": 72,
        "Low": 120
    }
    
    # Resolution time distributions (in hours) by priority
    # Format: (mean, std_dev, min, max)
    RESOLUTION_TIMES = {
        "Critical": (3, 2, 0.5, 8),      # Fast but sometimes breached
        "High": (18, 8, 2, 40),
        "Medium": (60, 20, 10, 120),
        "Low": (100, 30, 24, 168)        # Longer resolution time
    }
    
    # Priority distribution (weights)
    PRIORITY_WEIGHTS = {
        "Critical": 0.10,
        "High": 0.20,
        "Medium": 0.40,
        "Low": 0.30
    }
    
    def __init__(self, n_tickets: int = N_TICKETS, random_seed: int = 42):
        """
        Initialize the generator.
        
        Args:
            n_tickets: Number of tickets to generate
            random_seed: Random seed for reproducibility
        """
        self.n_tickets = n_tickets
        np.random.seed(random_seed)
    
    def generate_ticket_ids(self) -> list:
        """Generate unique ticket IDs in format TICKET-XXXXX."""
        return [f"TICKET-{str(i+1).zfill(5)}" for i in range(self.n_tickets)]
    
    def generate_created_dates(self) -> list:
        """Generate random creation dates between START_DATE and END_DATE."""
        time_between = (self.END_DATE - self.START_DATE).total_seconds()
        random_seconds = np.random.uniform(0, time_between, self.n_tickets)
        return [self.START_DATE + timedelta(seconds=s) for s in random_seconds]
    
    def generate_priorities(self) -> list:
        """Generate ticket priorities with realistic distribution."""
        priorities = list(self.PRIORITY_WEIGHTS.keys())
        weights = list(self.PRIORITY_WEIGHTS.values())
        return list(np.random.choice(priorities, size=self.n_tickets, p=weights))
    
    def generate_categories(self) -> list:
        """Generate ticket categories randomly."""
        return list(np.random.choice(self.CATEGORIES, size=self.n_tickets))
    
    def generate_teams(self) -> list:
        """Generate assigned teams randomly."""
        return list(np.random.choice(self.TEAMS, size=self.n_tickets))
    
    def generate_sla_targets(self, priorities: list) -> list:
        """
        Map SLA target hours based on priority.
        
        Args:
            priorities: List of priority levels
            
        Returns:
            List of SLA target hours
        """
        return [self.SLA_TARGETS[priority] for priority in priorities]
    
    def generate_resolution_hours(self, priorities: list) -> list:
        """
        Generate realistic resolution times based on priority.
        
        Resolution times follow distributions specific to each priority level.
        Critical tickets are usually fast but sometimes breach SLA.
        Low priority tickets take longer.
        
        Args:
            priorities: List of priority levels
            
        Returns:
            List of resolution hours
        """
        resolution_hours = []
        
        for priority in priorities:
            mean, std_dev, min_hours, max_hours = self.RESOLUTION_TIMES[priority]
            
            # Generate from normal distribution
            hours = np.random.normal(mean, std_dev)
            
            # Ensure within realistic bounds
            hours = max(min_hours, min(hours, max_hours))
            
            resolution_hours.append(round(hours, 2))
        
        return resolution_hours
    
    def generate_resolved_dates(self, created_dates: list, resolution_hours: list) -> list:
        """
        Generate resolution dates based on creation dates and resolution time.
        
        Args:
            created_dates: List of creation dates
            resolution_hours: List of resolution times in hours
            
        Returns:
            List of resolution dates
        """
        return [
            created + timedelta(hours=hours)
            for created, hours in zip(created_dates, resolution_hours)
        ]
    
    def calculate_sla_breached(self, resolution_hours: list, sla_targets: list) -> list:
        """
        Determine if SLA was breached (resolution_hours > sla_target).
        
        Args:
            resolution_hours: List of actual resolution hours
            sla_targets: List of SLA target hours
            
        Returns:
            List of boolean values indicating SLA breach
        """
        return [hours > target for hours, target in zip(resolution_hours, sla_targets)]
    
    def generate(self) -> pd.DataFrame:
        """
        Generate complete synthetic ticket dataset.
        
        Returns:
            DataFrame with generated ticket data
        """
        print(f"Generating {self.n_tickets} synthetic service desk tickets...")
        
        # Generate all columns
        ticket_ids = self.generate_ticket_ids()
        created_dates = self.generate_created_dates()
        priorities = self.generate_priorities()
        categories = self.generate_categories()
        teams = self.generate_teams()
        sla_targets = self.generate_sla_targets(priorities)
        resolution_hours = self.generate_resolution_hours(priorities)
        resolved_dates = self.generate_resolved_dates(created_dates, resolution_hours)
        sla_breached = self.calculate_sla_breached(resolution_hours, sla_targets)
        
        # Create DataFrame
        df = pd.DataFrame({
            "Ticket_ID": ticket_ids,
            "Created_Date": created_dates,
            "Resolved_Date": resolved_dates,
            "Priority": priorities,
            "Category": categories,
            "Assigned_Team": teams,
            "SLA_Target_Hours": sla_targets,
            "Resolution_Hours": resolution_hours,
            "SLA_Breached": sla_breached
        })
        
        print(f"✓ Generated {len(df)} tickets")
        return df
    
    @staticmethod
    def save_to_csv(df: pd.DataFrame, filepath: str = "data/raw_service_tickets.csv") -> None:
        """
        Save generated data to CSV file.
        
        Args:
            df: DataFrame to save
            filepath: Output file path (relative to project root)
        """
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"✓ Saved to {output_path}")


def generate_sample_dataset(n_tickets: int = 2000, 
                           output_path: str = "data/raw_service_tickets.csv") -> pd.DataFrame:
    """
    Convenience function to generate and save ticket dataset.
    
    Args:
        n_tickets: Number of tickets to generate
        output_path: Output file path
        
    Returns:
        Generated DataFrame
    """
    generator = TicketDataGenerator(n_tickets=n_tickets)
    df = generator.generate()
    generator.save_to_csv(df, output_path)
    
    # Print summary statistics
    print("\n" + "="*60)
    print("DATASET SUMMARY")
    print("="*60)
    print(f"Total Tickets: {len(df)}")
    print(f"\nPriority Distribution:")
    print(df["Priority"].value_counts().sort_index())
    print(f"\nCategory Distribution:")
    print(df["Category"].value_counts())
    print(f"\nTeam Distribution:")
    print(df["Assigned_Team"].value_counts())
    print(f"\nSLA Compliance:")
    sla_compliant = (~df["SLA_Breached"]).sum()
    sla_breached = df["SLA_Breached"].sum()
    print(f"  Met SLA: {sla_compliant} ({sla_compliant/len(df)*100:.1f}%)")
    print(f"  Breached SLA: {sla_breached} ({sla_breached/len(df)*100:.1f}%)")
    print(f"\nResolution Time Statistics (hours):")
    print(df["Resolution_Hours"].describe().round(2))
    print("="*60)
    
    return df


if __name__ == "__main__":
    """Run when executed directly."""
    df = generate_sample_dataset()
