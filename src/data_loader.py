"""
Data loading and input/output operations for Service Desk Analytics
"""

import pandas as pd
from pathlib import Path
from typing import Union, Optional


def load_csv(filepath: Union[str, Path]) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the loaded data
    """
    return pd.read_csv(filepath)


def load_excel(filepath: Union[str, Path], sheet_name: str = 0) -> pd.DataFrame:
    """
    Load data from an Excel file.
    
    Args:
        filepath: Path to the Excel file
        sheet_name: Sheet to load (default: first sheet)
        
    Returns:
        DataFrame containing the loaded data
    """
    return pd.read_excel(filepath, sheet_name=sheet_name)


def save_csv(df: pd.DataFrame, filepath: Union[str, Path]) -> None:
    """
    Save DataFrame to CSV file.
    
    Args:
        df: DataFrame to save
        filepath: Output file path
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)


def save_excel(df: pd.DataFrame, filepath: Union[str, Path]) -> None:
    """
    Save DataFrame to Excel file.
    
    Args:
        df: DataFrame to save
        filepath: Output file path
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(filepath, index=False)


def get_data_files(directory: Union[str, Path], pattern: str = "*.csv") -> list:
    """
    Get list of data files matching pattern in directory.
    
    Args:
        directory: Directory to search
        pattern: File pattern (default: *.csv)
        
    Returns:
        List of file paths
    """
    directory = Path(directory)
    return sorted(directory.glob(pattern))
