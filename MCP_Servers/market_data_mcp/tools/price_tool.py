from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_time_series


def get_latest_price(company: str) -> dict:
    """
    Get the latest stock price and trading information for a company.
    
    Provides real-time (or latest available) price data including:
    - Current price
    - Opening price
    - High and low prices
    - Trading volume
    - Previous close
    
    This is essential for understanding current market valuation and trading activity.
    Use this when you need the most recent price information for analysis or comparison.
    
    Args:
        company: Company ticker symbol (e.g., 'IBM', 'AAPL', 'NVDA')
    
    Returns:
        Dictionary containing:
        - company: Ticker symbol
        - latestPrice: Most recent trading price
        - open: Opening price
        - high: Day's high price
        - low: Day's low price
        - volume: Trading volume
        - previousClose: Previous day's closing price
        - priceChange: Price change from previous close
        - priceChangePercent: Percentage change from previous close
        - timestamp: Time of latest price update
    
    Example:
        >>> get_latest_price('IBM')
        {
            'company': 'IBM',
            'latestPrice': 145.32,
            'open': 144.50,
            'high': 146.20,
            'low': 143.80,
            'volume': 4523000,
            'previousClose': 144.00,
            'priceChange': 1.32,
            'priceChangePercent': '0.92%',
            'timestamp': '2024-01-15 16:00:00'
        }
    """
    try:
        # Load time series data
        time_series_data = load_time_series(company)
        
        # Get metadata
        meta_data = time_series_data.get("Meta Data", {})
        time_series = time_series_data.get("Time Series (1min)", {})
        
        if not time_series:
            return {
                "company": company.upper(),
                "error": "No time series data available"
            }
        
        # Get the latest timestamp (first key in ordered dict)
        latest_timestamp = next(iter(time_series.keys()))
        latest_data = time_series[latest_timestamp]
        
        # Get all timestamps to find previous close
        timestamps = list(time_series.keys())
        
        # Extract latest price information
        latest_price = float(latest_data["4. close"])
        open_price = float(latest_data["1. open"])
        high_price = float(latest_data["2. high"])
        low_price = float(latest_data["3. low"])
        volume = int(latest_data["5. volume"])
        
        # Calculate previous close (use the close from previous time period)
        previous_close = latest_price  # Default to current if no previous data
        if len(timestamps) > 1:
            previous_data = time_series[timestamps[1]]
            previous_close = float(previous_data["4. close"])
        
        # Calculate price change
        price_change = latest_price - previous_close
        price_change_percent = (price_change / previous_close) * 100 if previous_close != 0 else 0
        
        return {
            "company": company.upper(),
            "symbol": meta_data.get("2. Symbol", company.upper()),
            "latestPrice": round(latest_price, 2),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "volume": volume,
            "previousClose": round(previous_close, 2),
            "priceChange": round(price_change, 2),
            "priceChangePercent": f"{round(price_change_percent, 2)}%",
            "timestamp": latest_timestamp,
            "lastRefreshed": meta_data.get("3. Last Refreshed", latest_timestamp)
        }
        
    except FileNotFoundError as e:
        return {
            "company": company.upper(),
            "error": f"Data not found: {str(e)}"
        }
    except Exception as e:
        return {
            "company": company.upper(),
            "error": f"Error retrieving latest price: {str(e)}"
        }
