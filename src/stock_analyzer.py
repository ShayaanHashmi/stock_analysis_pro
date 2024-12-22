import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import time
import warnings
warnings.filterwarnings('ignore')

class StockAnalyzer:
    def __init__(self):
        self.output_dir = 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_stock_data(self, symbol, period='1y'):
        """Fetch stock data using yfinance"""
        try:
            time.sleep(1)  # Rate limiting
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            if df.empty:
                print(f"No data received for {symbol}")
                return None
            return df
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None

    def calculate_technical_indicators(self, df):
        """Calculate comprehensive technical indicators"""
        try:
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            # MACD
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

            # Moving Averages
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
            df['SMA_200'] = df['Close'].rolling(window=200).mean()

            # Bollinger Bands
            df['BB_middle'] = df['Close'].rolling(window=20).mean()
            df['BB_upper'] = df['BB_middle'] + 2*df['Close'].rolling(window=20).std()
            df['BB_lower'] = df['BB_middle'] - 2*df['Close'].rolling(window=20).std()

            # Stochastic Oscillator
            low_min = df['Low'].rolling(window=14).min()
            high_max = df['High'].rolling(window=14).max()
            df['Stochastic_K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
            df['Stochastic_D'] = df['Stochastic_K'].rolling(window=3).mean()

            # Average True Range (ATR)
            high_low = df['High'] - df['Low']
            high_close = np.abs(df['High'] - df['Close'].shift())
            low_close = np.abs(df['Low'] - df['Close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = np.max(ranges, axis=1)
            df['ATR'] = true_range.rolling(window=14).mean()

            # On-Balance Volume (OBV)
            df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()

            # Rate of Change (ROC)
            df['ROC'] = ((df['Close'] - df['Close'].shift(10)) / df['Close'].shift(10)) * 100

            # Money Flow Index (MFI)
            typical_price = (df['High'] + df['Low'] + df['Close']) / 3
            money_flow = typical_price * df['Volume']
            positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(window=14).sum()
            negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(window=14).sum()
            mfi_ratio = positive_flow / negative_flow
            df['MFI'] = 100 - (100 / (1 + mfi_ratio))

            # Relative Vigor Index (RVI)
            close_open = df['Close'] - df['Open']
            high_low = df['High'] - df['Low']
            df['RVI'] = close_open.rolling(window=10).mean() / high_low.rolling(window=10).mean()

            return df
        except Exception as e:
            print(f"Error calculating indicators: {str(e)}")
            return None
    def generate_signals(self, df):
        """Generate comprehensive trading signals"""
        signals = {}
        
        # RSI signals
        last_rsi = df['RSI'].iloc[-1]
        if last_rsi > 70:
            signals['RSI'] = 'Overbought'
        elif last_rsi < 30:
            signals['RSI'] = 'Oversold'
        else:
            signals['RSI'] = 'Neutral'

        # MACD signals
        if df['MACD'].iloc[-1] > df['Signal_Line'].iloc[-1]:
            signals['MACD'] = 'Buy'
        else:
            signals['MACD'] = 'Sell'

        # Moving Average signals
        if df['Close'].iloc[-1] > df['SMA_200'].iloc[-1]:
            signals['Long_Term_Trend'] = 'Bullish'
        else:
            signals['Long_Term_Trend'] = 'Bearish'

        # Stochastic signals
        if df['Stochastic_K'].iloc[-1] > 80:
            signals['Stochastic'] = 'Overbought'
        elif df['Stochastic_K'].iloc[-1] < 20:
            signals['Stochastic'] = 'Oversold'
        else:
            signals['Stochastic'] = 'Neutral'

        # MFI signals
        if df['MFI'].iloc[-1] > 80:
            signals['MFI'] = 'Overbought'
        elif df['MFI'].iloc[-1] < 20:
            signals['MFI'] = 'Oversold'
        else:
            signals['MFI'] = 'Neutral'

        # Bollinger Bands signals
        if df['Close'].iloc[-1] > df['BB_upper'].iloc[-1]:
            signals['Bollinger'] = 'Above Upper Band'
        elif df['Close'].iloc[-1] < df['BB_lower'].iloc[-1]:
            signals['Bollinger'] = 'Below Lower Band'
        else:
            signals['Bollinger'] = 'Within Bands'

        # Volume signals
        if df['OBV'].iloc[-1] > df['OBV'].iloc[-2]:
            signals['Volume_Trend'] = 'Increasing'
        else:
            signals['Volume_Trend'] = 'Decreasing'

        # Volatility (using ATR)
        atr_percent = (df['ATR'].iloc[-1] / df['Close'].iloc[-1]) * 100
        if atr_percent > 2:
            signals['Volatility'] = 'High'
        elif atr_percent < 1:
            signals['Volatility'] = 'Low'
        else:
            signals['Volatility'] = 'Moderate'

        return signals

    def generate_recommendation(self, tech_analysis, signals):
        """Generate a weighted recommendation based on multiple technical indicators"""
        try:
            # Initialize scoring system
            score = 0
            max_score = 0
            reasons = []

            # 1. Trend Analysis (Weight: 30%)
            max_score += 30
            if signals['Long_Term_Trend'] == 'Bullish':
                score += 30
                reasons.append("Long-term trend is bullish")
            else:
                reasons.append("Long-term trend is bearish")

            # 2. RSI Analysis (Weight: 15%)
            max_score += 15
            rsi = tech_analysis['rsi']
            if rsi < 30:
                score += 15
                reasons.append(f"RSI ({rsi:.2f}) indicates oversold conditions")
            elif rsi > 70:
                reasons.append(f"RSI ({rsi:.2f}) indicates overbought conditions")
            else:
                score += 7.5
                reasons.append(f"RSI ({rsi:.2f}) is neutral")

            # 3. MACD Signal (Weight: 20%)
            max_score += 20
            if signals['MACD'] == 'Buy':
                score += 20
                reasons.append("MACD shows bullish crossover")
            else:
                reasons.append("MACD shows bearish crossover")

            # 4. Volume Trend (Weight: 15%)
            max_score += 15
            if signals['Volume_Trend'] == 'Increasing':
                score += 15
                reasons.append("Volume is trending up")
            else:
                reasons.append("Volume is trending down")

            # 5. Bollinger Bands Position (Weight: 10%)
            max_score += 10
            if signals['Bollinger'] == 'Below Lower Band':
                score += 10
                reasons.append("Price below lower Bollinger Band suggests oversold")
            elif signals['Bollinger'] == 'Above Upper Band':
                reasons.append("Price above upper Bollinger Band suggests overbought")
            else:
                score += 5
                reasons.append("Price within Bollinger Bands")

            # 6. Stochastic Signal (Weight: 10%)
            max_score += 10
            if signals['Stochastic'] == 'Oversold':
                score += 10
                reasons.append("Stochastic indicates oversold conditions")
            elif signals['Stochastic'] == 'Overbought':
                reasons.append("Stochastic indicates overbought conditions")
            else:
                score += 5
                reasons.append("Stochastic is neutral")

            # Calculate final score as a percentage
            final_score = (score / max_score) * 100

            # Generate recommendation based on score
            if final_score >= 80:
                recommendation = "Strong Buy"
            elif final_score >= 60:
                recommendation = "Buy"
            elif final_score >= 40:
                recommendation = "Hold"
            elif final_score >= 20:
                recommendation = "Sell"
            else:
                recommendation = "Strong Sell"

            # Create detailed reasoning
            reasoning = " | ".join(reasons)

            return recommendation, final_score, reasoning

        except Exception as e:
            print(f"Error generating recommendation: {str(e)}")
            return "Hold", 50.0, "Error in analysis"
    def generate_excel_summary(self, symbols_data):
        """Generate a comprehensive Excel summary of all analyzed stocks"""
        try:
            # Create Excel writer object
            excel_path = f'{self.output_dir}/stock_analysis_summary_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
            writer = pd.ExcelWriter(excel_path, engine='openpyxl')
            
            # Summary DataFrame
            summary_data = []
            signals_data = []
            technical_data = []
            
            for symbol, data in symbols_data.items():
                if not data or 'technical_analysis' not in data:
                    continue
                    
                tech_analysis = data['technical_analysis']
                signals = tech_analysis['signals']
                
                # Calculate technical strength
                bullish_signals = sum(1 for signal in signals.values() 
                                   if signal in ['Buy', 'Bullish', 'Increasing'])
                total_signals = len(signals)
                strength = (bullish_signals / total_signals) * 100
                
                # Get recommendation
                recommendation, confidence_score, reasoning = self.generate_recommendation(
                    tech_analysis, signals)
                
                # Basic Summary
                summary_data.append({
                    'Symbol': symbol,
                    'Last Price': tech_analysis['last_price'],
                    'RSI': tech_analysis['rsi'],
                    'MACD': tech_analysis['macd'],
                    'Volume': tech_analysis['volume'],
                    'Analysis Date': datetime.now().strftime("%Y-%m-%d")
                })
                
                # Signals
                signals['Symbol'] = symbol
                signals_data.append(signals)
                
                # Technical Analysis Details
                technical_data.append({
                    'Symbol': symbol,
                    'Price': tech_analysis['last_price'],
                    'Recommendation': recommendation,
                    'Confidence Score': f"{confidence_score:.1f}%",
                    'Analysis Reasoning': reasoning,
                    'RSI': tech_analysis['rsi'],
                    'MACD': tech_analysis['macd'],
                    'Volume': tech_analysis['volume'],
                    'Technical Strength': f"{strength:.1f}%",
                    'RSI Status': 'Overbought' if tech_analysis['rsi'] > 70 else 'Oversold' if tech_analysis['rsi'] < 30 else 'Neutral',
                    'MACD Signal': signals.get('MACD', 'N/A'),
                    'Trend': signals.get('Long_Term_Trend', 'N/A'),
                    'Volume Trend': signals.get('Volume_Trend', 'N/A'),
                    'Volatility': signals.get('Volatility', 'N/A')
                })
            
            # Create DataFrames
            summary_df = pd.DataFrame(summary_data)
            signals_df = pd.DataFrame(signals_data)
            technical_df = pd.DataFrame(technical_data)
            
            # Sort DataFrames by Symbol
            summary_df = summary_df.sort_values('Symbol')
            signals_df = signals_df.sort_values('Symbol')
            technical_df = technical_df.sort_values('Symbol')
            
            # Write to Excel
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            signals_df.to_excel(writer, sheet_name='Signals', index=False)
            technical_df.to_excel(writer, sheet_name='Technical Analysis', index=False)
            
            # Add Rankings sheet
            rankings_data = {
                'Highest RSI': summary_df.nlargest(10, 'RSI')[['Symbol', 'RSI']],
                'Lowest RSI': summary_df.nsmallest(10, 'RSI')[['Symbol', 'RSI']],
                'Highest MACD': summary_df.nlargest(10, 'MACD')[['Symbol', 'MACD']],
                'Highest Volume': summary_df.nlargest(10, 'Volume')[['Symbol', 'Volume']]
            }
            
            start_row = 0
            rankings_sheet = writer.book.create_sheet('Rankings')
            
            for title, df in rankings_data.items():
                # Write title
                rankings_sheet.cell(row=start_row + 1, column=1, value=title)
                
                # Write data
                for r_idx, row in enumerate(df.values):
                    for c_idx, value in enumerate(row):
                        rankings_sheet.cell(row=start_row + r_idx + 2, 
                                         column=c_idx + 1, 
                                         value=value)
                
                start_row += len(df) + 3
            
            # Add Recommendations Rankings
            recommendations_df = pd.DataFrame(technical_data)
            
            # Strong Buy and Buy recommendations
            buy_recommendations = recommendations_df[
                recommendations_df['Recommendation'].isin(['Strong Buy', 'Buy'])
            ][['Symbol', 'Recommendation', 'Confidence Score', 'Price']].sort_values('Confidence Score', ascending=False)
            
            # Strong Sell and Sell recommendations
            sell_recommendations = recommendations_df[
                recommendations_df['Recommendation'].isin(['Strong Sell', 'Sell'])
            ][['Symbol', 'Recommendation', 'Confidence Score', 'Price']].sort_values('Confidence Score', ascending=True)
            
            # Add to Rankings sheet
            rankings_sheet.cell(row=start_row + 1, column=1, value='Top Buy Recommendations')
            for r_idx, row in enumerate(buy_recommendations.head(10).values):
                for c_idx, value in enumerate(row):
                    rankings_sheet.cell(row=start_row + r_idx + 2, column=c_idx + 1, value=value)
            
            start_row += len(buy_recommendations.head(10)) + 3
            
            rankings_sheet.cell(row=start_row + 1, column=1, value='Top Sell Recommendations')
            for r_idx, row in enumerate(sell_recommendations.head(10).values):
                for c_idx, value in enumerate(row):
                    rankings_sheet.cell(row=start_row + r_idx + 2, column=c_idx + 1, value=value)

            # Auto-adjust columns width
            for sheet in writer.book.sheetnames:
                worksheet = writer.book[sheet]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    worksheet.column_dimensions[column_letter].width = max_length + 2
            
            # Save the Excel file
            writer.close()
            
            print(f"\nExcel summary report generated: {excel_path}")
            return excel_path
            
        except Exception as e:
            print(f"Error generating Excel summary: {str(e)}")
            return None
    def plot_technical_analysis(self, df, symbol):
        """Create technical analysis plots"""
        try:
            # Price, Moving Averages, and Bollinger Bands
            plt.figure(figsize=(12, 6))
            plt.plot(df.index, df['Close'], label='Price', alpha=0.5)
            plt.plot(df.index, df['SMA_20'], label='20-day SMA', alpha=0.7)
            plt.plot(df.index, df['SMA_50'], label='50-day SMA', alpha=0.7)
            plt.plot(df.index, df['BB_upper'], label='BB Upper', linestyle='--', alpha=0.7)
            plt.plot(df.index, df['BB_lower'], label='BB Lower', linestyle='--', alpha=0.7)
            plt.title(f'{symbol} Price and Technical Indicators')
            plt.legend()
            plt.savefig(f'{self.output_dir}/{symbol}_technical.png')
            plt.close()

            # Momentum Indicators
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
            
            # RSI
            ax1.plot(df.index, df['RSI'], label='RSI')
            ax1.axhline(y=70, color='r', linestyle='--')
            ax1.axhline(y=30, color='g', linestyle='--')
            ax1.set_title('RSI')
            ax1.legend()

            # MACD
            ax2.plot(df.index, df['MACD'], label='MACD')
            ax2.plot(df.index, df['Signal_Line'], label='Signal Line')
            ax2.set_title('MACD')
            ax2.legend()

            # Volume
            ax3.bar(df.index, df['Volume'], label='Volume', alpha=0.5)
            ax3.set_title('Volume')
            
            plt.tight_layout()
            plt.savefig(f'{self.output_dir}/{symbol}_momentum.png')
            plt.close()

        except Exception as e:
            print(f"Error creating plots: {str(e)}")

    def analyze_stock(self, symbol, period='1y'):
        """Perform complete stock analysis"""
        try:
            # Get data
            df = self.get_stock_data(symbol, period)
            if df is None or df.empty:
                return None

            # Calculate indicators
            df = self.calculate_technical_indicators(df)
            if df is None:
                return None

            # Generate signals
            signals = self.generate_signals(df)

            # Create plots
            self.plot_technical_analysis(df, symbol)

            # Prepare results
            results = {
                'technical_analysis': {
                    'signals': signals,
                    'last_price': df['Close'].iloc[-1],
                    'volume': df['Volume'].iloc[-1],
                    'rsi': df['RSI'].iloc[-1],
                    'macd': df['MACD'].iloc[-1],
                    'stochastic_k': df['Stochastic_K'].iloc[-1],
                    'mfi': df['MFI'].iloc[-1],
                    'atr': df['ATR'].iloc[-1],
                    'roc': df['ROC'].iloc[-1]
                },
                'data': df
            }

            return results

        except Exception as e:
            print(f"Error in analysis: {str(e)}")
            return None

    def export_results(self, results, symbol):
        """Export analysis results to files"""
        try:
            if results and 'data' in results:
                # Export technical data
                results['data'].to_csv(f'{self.output_dir}/{symbol}_technical_data.csv')
                
                # Export signals and metrics
                if 'technical_analysis' in results:
                    tech_analysis = results['technical_analysis']
                    metrics_df = pd.DataFrame({
                        'Metric': tech_analysis.keys(),
                        'Value': tech_analysis.values()
                    })
                    metrics_df.to_csv(f'{self.output_dir}/{symbol}_analysis_summary.csv', index=False)

            print(f"Data exported for {symbol}")
        except Exception as e:
            print(f"Error exporting results: {str(e)}")

    def calculate_technical_strength(self, tech_analysis, signals):
        """Calculate overall technical strength as a percentage"""
        try:
            total_signals = 0
            bullish_signals = 0

            # RSI
            if tech_analysis['rsi'] < 30:
                bullish_signals += 1
            total_signals += 1

            # MACD
            if signals.get('MACD') == 'Buy':
                bullish_signals += 1
            total_signals += 1

            # Trend
            if signals.get('Long_Term_Trend') == 'Bullish':
                bullish_signals += 1
            total_signals += 1

            # Volume
            if signals.get('Volume_Trend') == 'Increasing':
                bullish_signals += 1
            total_signals += 1

            # Stochastic
            if signals.get('Stochastic') == 'Oversold':
                bullish_signals += 1
            total_signals += 1

            # Calculate percentage
            strength = (bullish_signals / total_signals) * 100
            return strength

        except Exception as e:
            print(f"Error calculating technical strength: {str(e)}")
            return 50.0  # Return neutral strength in case of error
