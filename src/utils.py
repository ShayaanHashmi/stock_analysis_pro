import pandas as pd
import numpy as np
from datetime import datetime
import os

def create_output_directory():
    """Create output directory if it doesn't exist"""
    if not os.path.exists('output'):
        os.makedirs('output')

def calculate_returns(data):
    """
    Calculate daily and cumulative returns
    
    Parameters:
    data (pandas.DataFrame): Stock price data with 'Close' column
    
    Returns:
    tuple: (daily_returns, cumulative_returns)
    """
    daily_returns = data['Close'].pct_change()
    cumulative_returns = (1 + daily_returns).cumprod()
    return daily_returns, cumulative_returns

def calculate_volatility(returns, window=30):
    """
    Calculate rolling volatility
    
    Parameters:
    returns (pandas.Series): Daily returns
    window (int): Rolling window size
    
    Returns:
    pandas.Series: Rolling volatility
    """
    return returns.rolling(window=window).std() * np.sqrt(252)

def export_to_csv(data, filename):
    """
    Export DataFrame to CSV
    
    Parameters:
    data (pandas.DataFrame): Data to export
    filename (str): Output filename
    """
    create_output_directory()
    filepath = os.path.join('output', filename)
    data.to_csv(filepath)
    print(f"Data exported to {filepath}")

def format_number(number):
    """
    Format large numbers for display
    
    Parameters:
    number (float): Number to format
    
    Returns:
    str: Formatted number
    """
    if number >= 1e9:
        return f"{number/1e9:.2f}B"
    elif number >= 1e6:
        return f"{number/1e6:.2f}M"
    elif number >= 1e3:
        return f"{number/1e3:.2f}K"
    else:
        return f"{number:.2f}"
