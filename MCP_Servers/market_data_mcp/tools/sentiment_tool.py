from typing import Optional
import sys
from pathlib import Path
import statistics

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_time_series


def get_market_sentiment(company: str, lookback_periods: Optional[int] = 30) -> dict:
    """
    Analyze market sentiment based on price action, volume, and momentum indicators.
    
    Market sentiment reflects the overall attitude of investors toward a stock:
    - Bullish: Optimistic, expecting prices to rise
    - Bearish: Pessimistic, expecting prices to fall
    - Neutral: No strong directional bias
    
    This tool combines multiple factors to gauge sentiment:
    - Price momentum and trend
    - Volume patterns (increasing volume = stronger conviction)
    - Volatility (high volatility = uncertainty)
    - Recent price patterns
    - Buying/selling pressure
    
    Use this for:
    - Understanding market psychology
    - Confirming trend strength
    - Identifying potential reversals
    - Timing entry and exit points
    
    Args:
        company: Company ticker symbol (e.g., 'IBM', 'AAPL', 'TSLA')
        lookback_periods: Number of periods to analyze (default: 30)
    
    Returns:
        Dictionary containing:
        - overallSentiment: Overall market sentiment (Bullish/Bearish/Neutral)
        - sentimentScore: Numerical score (-100 to +100)
        - confidence: Confidence level (High/Medium/Low)
        - buyingPressure: Measure of buying interest
        - sellingPressure: Measure of selling interest
        - volumeSignal: Volume-based signal
        - priceAction: Recent price action analysis
        - momentumIndicator: Momentum strength
        - riskLevel: Assessed risk level
        - recommendation: Suggested action based on sentiment
        - summary: Detailed sentiment summary
    
    Example:
        >>> get_market_sentiment('IBM', 30)
        {
            'company': 'IBM',
            'overallSentiment': 'Bullish',
            'sentimentScore': 65,
            'confidence': 'High',
            'buyingPressure': 'Strong',
            'sellingPressure': 'Weak',
            'volumeSignal': 'Accumulation',
            'priceAction': 'Consistent upward movement',
            'momentumIndicator': 'Positive',
            'riskLevel': 'Moderate',
            'recommendation': 'Consider buying on dips',
            'summary': 'Strong bullish sentiment with high buying pressure...'
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
        
        # Extract data
        timestamps = list(time_series.keys())[:lookback_periods]
        prices = [float(time_series[ts]["4. close"]) for ts in timestamps]
        opens = [float(time_series[ts]["1. open"]) for ts in timestamps]
        highs = [float(time_series[ts]["2. high"]) for ts in timestamps]
        lows = [float(time_series[ts]["3. low"]) for ts in timestamps]
        volumes = [int(time_series[ts]["5. volume"]) for ts in timestamps]
        
        if len(prices) < 10:
            return {
                "company": company.upper(),
                "error": f"Insufficient data. Need at least 10 periods, got {len(prices)}"
            }
        
        # Initialize sentiment score (range: -100 to +100)
        sentiment_score = 0
        
        # 1. Price Trend Analysis (weight: 30%)
        current_price = prices[0]
        start_price = prices[-1]
        price_change_percent = ((current_price - start_price) / start_price) * 100
        
        if price_change_percent > 3:
            sentiment_score += 30
        elif price_change_percent > 1:
            sentiment_score += 15
        elif price_change_percent < -3:
            sentiment_score -= 30
        elif price_change_percent < -1:
            sentiment_score -= 15
        
        # 2. Momentum Analysis (weight: 25%)
        # Count up days vs down days
        up_days = sum(1 for i in range(len(prices)-1) if prices[i] > prices[i+1])
        down_days = len(prices) - 1 - up_days
        
        if up_days > down_days * 1.5:
            sentiment_score += 25
            momentum_indicator = "Strong Positive"
        elif up_days > down_days:
            sentiment_score += 12
            momentum_indicator = "Positive"
        elif down_days > up_days * 1.5:
            sentiment_score -= 25
            momentum_indicator = "Strong Negative"
        elif down_days > up_days:
            sentiment_score -= 12
            momentum_indicator = "Negative"
        else:
            momentum_indicator = "Neutral"
        
        # 3. Volume Analysis (weight: 20%)
        avg_volume = statistics.mean(volumes)
        recent_volume = statistics.mean(volumes[:10])
        
        volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
        
        if volume_ratio > 1.3 and price_change_percent > 0:
            sentiment_score += 20
            volume_signal = "Strong Accumulation"
        elif volume_ratio > 1.1 and price_change_percent > 0:
            sentiment_score += 10
            volume_signal = "Accumulation"
        elif volume_ratio > 1.3 and price_change_percent < 0:
            sentiment_score -= 20
            volume_signal = "Strong Distribution"
        elif volume_ratio > 1.1 and price_change_percent < 0:
            sentiment_score -= 10
            volume_signal = "Distribution"
        else:
            volume_signal = "Neutral"
        
        # 4. Buying/Selling Pressure (weight: 15%)
        # Compare closes to highs/lows
        buying_pressure_score = 0
        for i in range(min(10, len(prices))):
            close = prices[i]
            high = highs[i]
            low = lows[i]
            range_size = high - low
            
            if range_size > 0:
                # Close near high = buying pressure
                close_position = (close - low) / range_size
                if close_position > 0.7:
                    buying_pressure_score += 1
                elif close_position < 0.3:
                    buying_pressure_score -= 1
        
        if buying_pressure_score > 5:
            sentiment_score += 15
            buying_pressure = "Strong"
            selling_pressure = "Weak"
        elif buying_pressure_score > 2:
            sentiment_score += 8
            buying_pressure = "Moderate"
            selling_pressure = "Weak"
        elif buying_pressure_score < -5:
            sentiment_score -= 15
            buying_pressure = "Weak"
            selling_pressure = "Strong"
        elif buying_pressure_score < -2:
            sentiment_score -= 8
            buying_pressure = "Weak"
            selling_pressure = "Moderate"
        else:
            buying_pressure = "Moderate"
            selling_pressure = "Moderate"
        
        # 5. Volatility Analysis (weight: 10%)
        price_std = statistics.stdev(prices)
        avg_price = statistics.mean(prices)
        coefficient_of_variation = (price_std / avg_price) * 100 if avg_price > 0 else 0
        
        if coefficient_of_variation > 3:
            sentiment_score -= 10
            volatility_impact = "High volatility indicates uncertainty"
            risk_level = "High"
        elif coefficient_of_variation > 1.5:
            sentiment_score -= 5
            volatility_impact = "Moderate volatility"
            risk_level = "Moderate"
        else:
            volatility_impact = "Low volatility indicates stability"
            risk_level = "Low"
        
        # Determine overall sentiment
        if sentiment_score > 50:
            overall_sentiment = "Strong Bullish"
            confidence = "High"
            recommendation = "Strong buy signal - Consider accumulating position"
        elif sentiment_score > 25:
            overall_sentiment = "Bullish"
            confidence = "Medium-High"
            recommendation = "Buy signal - Consider entering or adding to position"
        elif sentiment_score > 10:
            overall_sentiment = "Moderately Bullish"
            confidence = "Medium"
            recommendation = "Cautiously optimistic - Consider buying on dips"
        elif sentiment_score < -50:
            overall_sentiment = "Strong Bearish"
            confidence = "High"
            recommendation = "Strong sell signal - Consider reducing exposure"
        elif sentiment_score < -25:
            overall_sentiment = "Bearish"
            confidence = "Medium-High"
            recommendation = "Sell signal - Consider exiting position"
        elif sentiment_score < -10:
            overall_sentiment = "Moderately Bearish"
            confidence = "Medium"
            recommendation = "Cautiously pessimistic - Avoid new positions"
        else:
            overall_sentiment = "Neutral"
            confidence = "Low"
            recommendation = "Hold and wait for clearer signals"
        
        # Analyze price action pattern
        if up_days > down_days and price_change_percent > 0:
            price_action = "Consistent upward movement with positive momentum"
        elif down_days > up_days and price_change_percent < 0:
            price_action = "Consistent downward movement with negative momentum"
        elif abs(price_change_percent) < 1:
            price_action = "Sideways consolidation with no clear direction"
        else:
            price_action = "Mixed signals with volatile price swings"
        
        # Generate detailed summary
        summary_parts = []
        summary_parts.append(f"{overall_sentiment} sentiment with {confidence.lower()} confidence.")
        summary_parts.append(f"Sentiment score: {sentiment_score}/100.")
        summary_parts.append(f"Price has {'increased' if price_change_percent > 0 else 'decreased'} by {abs(price_change_percent):.2f}% over the period.")
        summary_parts.append(f"{buying_pressure} buying pressure vs {selling_pressure.lower()} selling pressure.")
        summary_parts.append(f"Volume indicates {volume_signal.lower()}.")
        summary_parts.append(f"{volatility_impact}.")
        summary_parts.append(f"Risk level: {risk_level}.")
        
        summary = " ".join(summary_parts)
        
        return {
            "company": company.upper(),
            "period": f"{lookback_periods} intervals",
            "analysisTimeframe": f"{timestamps[-1]} to {timestamps[0]}",
            "sentimentAnalysis": {
                "overallSentiment": overall_sentiment,
                "sentimentScore": sentiment_score,
                "confidence": confidence,
                "riskLevel": risk_level
            },
            "marketSignals": {
                "buyingPressure": buying_pressure,
                "sellingPressure": selling_pressure,
                "volumeSignal": volume_signal,
                "momentumIndicator": momentum_indicator
            },
            "priceMetrics": {
                "currentPrice": round(current_price, 2),
                "priceChange": round(current_price - start_price, 2),
                "priceChangePercent": f"{round(price_change_percent, 2)}%",
                "priceAction": price_action,
                "upDays": up_days,
                "downDays": down_days
            },
            "volumeMetrics": {
                "averageVolume": int(avg_volume),
                "recentVolume": int(recent_volume),
                "volumeRatio": round(volume_ratio, 2)
            },
            "recommendation": recommendation,
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
            "error": f"Error analyzing market sentiment: {str(e)}"
        }
