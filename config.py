# Stock list to analyze
STOCK_LIST = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 
    'NVDA', 'TSLA', 'JPM', 'V', 'WMT'
]

# Time periods
DEFAULT_PERIOD = "1y"
LONG_PERIOD = "5y"

# Technical Analysis Parameters
TECHNICAL_PARAMS = {
    'RSI_PERIOD': 14,
    'SMA_SHORT': 20,
    'SMA_LONG': 50,
    'EMA_SHORT': 12,
    'EMA_LONG': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Fundamental Analysis Thresholds
FUNDAMENTAL_THRESHOLDS = {
    'MIN_MARKET_CAP': 1000000000,  # 1B
    'MAX_PE': 50,
    'MIN_PROFIT_MARGIN': 0.10,
    'MAX_DEBT_TO_EQUITY': 2.0,
    'MIN_CURRENT_RATIO': 1.5,
    'MIN_ROE': 0.15
}

# Scoring Weights
WEIGHTS = {
    'TECHNICAL': 0.4,
    'FUNDAMENTAL': 0.4,
    'SENTIMENT': 0.2
}

# Output Settings
OUTPUT_DIR = "output"
EXCEL_FILENAME = "stock_analysis_report.xlsx"
