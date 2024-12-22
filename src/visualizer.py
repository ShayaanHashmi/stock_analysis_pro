import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    def __init__(self, style='seaborn'):
        """
        Initialize visualizer with a style
        
        Parameters:
        style (str): Matplotlib style to use
        """
        plt.style.use(style)
        
    def plot_price_history(self, data, title="Stock Price History", figsize=(12, 6)):
        """
        Plot stock price history with volume
        
        Parameters:
        data (pandas.DataFrame): Stock price data
        title (str): Plot title
        figsize (tuple): Figure size
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, height_ratios=[3, 1], sharex=True)
        
        # Plot price
        ax1.plot(data.index, data['Close'], label='Close Price')
        ax1.set_title(title)
        ax1.set_ylabel('Price')
        ax1.grid(True)
        ax1.legend()
        
        # Plot volume
        ax2.bar(data.index, data['Volume'])
        ax2.set_ylabel('Volume')
        ax2.grid(True)
        
        plt.tight_layout()
        return fig

    def plot_technical_indicators(self, data, figsize=(15, 10)):
        """
        Plot technical indicators
        
        Parameters:
        data (pandas.DataFrame): Data with technical indicators
        figsize (tuple): Figure size
        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=figsize)
        
        # Price and Moving Averages
        ax1.plot(data.index, data['Close'], label='Price')
        if 'SMA_20' in data.columns:
            ax1.plot(data.index, data['SMA_20'], label='SMA 20')
        if 'SMA_50' in data.columns:
            ax1.plot(data.index, data['SMA_50'], label='SMA 50')
        ax1.set_title('Price and Moving Averages')
        ax1.grid(True)
        ax1.legend()
        
        # RSI
        if 'RSI' in data.columns:
            ax2.plot(data.index, data['RSI'])
            ax2.axhline(y=70, color='r', linestyle='--')
            ax2.axhline(y=30, color='g', linestyle='--')
            ax2.set_title('RSI')
            ax2.grid(True)
        
        # MACD
        if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
            ax3.plot(data.index, data['MACD'], label='MACD')
            ax3.plot(data.index, data['MACD_Signal'], label='Signal')
            ax3.set_title('MACD')
            ax3.grid(True)
            ax3.legend()
        
        plt.tight_layout()
        return fig

    def plot_returns_distribution(self, returns, figsize=(10, 6)):
        """
        Plot distribution of returns
        
        Parameters:
        returns (pandas.Series): Series of returns
        figsize (tuple): Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        sns.histplot(returns, kde=True, ax=ax)
        ax.set_title('Returns Distribution')
        ax.set_xlabel('Returns')
        ax.set_ylabel('Frequency')
        return fig

    def save_plot(self, fig, filename):
        """
        Save plot to file
        
        Parameters:
        fig (matplotlib.figure.Figure): Figure to save
        filename (str): Output filename
        """
        fig.savefig(f'output/{filename}')
        plt.close(fig)
