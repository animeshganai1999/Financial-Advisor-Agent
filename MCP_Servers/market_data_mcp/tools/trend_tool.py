from typing import Optional
import sys
from pathlib import Path
import statistics

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_time_series


def get_price_trend_summary(company: str, lookback_periods: Optional[int] = 50) -> dict:
    """
    Analyze price trends and provide a comprehensive trend summary.
    
    This tool analyzes recent price movements to identify:
    - Overall trend direction (uptrend, downtrend, sideways)
    - Trend strength and consistency
    - Support and resistance levels
    - Price momentum and volatility
    - Recent price patterns
    
    Useful for:
    - Identifying entry and exit points
    - Understanding market sentiment
    - Confirming trend reversals
    - Assessing trading opportunities
    
    Args:
        company: Company ticker symbol (e.g., 'IBM', 'AAPL', 'NVDA')
        lookback_periods: Number of time periods to analyze (default: 50)
    
    Returns:
        Dictionary containing:
        - trendDirection: Overall trend (Uptrend/Downtrend/Sideways)
        - trendStrength: Strength of the trend (Strong/Moderate/Weak)
        - priceChange: Price change over period
        - priceChangePercent: Percentage change
        - averagePrice: Average price over period
        - volatility: Price volatility measure
        - supportLevel: Identified support level
        - resistanceLevel: Identified resistance level
        - momentum: Current momentum (Bullish/Bearish/Neutral)
        - recentPattern: Identified price pattern
        - summary: Textual summary of trend analysis
    
    Example:
        >>> get_price_trend_summary('IBM', 50)
        {
            'company': 'IBM',
            'period': '50 intervals',
            'trendDirection': 'Uptrend',
            'trendStrength': 'Strong',
            'priceChange': 8.50,
            'priceChangePercent': '6.22%',
            'averagePrice': 142.30,
            'volatility': 'Moderate',
            'supportLevel': 138.50,
            'resistanceLevel': 148.20,
            'momentum': 'Bullish',
            'recentPattern': 'Higher highs and higher lows',
            'summary': 'Strong uptrend with bullish momentum...'
        }
    """
    try:
        # Load time series data
        time_series_data = load_time_series(company)
        time_series = time_series_data.get("Time Series (1min)", {})
        
        if not time_series:
            return {
                "company": company.upper(),
                "error": "No time series data available"
            }
        
        # Extract price data (most recent first)
        timestamps = list(time_series.keys())[:lookback_periods]
        prices = [float(time_series[ts]["4. close"]) for ts in timestamps]
        highs = [float(time_series[ts]["2. high"]) for ts in timestamps]
        lows = [float(time_series[ts]["3. low"]) for ts in timestamps]
        volumes = [int(time_series[ts]["5. volume"]) for ts in timestamps]
        
        if len(prices) < 10:
            return {
                "company": company.upper(),
                "error": f"Insufficient data. Need at least 10 periods, got {len(prices)}"
            }
        
        # Calculate basic metrics
        current_price = prices[0]
        start_price = prices[-1]
        price_change = current_price - start_price
        price_change_percent = (price_change / start_price) * 100 if start_price != 0 else 0
        
        average_price = statistics.mean(prices)
        price_std = statistics.stdev(prices) if len(prices) > 1 else 0
        
        # Identify support and resistance
        support_level = min(lows)
        resistance_level = max(highs)
        
        # Determine trend direction
        # Split into segments and compare
        segment_size = len(prices) // 3
        recent_avg = statistics.mean(prices[:segment_size])
        middle_avg = statistics.mean(prices[segment_size:2*segment_size])
        older_avg = statistics.mean(prices[2*segment_size:])
        
        trend_direction = "Sideways"
        if recent_avg > middle_avg > older_avg:
            trend_direction = "Uptrend"
        elif recent_avg < middle_avg < older_avg:
            trend_direction = "Downtrend"
        
        # Determine trend strength
        trend_strength = "Weak"
        if abs(price_change_percent) > 5:
            trend_strength = "Strong"
        elif abs(price_change_percent) > 2:
            trend_strength = "Moderate"
        
        # Calculate volatility
        coefficient_of_variation = (price_std / average_price) * 100 if average_price != 0 else 0
        volatility = "Low"
        if coefficient_of_variation > 3:
            volatility = "High"
        elif coefficient_of_variation > 1.5:
            volatility = "Moderate"
        
        # Determine momentum
        recent_change = prices[0] - prices[min(5, len(prices)-1)]
        momentum = "Neutral"
        if recent_change > 0 and trend_direction == "Uptrend":
            momentum = "Strong Bullish"
        elif recent_change > 0:
            momentum = "Bullish"
        elif recent_change < 0 and trend_direction == "Downtrend":
            momentum = "Strong Bearish"
        elif recent_change < 0:
            momentum = "Bearish"
        
        # Identify recent pattern
        recent_pattern = "Consolidation"
        if trend_direction == "Uptrend" and momentum in ["Bullish", "Strong Bullish"]:
            recent_pattern = "Higher highs and higher lows"
        elif trend_direction == "Downtrend" and momentum in ["Bearish", "Strong Bearish"]:
            recent_pattern = "Lower highs and lower lows"
        elif volatility == "High":
            recent_pattern = "High volatility with no clear direction"
        
        # Calculate average volume
        avg_volume = int(statistics.mean(volumes))
        recent_volume = int(statistics.mean(volumes[:5]))
        volume_trend = "Average"
        if recent_volume > avg_volume * 1.2:
            volume_trend = "Increasing (Strong interest)"
        elif recent_volume < avg_volume * 0.8:
            volume_trend = "Decreasing (Weak interest)"
        
        # Distance from support and resistance
        distance_from_support = ((current_price - support_level) / current_price) * 100
        distance_from_resistance = ((resistance_level - current_price) / current_price) * 100
        
        # Generate summary
        summary_parts = []
        summary_parts.append(f"{trend_strength} {trend_direction.lower()} with {momentum.lower()} momentum.")
        summary_parts.append(f"Price has {'gained' if price_change > 0 else 'lost'} {abs(price_change_percent):.2f}% over the period.")
        summary_parts.append(f"Volatility is {volatility.lower()}.")
        summary_parts.append(f"Trading volume is {volume_trend.lower()}.")
        
        if distance_from_support < 5:
            summary_parts.append(f"Price is near support level at ${support_level:.2f}.")
        elif distance_from_resistance < 5:
            summary_parts.append(f"Price is near resistance level at ${resistance_level:.2f}.")
        
        summary = " ".join(summary_parts)
        
        return {
            "company": company.upper(),
            "period": f"{lookback_periods} intervals",
            "analysisTimeframe": f"{timestamps[-1]} to {timestamps[0]}",
            "trendAnalysis": {
                "trendDirection": trend_direction,
                "trendStrength": trend_strength,
                "momentum": momentum,
                "recentPattern": recent_pattern
            },
            "priceMetrics": {
                "currentPrice": round(current_price, 2),
                "startPrice": round(start_price, 2),
                "priceChange": round(price_change, 2),
                "priceChangePercent": f"{round(price_change_percent, 2)}%",
                "averagePrice": round(average_price, 2),
                "volatility": volatility,
                "standardDeviation": round(price_std, 2)
            },
            "supportResistance": {
                "supportLevel": round(support_level, 2),
                "resistanceLevel": round(resistance_level, 2),
                "distanceFromSupport": f"{round(distance_from_support, 2)}%",
                "distanceFromResistance": f"{round(distance_from_resistance, 2)}%"
            },
            "volumeAnalysis": {
                "averageVolume": avg_volume,
                "recentVolume": recent_volume,
                "volumeTrend": volume_trend
            },
            "summary": summary
        }
        
    except FileNotFoundError as e:
        return {
            "company": company.upper(),
            "error": f"Data not found: {str(e)}"
        }
    except Exception as e:
        return {
            "company": company.upper(),
            "error": f"Error analyzing price trend: {str(e)}"
        }
