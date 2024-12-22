import yfinance as yf
import pandas as pd
from datetime import datetime

class FundamentalAnalyzer:
    def __init__(self):
        """Initialize the Fundamental Analyzer"""
        self.metrics = {}
        
    def analyze_stock(self, symbol):
        """
        Perform fundamental analysis on a stock
        
        Parameters:
        symbol (str): Stock symbol
        
        Returns:
        dict: Fundamental analysis results
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Basic company information
            self.metrics['Company_Name'] = info.get('longName', 'N/A')
            self.metrics['Sector'] = info.get('sector', 'N/A')
            self.metrics['Industry'] = info.get('industry', 'N/A')
            
            # Valuation metrics
            self.metrics['Market_Cap'] = info.get('marketCap', 'N/A')
            self.metrics['PE_Ratio'] = info.get('trailingPE', 'N/A')
            self.metrics['Forward_PE'] = info.get('forwardPE', 'N/A')
            self.metrics['PB_Ratio'] = info.get('priceToBook', 'N/A')
            
            # Financial metrics
            self.metrics['Revenue'] = info.get('totalRevenue', 'N/A')
            self.metrics['Revenue_Growth'] = info.get('revenueGrowth', 'N/A')
            self.metrics['Profit_Margin'] = info.get('profitMargins', 'N/A')
            self.metrics['Operating_Margin'] = info.get('operatingMargins', 'N/A')
            
            # Dividend information
            self.metrics['Dividend_Yield'] = info.get('dividendYield', 'N/A')
            self.metrics['Payout_Ratio'] = info.get('payoutRatio', 'N/A')
            
            # Financial health
            self.metrics['Current_Ratio'] = info.get('currentRatio', 'N/A')
            self.metrics['Debt_To_Equity'] = info.get('debtToEquity', 'N/A')
            
            return self.metrics
            
        except Exception as e:
            print(f"Error analyzing {symbol}: {str(e)}")
            return None
    
    def get_financial_statements(self, symbol):
        """
        Get financial statements for a stock
        
        Parameters:
        symbol (str): Stock symbol
        
        Returns:
        dict: Dictionary containing financial statements
        """
        try:
            stock = yf.Ticker(symbol)
            
            statements = {
                'Income_Statement': stock.financials,
                'Balance_Sheet': stock.balance_sheet,
                'Cash_Flow': stock.cashflow
            }
            
            return statements
            
        except Exception as e:
            print(f"Error fetching financial statements for {symbol}: {str(e)}")
            return None
    
    def calculate_financial_ratios(self, statements):
        """
        Calculate financial ratios from statements
        
        Parameters:
        statements (dict): Financial statements
        
        Returns:
        dict: Financial ratios
        """
        ratios = {}
        
        if statements and all(k in statements for k in ['Income_Statement', 'Balance_Sheet']):
            try:
                income = statements['Income_Statement']
                balance = statements['Balance_Sheet']
                
                # Calculate ROE
                if 'Net Income' in income.index and 'Total Stockholder Equity' in balance.index:
                    net_income = income.loc['Net Income'].iloc[0]
                    equity = balance.loc['Total Stockholder Equity'].iloc[0]
                    ratios['ROE'] = net_income / equity if equity != 0 else 'N/A'
                
                # Calculate ROA
                if 'Net Income' in income.index and 'Total Assets' in balance.index:
                    net_income = income.loc['Net Income'].iloc[0]
                    assets = balance.loc['Total Assets'].iloc[0]
                    ratios['ROA'] = net_income / assets if assets != 0 else 'N/A'
                
            except Exception as e:
                print(f"Error calculating ratios: {str(e)}")
                
        return ratios
    
    def get_analyst_recommendations(self, symbol):
        """
        Get analyst recommendations for a stock
        
        Parameters:
        symbol (str): Stock symbol
        
        Returns:
        pandas.DataFrame: Analyst recommendations
        """
        try:
            stock = yf.Ticker(symbol)
            return stock.recommendations
        except Exception as e:
            print(f"Error fetching analyst recommendations for {symbol}: {str(e)}")
            return None
    
    def format_metrics(self):
        """
        Format metrics for display
        
        Returns:
        dict: Formatted metrics
        """
        formatted = {}
        for key, value in self.metrics.items():
            if isinstance(value, float):
                if 'Ratio' in key or 'Margin' in key or 'Growth' in key or 'Yield' in key:
                    formatted[key] = f"{value:.2%}" if value != 'N/A' else 'N/A'
                else:
                    formatted[key] = f"{value:,.2f}" if value != 'N/A' else 'N/A'
            else:
                formatted[key] = value
        return formatted
