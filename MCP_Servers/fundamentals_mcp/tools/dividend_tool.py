import random
from datetime import datetime, timedelta
from typing import Optional
from .data_loader import load_financial_data

def get_dividend_info(company: str) -> dict:
    """
    Retrieve dividend information including yield, payout ratio, and ex-dividend date.
    
    Dividend metrics are crucial for income-focused investors:
    - Dividend Yield: Annual dividend as percentage of stock price (higher yield may indicate value or risk)
    - Payout Ratio: Percentage of earnings paid as dividends (sustainable range is typically 30-60%)
    - Ex-Dividend Date: Date after which new buyers won't receive the upcoming dividend payment
    
    A healthy dividend stock typically has sustainable payout ratio (<70%) and consistent yield.
    
    Formulas:
    - Dividend Yield = (Annual Dividend per Share / Current Stock Price) * 100
    - Payout Ratio = (Dividend Per Share / EPS) * 100
    
    Args:
        company: Company ticker symbol or name (e.g., 'JNJ', 'KO')
    
    Returns:
        Dictionary containing dividend yield, payout ratio, and ex-dividend date
    """
    try:
        # Load required financial data
        financial_data = load_financial_data(company, ['overview'])
        overview = financial_data["overview"]
        
        # Extract dividend data from overview
        dividend_per_share = float(overview.get("DividendPerShare", 0))
        ex_dividend_date = overview.get("ExDividendDate", "N/A")
        dividend_date = overview.get("DividendDate", "N/A")
        
        # Get current stock price (we can derive from market cap and shares outstanding)
        market_cap = float(overview.get("MarketCapitalization", 0))
        shares_outstanding = float(overview.get("SharesOutstanding", 1))
        
        # Calculate current stock price
        if shares_outstanding > 0:
            current_price = market_cap / shares_outstanding
        else:
            current_price = 0
        
        # Calculate dividend yield: (Annual Dividend per Share / Current Stock Price) * 100
        if current_price > 0:
            dividend_yield = round((dividend_per_share / current_price) * 100, 2)
        else:
            dividend_yield = 0.0
        
        # Calculate payout ratio: (Dividend Per Share / EPS) * 100
        eps = float(overview.get("EPS", 0))
        if eps > 0:
            payout_ratio = round((dividend_per_share / eps) * 100, 2)
        else:
            payout_ratio = 0.0
        
        return {
            "company": overview["Symbol"],
            "DividendPerShare": dividend_per_share,
            "DividendYield": f"{dividend_yield}%",
            "PayoutRatio": f"{payout_ratio}%",
            "ExDividendDate": ex_dividend_date,
            "DividendPaymentDate": dividend_date,
            "CurrentStockPrice": round(current_price, 2)
        }
    
    except FileNotFoundError as e:
        return {
            "company": company.upper(),
            "error": f"File not found: {str(e)}"
        }
    except KeyError as e:
        return {
            "company": company.upper(),
            "error": f"Missing required field: {str(e)}"
        }
    except Exception as e:
        return {
            "company": company.upper(),
            "error": f"Error fetching dividend info: {str(e)}"
        }
