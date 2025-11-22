from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_financial_data

def get_leverage_ratios(company: str, year_range: Optional[int] = 1) -> dict:
    """
    Assess financial leverage and debt sustainability through key debt ratios.
    
    Leverage ratios measure financial risk and ability to service debt obligations:
    - Debt-to-Equity: Total debt relative to shareholder equity (lower is safer, >2.0 indicates high leverage)
    - Interest Coverage: Ability to pay interest from operating income (>3.0 is healthy, <1.5 is risky)
    - Debt-to-EBITDA: Debt repayment capacity measured in years of EBITDA (<3.0 is generally healthy)
    
    Lower leverage ratios indicate stronger financial stability and lower bankruptcy risk.
    Compare against industry peers for context.
    
    Args:
        company: Company ticker symbol or name (e.g., 'BA', 'F')
        year_range: Number of years to analyze (default: 1 for last year only)
    
    Returns:
        Dictionary containing debt-to-equity, interest coverage, and debt-to-EBITDA ratios
    """
    try:
        # Load required financial data
        financial_data = load_financial_data(company, ['balance_sheet', 'income_statement'])
        balance_sheet = financial_data["balance_sheet"]
        income_statement = financial_data["income_statement"]
        
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
            is_data = income_statement["annualReports"][i]
            
            # Extract values
            total_debt = float(bs.get("shortLongTermDebtTotal", 0))
            total_equity = float(bs.get("totalShareholderEquity", 1))  # Avoid division by zero
            
            operating_income = float(is_data.get("operatingIncome", 0))
            interest_expense = float(is_data.get("interestExpense", 1))  # Avoid division by zero
            ebitda = float(is_data.get("ebitda", 1))  # Avoid division by zero
            
            # Calculate ratios
            debt_to_equity = round(total_debt / total_equity, 2) if total_equity > 0 else 0
            interest_coverage = round(operating_income / interest_expense, 2) if interest_expense > 0 else 0
            debt_to_ebitda = round(total_debt / ebitda, 2) if ebitda > 0 else 0
            
            year_data = {
                "fiscalYear": bs["fiscalDateEnding"],
                "DebtToEquity": debt_to_equity,
                "InterestCoverage": interest_coverage,
                "DebtToEBITDA": debt_to_ebitda
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
            "error": f"Error calculating leverage ratios: {str(e)}"
        }
