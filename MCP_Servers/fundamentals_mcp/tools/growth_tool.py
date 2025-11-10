from typing import Optional
from .data_loader import load_financial_data


def _calculate_growth_rate(current_value: float, previousValue: float) -> float:
    """
    Calculate year-over-year growth rate.
    
    Args:
        current_value: Current year value
        previous_value: Previous year value
        
    Returns:
        Growth rate as a percentage
    """
    if previousValue == 0:
        return 0.0
    growth_rate = ((current_value - previousValue) / previousValue) * 100
    return round(growth_rate, 2)


def _calculate_growth_for_year(is_current: dict, is_previous: dict, earnings_current: dict, earnings_previous: dict) -> dict:
    """
    Calculate all growth metrics for a single year.
    
    Args:
        is_current: Current year income statement data
        is_previous: Previous year income statement data
        earnings_current: Current year earnings data
        earnings_previous: Previous year earnings data
        
    Returns:
        Dictionary with calculated growth metrics
    """
    # Extract values and convert to float
    revenue_current = float(is_current["totalRevenue"])
    revenue_previous = float(is_previous["totalRevenue"])
    
    operating_income_current = float(is_current["operatingIncome"])
    operating_income_previous = float(is_previous["operatingIncome"])
    
    eps_current = float(earnings_current["reportedEPS"])
    eps_previous = float(earnings_previous["reportedEPS"])
    
    # Calculate growth rates
    revenue_growth = _calculate_growth_rate(revenue_current, revenue_previous)
    operating_income_growth = _calculate_growth_rate(operating_income_current, operating_income_previous)
    eps_growth = _calculate_growth_rate(eps_current, eps_previous)
    
    return {
        "fiscalYear": is_current["fiscalDateEnding"],
        "RevenueGrowth": f"{revenue_growth}% YoY",
        "EPSGrowth": f"{eps_growth}% YoY",
        "OperatingIncomeGrowth": f"{operating_income_growth}% YoY"
    }


def get_growth_metrics(company: str, year_range: Optional[int] = 1) -> dict:
    """
    Analyze company growth through year-over-year changes in revenue, earnings, and operating income.
    
    Growth metrics indicate business expansion and competitive positioning:
    - Revenue Growth YoY: Top-line growth showing market share gains and pricing power
    - EPS Growth YoY: Bottom-line earnings growth indicating profitability improvement
    - Operating Income Growth YoY: Core business profitability growth excluding one-time items
    
    Consistent positive growth across these metrics indicates strong business momentum.
    Growth stocks typically show 10%+ annual growth rates.
    
    Formulas:
    - Revenue Growth = ((Current Revenue - Previous Revenue) / Previous Revenue) * 100
    - EPS Growth = ((Current EPS - Previous EPS) / Previous EPS) * 100
    - Operating Income Growth = ((Current Operating Income - Previous Operating Income) / Previous Operating Income) * 100
    
    Args:
        company: Company ticker symbol or name (e.g., 'NVDA', 'TSLA')
        year_range: Number of years to analyze (default: 1 for last year only)
    
    Returns:
        Dictionary containing year-over-year growth rates for revenue, EPS, and operating income
    """
    try:
        # Load required financial data
        financial_data = load_financial_data(company, ['income_statement', 'earnings'])
        income_statement = financial_data["income_statement"]
        earnings = financial_data["earnings"]
        
        # Ensure we have enough data for the requested year range
        max_years = min(year_range, len(income_statement["annualReports"]) - 1)
        
        if max_years == 0:
            return {
                "company": company.upper(),
                "error": "Insufficient data. Need at least 2 years of data to calculate growth."
            }
        
        results = []
        
        # Calculate growth for each year in the range
        for i in range(max_years):
            is_current = income_statement["annualReports"][i]
            is_previous = income_statement["annualReports"][i + 1]
            
            # Find matching earnings data by fiscal year
            current_fiscal_year = is_current["fiscalDateEnding"]
            previous_fiscal_year = is_previous["fiscalDateEnding"]
            
            # Search for matching earnings in annualEarnings
            earnings_current = None
            earnings_previous = None
            
            for earning in earnings["annualEarnings"]:
                if earning["fiscalDateEnding"] == current_fiscal_year:
                    earnings_current = earning
                if earning["fiscalDateEnding"] == previous_fiscal_year:
                    earnings_previous = earning
            
            if not earnings_current or not earnings_previous:
                continue
            
            year_data = _calculate_growth_for_year(is_current, is_previous, earnings_current, earnings_previous)
            results.append(year_data)
        
        if not results:
            return {
                "company": company.upper(),
                "error": "Could not match earnings data with income statement data."
            }
        
        # Return structure based on year_range
        if year_range == 1:
            # Single year - return simplified format
            return {
                "company": income_statement["symbol"],
                **results[0]
            }
        else:
            # Multiple years - return array
            return {
                "company": income_statement["symbol"],
                "yearRange": len(results),
                "data": results
            }
    
    except FileNotFoundError as e:
        return {
            "company": company.upper(),
            "error": f"File not found: {str(e)}"
        }
    except ValueError as e:
        return {
            "company": company.upper(),
            "error": f"Invalid data: {str(e)}"
        }
    except KeyError as e:
        return {
            "company": company.upper(),
            "error": f"Missing required field in financial data: {str(e)}"
        }
    except Exception as e:
        return {
            "company": company.upper(),
            "error": f"Error calculating growth metrics: {str(e)}"
        }
