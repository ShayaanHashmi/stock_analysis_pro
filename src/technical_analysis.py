import pandas as pd
import numpy as np
import ta

class TechnicalAnalyzer:
    def __init__(self, data):
        """
        Initialize with price data
        
        Parameters:
        data (pandas.DataFrame): DataFrame with OHLCV data
        """
        self.data = data
        self.indicators = {}

    def add_all_indicators(self):
        """Add all technical indicators to the dataset"""
        self.add_moving_averages()
        self.add_rsi()
        self.add_macd()
        self.add_bollinger_bands()
        self.add_atr()
        return self.data

    def add_moving_averages(self, periods=[20, 50, 200]):
        """
        Add Simple Moving Averages
        
        Parameters:
        periods (list): List of periods for moving averages
        """
        for period in periods:
            self.data[f'SMA_{period}'] = ta.trend.sma_indicator(self.data['Close'], window=period)
            self.data[f'EMA_{period}'] = ta.trend.ema_indicator(self.data['Close'], window=period)

    def add_rsi(self, period=14):
        """
        Add Relative Strength Index
        
        Parameters:
        period (int): Period for RSI calculation
        """
        self.data['RSI'] = ta.momentum.rsi(self.data['Close'], window=period)

    def add_macd(self, fast=12, slow=26, signal=9):
        """
        Add MACD indicator
        
        Parameters:
        fast (int): Fast period
        slow (int): Slow period
        signal (int): Signal period
        """
        self.data['MACD'] = ta.trend.macd(self.data['Close'], 
                                         window_slow=slow, 
                                         window_fast=fast)
        self.data['MACD_Signal'] = ta.trend.macd_signal(self.data['Close'], 
                                                       window_slow=slow, 
                                                       window_fast=fast, 
                                                       window_sign=signal)

    def add_bollinger_bands(self, window=20, window_dev=2):
        """
        Add Bollinger Bands
        
        Parameters:
        window (int): Moving average window
        window_dev (int): Standard deviation multiplier
        """
        self.data['BB_Upper'] = ta.volatility.bollinger_hband(self.data['Close'], 
                                                             window=window, 
                                                             window_dev=window_dev)
        self.data['BB_Lower'] = ta.volatility.bollinger_lband(self.data['Close'], 
                                                             window=window, 
                                                             window_dev=window_dev)
        self.data['BB_Middle'] = ta.volatility.bollinger_mavg(self.data['Close'], 
                                                             window=window)

    def add_atr(self, window=14):
        """
        Add Average True Range
        
        Parameters:
        window (int): Period for ATR calculation
        """
        self.data['ATR'] = ta.volatility.average_true_range(high=self.data['High'],
                                                           low=self.data['Low'],
                                                           close=self.data['Close'],
                                                           window=window)

    def generate_signals(self):
        """
        Generate trading signals based on technical indicators
        
        Returns:
        pandas.DataFrame: DataFrame with trading signals
        """
        signals = pd.DataFrame(index=self.data.index)
        
        # RSI signals
        signals['RSI_Signal'] = np.where(self.data['RSI'] < 30, 1, 
                                       np.where(self.data['RSI'] > 70, -1, 0))
        
        # MACD signals
        signals['MACD_Signal'] = np.where(self.data['MACD'] > self.data['MACD_Signal'], 1, -1)
        
        # Bollinger Bands signals
        signals['BB_Signal'] = np.where(self.data['Close'] < self.data['BB_Lower'], 1,
                                      np.where(self.data['Close'] > self.data['BB_Upper'], -1, 0))
        
        # Moving Average signals
        signals['MA_Signal'] = np.where(self.data['Close'] > self.data['SMA_50'], 1, -1)
        
        # Combined signal
        signals['Combined_Signal'] = (signals['RSI_Signal'] + 
                                    signals['MACD_Signal'] + 
                                    signals['BB_Signal'] + 
                                    signals['MA_Signal'])
        
        return signals

    def get_summary(self):
        """
        Get technical analysis summary
        
        Returns:
        dict: Summary of technical indicators
        """
        latest = self.data.iloc[-1]
        
        summary = {
            'RSI': latest['RSI'],
            'MACD': latest['MACD'],
            'MACD_Signal': latest['MACD_Signal'],
            'BB_Position': (latest['Close'] - latest['BB_Lower']) / (latest['BB_Upper'] - latest['BB_Lower']),
            'SMA_50': latest['SMA_50'],
            'Current_Price': latest['Close']
        }
        
        return summary
