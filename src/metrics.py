"""
Metrics calculation and KPI computation for Service Desk Analytics
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


def calculate_average_resolution_time(df: pd.DataFrame, created_col: str,
                                     resolved_col: str) -> float:
    """
    Calculate average resolution time (in hours).
    
    Args:
        df: DataFrame containing ticket data
        created_col: Column name for ticket creation datetime
        resolved_col: Column name for ticket resolution datetime
        
    Returns:
        Average resolution time in hours
    """
    df_copy = df.copy()
    df_copy[created_col] = pd.to_datetime(df_copy[created_col])
    df_copy[resolved_col] = pd.to_datetime(df_copy[resolved_col])
    resolution_time = (df_copy[resolved_col] - df_copy[created_col]).dt.total_seconds() / 3600
    return resolution_time.mean()


def calculate_sla_compliance(df: pd.DataFrame, resolved_col: str,
                            sla_col: str) -> float:
    """
    Calculate SLA compliance rate (percentage).
    
    Args:
        df: DataFrame containing ticket data
        resolved_col: Column indicating if ticket is resolved (boolean)
        sla_col: Column indicating if SLA was met (boolean)
        
    Returns:
        SLA compliance percentage (0-100)
    """
    resolved_tickets = df[df[resolved_col] == True]
    if len(resolved_tickets) == 0:
        return 0.0
    compliance_rate = (resolved_tickets[sla_col].sum() / len(resolved_tickets)) * 100
    return compliance_rate


def calculate_ticket_volume(df: pd.DataFrame, date_col: str,
                           group_by: str = "D") -> pd.Series:
    """
    Calculate ticket volume over time.
    
    Args:
        df: DataFrame containing ticket data
        date_col: Column name for date
        group_by: Frequency for grouping ("D"=daily, "W"=weekly, "M"=monthly)
        
    Returns:
        Series with dates and ticket counts
    """
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col])
    return df_copy.set_index(date_col).resample(group_by).size()


def calculate_metrics_by_category(df: pd.DataFrame, category_col: str,
                                 metric_col: str, metric_type: str = "mean") -> pd.DataFrame:
    """
    Calculate aggregate metrics grouped by category.
    
    Args:
        df: DataFrame containing ticket data
        category_col: Column to group by
        metric_col: Column to calculate metric on
        metric_type: "mean", "median", "sum", "count", "std"
        
    Returns:
        DataFrame with category and metric values
    """
    if metric_type == "mean":
        result = df.groupby(category_col)[metric_col].mean()
    elif metric_type == "median":
        result = df.groupby(category_col)[metric_col].median()
    elif metric_type == "sum":
        result = df.groupby(category_col)[metric_col].sum()
    elif metric_type == "count":
        result = df.groupby(category_col)[metric_col].count()
    elif metric_type == "std":
        result = df.groupby(category_col)[metric_col].std()
    else:
        raise ValueError(f"Unknown metric type: {metric_type}")
    
    return result.reset_index().rename(columns={metric_col: metric_type.capitalize()})


def calculate_percentile(df: pd.DataFrame, column: str, percentile: float) -> float:
    """
    Calculate percentile value for a column.
    
    Args:
        df: DataFrame containing data
        column: Column to analyze
        percentile: Percentile value (0-100)
        
    Returns:
        Percentile value
    """
    return df[column].quantile(percentile / 100)


def get_summary_statistics(df: pd.DataFrame, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Get summary statistics for DataFrame columns.
    
    Args:
        df: DataFrame to analyze
        columns: Specific columns to analyze (default: all numeric)
        
    Returns:
        DataFrame with summary statistics
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    
    return df[columns].describe().T
