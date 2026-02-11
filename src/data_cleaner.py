"""
Data cleaning and validation functions for Service Desk Analytics
"""

import pandas as pd
from typing import List, Optional
import numpy as np


def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Remove duplicate rows from DataFrame.
    
    Args:
        df: Input DataFrame
        subset: Column names to consider for duplication check (default: all columns)
        
    Returns:
        DataFrame with duplicates removed
    """
    return df.drop_duplicates(subset=subset)


def remove_null_values(df: pd.DataFrame, columns: Optional[List[str]] = None, 
                      how: str = "any") -> pd.DataFrame:
    """
    Remove rows with null values.
    
    Args:
        df: Input DataFrame
        columns: Specific columns to check for nulls
        how: "any" or "all" - remove rows where any or all values are null
        
    Returns:
        DataFrame with null values removed
    """
    if columns:
        return df.dropna(subset=columns, how=how)
    return df.dropna(how=how)


def standardize_datetime(df: pd.DataFrame, column: str, 
                        format: Optional[str] = None) -> pd.DataFrame:
    """
    Standardize datetime column format.
    
    Args:
        df: Input DataFrame
        column: Column name containing dates
        format: Expected datetime format string
        
    Returns:
        DataFrame with standardized datetime column
    """
    df_copy = df.copy()
    df_copy[column] = pd.to_datetime(df_copy[column], format=format)
    return df_copy


def standardize_text(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Standardize text columns (clean whitespace, lowercase, etc).
    
    Args:
        df: Input DataFrame
        columns: List of text column names to standardize
        
    Returns:
        DataFrame with standardized text columns
    """
    df_copy = df.copy()
    for col in columns:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].astype(str).str.strip().str.lower()
    return df_copy


def fill_missing_values(df: pd.DataFrame, strategy: str = "mean",
                       columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Fill missing values using specified strategy.
    
    Args:
        df: Input DataFrame
        strategy: "mean", "median", "forward_fill", "backward_fill", or specific value
        columns: Specific columns to fill
        
    Returns:
        DataFrame with missing values filled
    """
    df_copy = df.copy()
    target_cols = columns if columns else df_copy.columns
    
    if strategy == "mean":
        df_copy[target_cols] = df_copy[target_cols].fillna(df_copy[target_cols].mean())
    elif strategy == "median":
        df_copy[target_cols] = df_copy[target_cols].fillna(df_copy[target_cols].median())
    elif strategy == "forward_fill":
        df_copy[target_cols] = df_copy[target_cols].fillna(method='ffill')
    elif strategy == "backward_fill":
        df_copy[target_cols] = df_copy[target_cols].fillna(method='bfill')
    else:
        df_copy[target_cols] = df_copy[target_cols].fillna(strategy)
    
    return df_copy


def validate_data_types(df: pd.DataFrame, expected_types: dict) -> dict:
    """
    Validate that DataFrame columns have expected types.
    
    Args:
        df: Input DataFrame
        expected_types: Dictionary mapping column names to expected types
        
    Returns:
        Dictionary with validation results
    """
    results = {"valid": True, "issues": []}
    
    for col, expected_type in expected_types.items():
        if col not in df.columns:
            results["issues"].append(f"Column '{col}' not found")
            results["valid"] = False
        elif not df[col].dtype == expected_type:
            results["issues"].append(
                f"Column '{col}' is {df[col].dtype}, expected {expected_type}"
            )
            results["valid"] = False
    
    return results
