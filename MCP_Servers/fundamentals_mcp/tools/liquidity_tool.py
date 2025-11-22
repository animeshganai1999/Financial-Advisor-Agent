from typing import Optional
import random
import sys
from pathlib import Path

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_financial_data


def get_liquidity_ratios(company: str, year_range: Optional[int] = 1) -> dict:
    """
    Evaluate short-term financial health and ability to meet immediate obligations.
    
    Liquidity ratios assess the company's ability to pay short-term debts:
    - Current Ratio: Current assets / current liabilities (>2.0 is strong, <1.0 indicates potential solvency issues)
    - Quick Ratio (Acid Test): (Current assets - inventory) / current liabilities (>1.0 is healthy)
    - Cash Ratio: Cash & equivalents / current liabilities (most conservative measure, >0.5 is solid)
    
    Higher ratios indicate better ability to handle financial stress and unexpected expenses.
    Essential for assessing bankruptcy risk.
    
    Args:
        company: Company ticker symbol or name (e.g., 'AAPL', 'MSFT')
        year_range: Number of years to analyze (default: 1 for last year only)
    
    Returns:
        Dictionary containing current ratio, quick ratio, and cash ratio
    """
    try:
        # Load required financial data
        financial_data = load_financial_data(company, ['balance_sheet'])
        balance_sheet = financial_data["balance_sheet"]
        
        # Ensure we have enough data
        max_years = min(year_range, len(balance_sheet["annualReports"]))
        
        if max_years == 0:
            return {
                "company": company.upper(),
                "error": "Insufficient data."
            }
        
        results = []
        
        for i in range(max_years):
            bs = balance_sheet["annualReports"][i]
            
            # Extract values
            current_assets = float(bs.get("totalCurrentAssets", 0))
            current_liabilities = float(bs.get("totalCurrentLiabilities", 1))  # Avoid division by zero
            inventory = float(bs.get("inventory", 0))
            cash = float(bs.get("cashAndCashEquivalentsAtCarryingValue", 0))
            
            # Calculate ratios
            current_ratio = round(current_assets / current_liabilities, 2) if current_liabilities > 0 else 0
            quick_ratio = round((current_assets - inventory) / current_liabilities, 2) if current_liabilities > 0 else 0
            cash_ratio = round(cash / current_liabilities, 2) if current_liabilities > 0 else 0
            
            year_data = {
                "fiscalYear": bs["fiscalDateEnding"],
                "CurrentRatio": current_ratio,
                "QuickRatio": quick_ratio,
                "CashRatio": cash_ratio
            }
            
            results.append(year_data)
        
        # Return structure based on year_range
        if year_range == 1:
            return {
                "company": balance_sheet["symbol"],
                **results[0]
            }
        else:
            return {
                "company": balance_sheet["symbol"],
                "yearRange": max_years,
                "data": results
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
            "error": f"Error calculating liquidity ratios: {str(e)}"
        }
