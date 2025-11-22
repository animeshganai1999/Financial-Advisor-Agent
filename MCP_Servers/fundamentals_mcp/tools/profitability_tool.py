from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_financial_data


def get_profitability_ratios(company: str, year_range: Optional[int] = 1) -> dict:
    """
    Measure company profitability through margins and return ratios.
    
    Profitability metrics assess how efficiently a company converts revenue into profit:
    - Gross Margin: (Revenue - COGS) / Revenue - measures pricing power and production efficiency
    - Operating Margin: Operating income / Revenue - core business profitability before taxes
    - Net Margin: Net income / Revenue - bottom-line profitability after all expenses
    - ROE (Return on Equity): Net income / Shareholder equity - returns generated for shareholders (>15% is excellent)
    - ROA (Return on Assets): Net income / Total assets - efficiency in using assets to generate profit
    
    Higher margins and returns indicate competitive advantages and superior management.
    
    Args:
        company: Company ticker symbol or name (e.g., 'GOOGL', 'META')
        year_range: Number of years to analyze (default: 1 for last year only)
    
    Returns:
        Dictionary containing gross, operating, and net margins, plus ROE and ROA
    """
    try:
        # Load required financial data
        financial_data = load_financial_data(company, ['income_statement', 'balance_sheet'])
        income_statement = financial_data["income_statement"]
        balance_sheet = financial_data["balance_sheet"]
        
        # Ensure we have enough data
        max_years = min(year_range, len(income_statement["annualReports"]))
        
        if max_years == 0:
            return {
                "company": company.upper(),
                "error": "Insufficient data."
            }
        
        results = []
        
        for i in range(max_years):
            is_data = income_statement["annualReports"][i]
            bs = balance_sheet["annualReports"][i]
            
            # Extract values
            total_revenue = float(is_data.get("totalRevenue", 1))  # Avoid division by zero
            gross_profit = float(is_data.get("grossProfit", 0))
            operating_income = float(is_data.get("operatingIncome", 0))
            net_income = float(is_data.get("netIncome", 0))
            total_assets = float(bs.get("totalAssets", 1))
            total_equity = float(bs.get("totalShareholderEquity", 1))
            
            # Calculate margins
            gross_margin = round((gross_profit / total_revenue) * 100, 2) if total_revenue > 0 else 0
            operating_margin = round((operating_income / total_revenue) * 100, 2) if total_revenue > 0 else 0
            net_margin = round((net_income / total_revenue) * 100, 2) if total_revenue > 0 else 0
            
            # Calculate returns
            roe = round((net_income / total_equity) * 100, 2) if total_equity > 0 else 0
            roa = round((net_income / total_assets) * 100, 2) if total_assets > 0 else 0
            
            year_data = {
                "fiscalYear": is_data["fiscalDateEnding"],
                "GrossMargin": f"{gross_margin}%",
                "OperatingMargin": f"{operating_margin}%",
                "NetMargin": f"{net_margin}%",
                "ROE": f"{roe}%",
                "ROA": f"{roa}%"
            }
            
            results.append(year_data)
        
        # Return structure based on year_range
        if year_range == 1:
            return {
                "company": income_statement["symbol"],
                **results[0]
            }
        else:
            return {
                "company": income_statement["symbol"],
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
            "error": f"Error calculating profitability ratios: {str(e)}"
        }
