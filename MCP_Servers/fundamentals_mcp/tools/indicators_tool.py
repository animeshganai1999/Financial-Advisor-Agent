from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_financial_data

def get_fundamental_indicators(stock_symbol: str) -> dict:
    """
    Retrieve fundamental-based long-term indicators for investment analysis.
    
    These indicators are derived from fundamental company data (not real-time):
    - Beta: Stock volatility relative to market - used for portfolio risk assessment
    - SMA_50: 50-day Simple Moving Average - medium-term trend from historical data
    - SMA_200: 200-day Simple Moving Average - long-term trend and key support/resistance
    - 52-week range: Annual trading range for valuation context
    
    Use this for:
    - Long-term investment decisions
    - Portfolio risk assessment
    - Historical trend context
    - Valuation relative to trading range
    
    For short-term trading signals (RSI, MACD, intraday indicators), use Market Data MCP.
    
    Args:
        stock_symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        Dictionary containing Beta, long-term moving averages, and 52-week range
    """
    try:
        # Load required financial data
        financial_data = load_financial_data(stock_symbol, ['overview'])
        overview = financial_data["overview"]
        
        # Extract fundamental indicators from overview
        sma_50 = float(overview.get("50DayMovingAverage", 0))
        sma_200 = float(overview.get("200DayMovingAverage", 0))
        beta = float(overview.get("Beta", 0))
        week_52_high = float(overview.get("52WeekHigh", 0))
        week_52_low = float(overview.get("52WeekLow", 0))
        
        # Calculate additional context
        price_to_52w_high = 0
        price_to_52w_low = 0
        if sma_50 > 0 and week_52_high > 0:
            price_to_52w_high = ((sma_50 - week_52_high) / week_52_high) * 100
        if sma_50 > 0 and week_52_low > 0:
            price_to_52w_low = ((sma_50 - week_52_low) / week_52_low) * 100
        
        # Trend analysis based on MA relationship
        long_term_trend = "Unknown"
        if sma_50 > 0 and sma_200 > 0:
            if sma_50 > sma_200 * 1.02:
                long_term_trend = "Bullish (50-day above 200-day)"
            elif sma_50 < sma_200 * 0.98:
                long_term_trend = "Bearish (50-day below 200-day)"
            else:
                long_term_trend = "Neutral (MAs converging)"
        
        return {
            "symbol": overview["Symbol"],
            "fundamentalIndicators": {
                "Beta": beta,
                "SMA_50": sma_50,
                "SMA_200": sma_200,
                "52WeekHigh": week_52_high,
                "52WeekLow": week_52_low,
                "52WeekRange": f"${week_52_low} - ${week_52_high}"
            },
            "analysis": {
                "longTermTrend": long_term_trend,
                "volatilityVsMarket": "Higher" if beta > 1.0 else "Lower" if beta < 1.0 else "Same",
                "distanceFrom52WeekHigh": f"{round(price_to_52w_high, 1)}%",
                "distanceFrom52WeekLow": f"{round(price_to_52w_low, 1)}%"
            },
            "note": "These are long-term fundamental indicators. For real-time technical analysis (RSI, MACD, intraday trends), use Market Data MCP."
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
            "error": f"Error fetching fundamental indicators: {str(e)}"
        }
