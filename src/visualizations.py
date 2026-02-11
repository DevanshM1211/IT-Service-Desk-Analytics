"""
Visualization and charting functions for Service Desk Analytics
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from typing import Union, Optional, List


def save_chart(fig, filepath: Union[str, Path], format: str = "html") -> None:
    """
    Save plotly figure to file.
    
    Args:
        fig: Plotly figure object
        filepath: Output file path
        format: Output format - "html", "png", "jpg", "svg", "pdf"
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    if format == "html":
        fig.write_html(filepath)
    elif format in ["png", "jpg", "svg", "pdf"]:
        fig.write_image(filepath)
    else:
        raise ValueError(f"Unsupported format: {format}")


def create_time_series(df: pd.DataFrame, date_col: str, value_col: str,
                      title: str = "Time Series Analysis") -> go.Figure:
    """
    Create a time series line chart.
    
    Args:
        df: Input DataFrame
        date_col: Column name for dates
        value_col: Column name for values
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = px.line(df, x=date_col, y=value_col, 
                  title=title,
                  labels={date_col: "Date", value_col: "Value"})
    fig.update_layout(hovermode='x unified')
    return fig


def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str,
                    title: str = "Bar Chart") -> go.Figure:
    """
    Create a bar chart.
    
    Args:
        df: Input DataFrame
        x_col: Column for X-axis
        y_col: Column for Y-axis values
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def create_distribution(df: pd.DataFrame, column: str,
                       bins: int = 30, title: str = "Distribution") -> go.Figure:
    """
    Create a histogram for distribution analysis.
    
    Args:
        df: Input DataFrame
        column: Column to analyze
        bins: Number of bins
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = px.histogram(df, x=column, nbins=bins, title=title)
    return fig


def create_pie_chart(df: pd.DataFrame, values_col: str, names_col: str,
                    title: str = "Distribution") -> go.Figure:
    """
    Create a pie chart.
    
    Args:
        df: Input DataFrame prepared with aggregated values
        values_col: Column containing values for pie slices
        names_col: Column containing labels
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = px.pie(df, values=values_col, names=names_col, title=title)
    return fig


def create_box_plot(df: pd.DataFrame, y_col: str, x_col: Optional[str] = None,
                   title: str = "Box Plot") -> go.Figure:
    """
    Create a box plot for distribution and outlier detection.
    
    Args:
        df: Input DataFrame
        y_col: Column for Y-axis values
        x_col: Optional column for grouping
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = px.box(df, y=y_col, x=x_col, title=title)
    return fig


def create_scatter(df: pd.DataFrame, x_col: str, y_col: str,
                  color_col: Optional[str] = None, size_col: Optional[str] = None,
                  title: str = "Scatter Plot") -> go.Figure:
    """
    Create a scatter plot.
    
    Args:
        df: Input DataFrame
        x_col: Column for X-axis
        y_col: Column for Y-axis
        color_col: Optional column for color coding
        size_col: Optional column for bubble size
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col,
                     title=title, hover_data=df.columns)
    return fig
