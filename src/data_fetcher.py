import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self):
        self.data = None
        
    def fetch_stock_data(self, symbol, period='1y'):
        """
        Fetch stock data from Yahoo Finance
        
        Parameters:
        symbol (str): Stock symbol
        period (str): Time period - 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        
        Returns:
        pandas.DataFrame: Historical stock data
        """
        try:
            stock = yf.Ticker(symbol)
            self.data = stock.history(period=period)
            return self.data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def fetch_multiple_stocks(self, symbols, period='1y'):
        """
        Fetch data for multiple stocks
        
        Parameters:
        symbols (list): List of stock symbols
        period (str): Time period
        
        Returns:
        dict: Dictionary with stock symbols as keys and DataFrames as values
        """
        stock_data = {}
        for symbol in symbols:
            data = self.fetch_stock_data(symbol, period)
            if data is not None:
                stock_data[symbol] = data
        return stock_data
    
    def get_stock_info(self, symbol):
        """
        Get basic information about a stock
        
        Parameters:
        symbol (str): Stock symbol
        
        Returns:
        dict: Stock information
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return info
        except Exception as e:
            print(f"Error fetching info for {symbol}: {str(e)}")
            return None

    def get_latest_price(self, symbol):
        """
        Get the latest price for a stock
        
        Parameters:
        symbol (str): Stock symbol
        
        Returns:
        float: Latest stock price
        """
        try:
            stock = yf.Ticker(symbol)
            return stock.history(period='1d')['Close'].iloc[-1]
        except Exception as e:
            print(f"Error fetching latest price for {symbol}: {str(e)}")
            return None
