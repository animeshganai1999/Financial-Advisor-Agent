from typing import Optional
import sys
from pathlib import Path
import statistics

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_time_series, load_overview


def _calculate_sma(prices: list, period: int) -> float:
    """Calculate Simple Moving Average."""
    if len(prices) < period:
        return 0.0
    return round(statistics.mean(prices[:period]), 2)


def _calculate_ema(prices: list, period: int) -> float:
    """Calculate Exponential Moving Average."""
    if len(prices) < period:
        return 0.0
    
    multiplier = 2 / (period + 1)
    ema = statistics.mean(prices[:period])  # Start with SMA
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    
    return round(ema, 2)


def _calculate_rsi(prices: list, period: int = 14) -> float:
    """Calculate Relative Strength Index (RSI)."""
    if len(prices) < period + 1:
        return 50.0  # Neutral RSI if insufficient data
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    if len(gains) < period:
        return 50.0
    
    avg_gain = statistics.mean(gains[:period])
    avg_loss = statistics.mean(losses[:period])
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return round(rsi, 2)


def _calculate_macd(prices: list) -> dict:
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Returns:
        Dictionary with MACD line, signal line, and histogram
    """
    if len(prices) < 26:
        return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}
    
    # Calculate 12-day and 26-day EMAs
    ema_12 = _calculate_ema(prices, 12)
    ema_26 = _calculate_ema(prices, 26)
    
    # MACD line
    macd_line = ema_12 - ema_26
    
    # For simplicity, using a simple moving average for signal line
    # In production, this should be a 9-day EMA of the MACD line
    signal_line = macd_line * 0.9  # Simplified
    
    # Histogram
    histogram = macd_line - signal_line
    
    return {
        "macd": round(macd_line, 2),
        "signal": round(signal_line, 2),
        "histogram": round(histogram, 2)
    }


def get_technical_indicators(company: str, period: Optional[int] = 14) -> dict:
    """
    Calculate real-time technical indicators for short-term trading and momentum analysis.
    
    Technical indicators calculated from intraday price data help identify:
    
    RSI (Relative Strength Index):
    - Real-time momentum indicator (0-100 scale)
    - Above 70: Overbought (potential sell signal)
    - Below 30: Oversold (potential buy signal)
    - 40-60: Neutral zone
    
    MACD (Moving Average Convergence Divergence):
    - Trend-following momentum indicator
    - MACD > Signal: Bullish crossover
    - MACD < Signal: Bearish crossover
    - Histogram shows momentum strength
    
    Short-term Moving Averages:
    - SMA: Simple Moving Average calculated from recent prices
    - EMA: Exponential Moving Average (gives more weight to recent prices)
    - Price above MA: Short-term uptrend
    - Price below MA: Short-term downtrend
    
    Beta:
    - Volatility relative to market (S&P 500)
    - Beta > 1: More volatile than market
    - Beta < 1: Less volatile than market
    
    52-Week Range:
    - Annual high/low trading range
    - Position in range indicates strength/value
    
    Use this for:
    - Short-term trading decisions
    - Entry/exit timing
    - Momentum analysis
    - Volatility assessment
    - Intraday trend confirmation
    
    Args:
        company: Company ticker symbol (e.g., 'IBM', 'AAPL', 'TSLA')
        period: Period for RSI and moving averages (default: 14 for intraday)
    
    Returns:
        Dictionary containing:
        - RSI: Real-time Relative Strength Index
        - MACD: MACD line, signal line, and histogram
        - SMA: Short-term Simple Moving Average
        - EMA: Short-term Exponential Moving Average
        - Beta: Market volatility measure
        - 52WeekHigh/Low: Annual trading range
        - currentPrice: Latest intraday price
        - analysis: Momentum, trend, and volatility interpretation
    
    Example:
        >>> get_technical_indicators('IBM', 14)
        {
            'company': 'IBM',
            'RSI': 58.32,
            'MACD': {'macd': 1.45, 'signal': 1.30, 'histogram': 0.15},
            'SMA_14': 144.50,
            'EMA_14': 145.20,
            'currentPrice': 145.32,
            'analysis': {
                'momentum': 'Neutral',
                'trend': 'Bullish',
                'signal': 'Hold'
            }
        }
    """
    try:
        # Load time series and overview data
        time_series_data = load_time_series(company)
        overview_data = load_overview(company)
        
        time_series = time_series_data.get("Time Series (1min)", {})
        
        if not time_series:
            return {
                "company": company.upper(),
                "error": "No intraday time series data available"
            }
        
        # Extract closing prices (most recent first)
        closing_prices = [float(data["4. close"]) for data in time_series.values()]
        
        # Get current price
        current_price = closing_prices[0] if closing_prices else 0.0
        
        # Calculate real-time technical indicators
        rsi = _calculate_rsi(closing_prices, period)
        macd = _calculate_macd(closing_prices)
        sma = _calculate_sma(closing_prices, period)
        ema = _calculate_ema(closing_prices, period)
        
        # Get Beta and 52-week range from overview
        beta = float(overview_data.get("Beta", 1.0))
        week_52_high = float(overview_data.get("52WeekHigh", 0.0))
        week_52_low = float(overview_data.get("52WeekLow", 0.0))
        
        # Calculate position in 52-week range
        range_position = 0
        if week_52_high != week_52_low:
            range_position = ((current_price - week_52_low) / (week_52_high - week_52_low)) * 100
        
        # Analyze momentum
        momentum_analysis = "Neutral"
        trading_signal = "Hold"
        if rsi > 70:
            momentum_analysis = "Overbought"
            trading_signal = "Consider selling or taking profits"
        elif rsi < 30:
            momentum_analysis = "Oversold"
            trading_signal = "Consider buying on dips"
        elif rsi > 60:
            momentum_analysis = "Bullish"
            trading_signal = "Upward momentum"
        elif rsi < 40:
            momentum_analysis = "Bearish"
            trading_signal = "Downward pressure"
        
        # Analyze short-term trend
        trend_analysis = "Sideways"
        if current_price > sma and current_price > ema:
            trend_analysis = "Short-term Uptrend"
        elif current_price < sma and current_price < ema:
            trend_analysis = "Short-term Downtrend"
        
        # MACD signal
        macd_signal = "Neutral"
        if macd["histogram"] > 0.5:
            macd_signal = "Strong Bullish - MACD well above signal"
        elif macd["histogram"] > 0:
            macd_signal = "Bullish - MACD above signal"
        elif macd["histogram"] < -0.5:
            macd_signal = "Strong Bearish - MACD well below signal"
        elif macd["histogram"] < 0:
            macd_signal = "Bearish - MACD below signal"
        
        # Volatility analysis
        volatility_analysis = "Average"
        if beta > 1.2:
            volatility_analysis = "High - More volatile than market"
        elif beta < 0.8:
            volatility_analysis = "Low - Less volatile than market"
        elif beta > 1.0:
            volatility_analysis = "Moderate-High"
        else:
            volatility_analysis = "Moderate-Low"
        
        return {
            "company": company.upper(),
            "timestamp": list(time_series.keys())[0] if time_series else "N/A",
            "currentPrice": round(current_price, 2),
            "technicalIndicators": {
                "RSI": rsi,
                "RSI_Period": period,
                "MACD": macd,
                f"SMA_{period}": sma,
                f"EMA_{period}": ema,
                "Beta": beta,
                "52WeekHigh": week_52_high,
                "52WeekLow": week_52_low,
                "positionIn52WeekRange": f"{round(range_position, 1)}%"
            },
            "analysis": {
                "momentum": momentum_analysis,
                "shortTermTrend": trend_analysis,
                "macdSignal": macd_signal,
                "volatility": volatility_analysis,
                "tradingSignal": trading_signal
            },
            "interpretation": {
                "RSI": f"RSI at {rsi} indicates {momentum_analysis.lower()} conditions",
                "trend": f"Price at ${current_price} relative to moving averages suggests {trend_analysis.lower()}",
                "MACD": macd_signal,
                "volatility": f"Beta of {beta} indicates {volatility_analysis.lower()} volatility",
                "52WeekPosition": f"Trading at {round(range_position, 1)}% of 52-week range",
                "recommendation": trading_signal
            }
        }
        
    except FileNotFoundError as e:
        return {
            "company": company.upper(),
            "error": f"Data not found: {str(e)}"
        }
    except Exception as e:
        return {
            "company": company.upper(),
            "error": f"Error calculating technical indicators: {str(e)}"
        }
