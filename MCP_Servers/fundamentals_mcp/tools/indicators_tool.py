from typing import Optional
from .data_loader import load_financial_data

def get_technical_indicators(stock_symbol: str) -> dict:
    """
    Retrieve technical analysis indicators for a stock including RSI, MACD, and moving averages.
    
    Technical indicators help identify momentum, trend direction, and potential entry/exit points.
    - RSI (Relative Strength Index): Momentum oscillator measuring overbought (>70) or oversold (<30) conditions
    - MACD (Moving Average Convergence Divergence): Trend-following momentum indicator showing relationship between two EMAs
    - SMA_50: 50-day Simple Moving Average - intermediate term trend indicator
    - SMA_200: 200-day Simple Moving Average - long term trend indicator and support/resistance level
    
    Args:
        stock_symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        Dictionary containing RSI, MACD, 50-day SMA, and 200-day SMA values
    """
    try:
        # Load required financial data
        financial_data = load_financial_data(stock_symbol, ['overview'])
        overview = financial_data["overview"]
        
        # Extract technical indicators from overview
        sma_50 = float(overview.get("50DayMovingAverage", 0))
        sma_200 = float(overview.get("200DayMovingAverage", 0))
        
        # Note: RSI and MACD are not in the OVERVIEW.json
        # These would typically come from time series data or a separate technical analysis API
        # For now, we'll indicate they're not available in this dataset
        
        return {
            "symbol": overview["Symbol"],
            "SMA_50": sma_50,
            "SMA_200": sma_200,
            "CurrentPrice": "Use overview data for current price context",
            "52WeekHigh": float(overview.get("52WeekHigh", 0)),
            "52WeekLow": float(overview.get("52WeekLow", 0)),
            "Beta": float(overview.get("Beta", 0)),
            "note": "RSI and MACD require intraday time series data - not available in current dataset"
        }
    
    except FileNotFoundError as e:
        return {
            "symbol": stock_symbol.upper(),
            "error": f"File not found: {str(e)}"
        }
    except KeyError as e:
        return {
            "symbol": stock_symbol.upper(),
            "error": f"Missing required field: {str(e)}"
        }
    except Exception as e:
        return {
            "symbol": stock_symbol.upper(),
            "error": f"Error fetching technical indicators: {str(e)}"
        }
