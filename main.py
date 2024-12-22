import warnings
warnings.filterwarnings("ignore")

from src.stock_analyzer import StockAnalyzer
import yfinance as yf
import time

def get_stock_list():
    """Returns a list of popular stocks"""
    return [
        # Technology
        "AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "TSM", "AVGO", "ORCL", "CSCO", 
        "ADBE", "CRM", "INTC", "AMD", "QCOM",
        # Finance
        "JPM", "BAC", "WFC", "GS", "MS", "BLK", "C", "SPGI", "AXP", "V", "MA", "PYPL", 
        "SCHW",
        # Healthcare
        "JNJ", "UNH", "PFE", "MRK", "ABT", "TMO", "DHR", "BMY", "AMGN", "LLY", "GILD",
        # Consumer
        "AMZN", "WMT", "PG", "KO", "PEP", "COST", "MCD", "NKE", "SBUX", "DIS", "HD", 
        "LOW",
        # Industrial
        "CAT", "DE", "BA", "GE", "MMM", "HON", "UPS", "FDX", "RTX", "LMT",
        # Energy
        "XOM", "CVX", "COP", "SLB", "EOG", "PXD", "MPC",
        # Telecommunications
        "VZ", "T", "TMUS",
        # Real Estate
        "AMT", "PLD", "CCI", "EQIX",
        # Materials
        "LIN", "APD", "ECL", "DD",
        # Utilities
        "NEE", "DUK", "SO", "D",
        # Auto
        "F", "GM", "TM",
        # Retail
        "TGT", "LULU", "ROST", "TJX",
        # Entertainment
        "NFLX", "CMCSA", "EA", "ATVI",
        # Semiconductor
        "AMAT", "KLAC", "LRCX", "MU",
        # Internet
        "BABA", "JD", "BIDU", "SHOP",
        # Cannabis
        "CGC", "TLRY", "ACB",
        # Gaming
        "TTWO", "RBLX", "U",
        # Fintech
        "SQ", "COIN", "AFRM",
        # EV
        "NIO", "RIVN", "LCID"
    ]

def main():
    # Create analyzer instance
    analyzer = StockAnalyzer()
    
    # Get list of stocks
    symbols = get_stock_list()
    print(f"Starting analysis for {len(symbols)} stocks...")
    
    # Store all results
    all_results = {}
    failed_symbols = []
    
    # Progress tracking
    total_stocks = len(symbols)
    start_time = time.time()
    
    for index, symbol in enumerate(symbols, 1):
        print(f"\n{'='*50}")
        print(f"Processing {symbol} ({index}/{total_stocks})...")
        print(f"{'='*50}")
        
        # Add retry mechanism
        max_retries = 3
        success = False
        
        for attempt in range(max_retries):
            try:
                # Perform analysis
                results = analyzer.analyze_stock(symbol)
                
                if results:
                    # Store results for summary report
                    all_results[symbol] = results
                    
                    # Display technical analysis results
                    tech_analysis = results['technical_analysis']
                    signals = tech_analysis['signals']
                    
                    # Get recommendation
                    recommendation, confidence_score, reasoning = analyzer.generate_recommendation(
                        tech_analysis, signals)
                    
                    print("\nAnalysis Results:")
                    print(f"Last Price: ${tech_analysis['last_price']:.2f}")
                    print(f"Recommendation: {recommendation}")
                    print(f"Confidence Score: {confidence_score:.1f}%")
                    print(f"Analysis Reasoning: {reasoning}")
                    
                    print("\nKey Indicators:")
                    print(f"RSI: {tech_analysis['rsi']:.2f}")
                    print(f"MACD: {tech_analysis['macd']:.2f}")
                    
                    print("\nTrading Signals:")
                    for indicator, signal in signals.items():
                        print(f"{indicator}: {signal}")
                    
                    # Export results
                    analyzer.export_results(results, symbol)
                    
                    print(f"\nAnalysis completed for {symbol}")
                    success = True
                    break  # Success, exit retry loop
                    
            except Exception as e:
                print(f"Error during analysis of {symbol}: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying... (Attempt {attempt + 2} of {max_retries})")
                    time.sleep(2)  # Wait before retrying
        
        if not success:
            failed_symbols.append(symbol)
            print(f"Failed to analyze {symbol} after {max_retries} attempts")
        
        # Progress update
        elapsed_time = time.time() - start_time
        avg_time_per_stock = elapsed_time / index
        remaining_stocks = total_stocks - index
        estimated_time_remaining = remaining_stocks * avg_time_per_stock
        
        print(f"\nProgress: {index}/{total_stocks} stocks processed")
        print(f"Estimated time remaining: {estimated_time_remaining/60:.1f} minutes")
        
        time.sleep(1)  # Prevent rate limiting
    
    # Generate summary reports
    if all_results:
        try:
            # Generate Excel summary
            excel_path = analyzer.generate_excel_summary(all_results)
            if excel_path:
                print(f"Excel summary created at: {excel_path}")
            
            print("\nSummary Reports Generated Successfully!")
        except Exception as e:
            print(f"Error generating summary reports: {str(e)}")
    
    # Print analysis summary
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print("="*50)
    print(f"Total stocks processed: {total_stocks}")
    print(f"Successfully analyzed: {len(all_results)}")
    print(f"Failed to analyze: {len(failed_symbols)}")
    
    if failed_symbols:
        print("\nFailed stocks:")
        for symbol in failed_symbols:
            print(f"- {symbol}")
    
    # Print total execution time
    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time/60:.1f} minutes")

if __name__ == "__main__":
    main()
