import os
import json
from pathlib import Path
from typing import Optional
from .data_loader import load_financial_data


def _calculate_inventory_turnover(cogs: float, inventory_current: float, inventory_previous: float) -> float:
    """Calculate Inventory Turnover ratio."""
    avg_inventory = (inventory_current + inventory_previous) / 2
    return round(cogs / avg_inventory, 2)


def _calculate_asset_turnover(revenue: float, assets_current: float, assets_previous: float) -> float:
    """Calculate Asset Turnover ratio."""
    avg_assets = (assets_current + assets_previous) / 2
    return round(revenue / avg_assets, 2)


def _calculate_receivable_turnover(revenue: float, receivables_current: float, receivables_previous: float) -> float:
    """Calculate Receivable Turnover ratio."""
    avg_receivables = (receivables_current + receivables_previous) / 2
    return round(revenue / avg_receivables, 2)


def _calculate_ratios_for_year(bs_current: dict, bs_previous: dict, is_current: dict) -> dict:
    """
    Calculate all efficiency ratios for a single year.
    
    Args:
        bs_current: Current year balance sheet data
        bs_previous: Previous year balance sheet data
        is_current: Current year income statement data
        
    Returns:
        Dictionary with calculated ratios for the year
    """
    # Extract values and convert to float
    cogs = float(is_current["costofGoodsAndServicesSold"])
    total_revenue = float(is_current["totalRevenue"])
    
    inventory_current = float(bs_current["inventory"])
    inventory_previous = float(bs_previous["inventory"])
    
    total_assets_current = float(bs_current["totalAssets"])
    total_assets_previous = float(bs_previous["totalAssets"])
    
    receivables_current = float(bs_current["currentNetReceivables"])
    receivables_previous = float(bs_previous["currentNetReceivables"])
    
    # Calculate efficiency ratios
    inventory_turnover = _calculate_inventory_turnover(cogs, inventory_current, inventory_previous)
    asset_turnover = _calculate_asset_turnover(total_revenue, total_assets_current, total_assets_previous)
    receivable_turnover = _calculate_receivable_turnover(total_revenue, receivables_current, receivables_previous)
    
    return {
        "fiscalYear": bs_current["fiscalDateEnding"],
        "InventoryTurnover": inventory_turnover,
        "AssetTurnover": asset_turnover,
        "ReceivableTurnover": receivable_turnover
    }


def get_efficiency_ratios(company: str, year_range: Optional[int] = 1) -> dict:
    """
    Analyze operational efficiency through asset utilization and turnover ratios.
    
    Efficiency ratios measure how effectively a company uses its assets and manages operations:
    - Inventory Turnover: How many times inventory is sold and replaced (higher is better, indicates efficient inventory management)
    - Asset Turnover: Revenue generated per dollar of assets (measures overall asset utilization efficiency)
    - Receivable Turnover: How quickly company collects payments from customers (higher indicates better credit management)
    
    Higher ratios generally indicate more efficient operations and better asset management.
    
    Formulas:
    - Inventory Turnover = Cost of Goods Sold / Average Inventory
    - Asset Turnover = Total Revenue / Average Total Assets
    - Receivable Turnover = Total Revenue / Average Accounts Receivable
    
    Args:
        company: Company ticker symbol or name (e.g., 'AAPL', 'Tesla')
        year_range: Number of years to analyze (default: 1 for last year only)
    
    Returns:
        Dictionary containing efficiency ratios for the specified year range
    """
    try:
        # Load required financial data using shared data loader
        financial_data = load_financial_data(company, ['balance_sheet', 'income_statement'])
        balance_sheet = financial_data["balance_sheet"]
        income_statement = financial_data["income_statement"]
        
        # Ensure we have enough data for the requested year range
        max_years = min(year_range, len(balance_sheet["annualReports"]) - 1)
        
        if max_years == 0:
            return {
                "company": company.upper(),
                "error": "Insufficient data. Need at least 2 years of data to calculate ratios."
            }
        
        results = []
        
        # Calculate ratios for each year in the range
        for i in range(max_years):
            bs_current = balance_sheet["annualReports"][i]
            bs_previous = balance_sheet["annualReports"][i + 1]
            is_current = income_statement["annualReports"][i]
            
            year_data = _calculate_ratios_for_year(bs_current, bs_previous, is_current)
            results.append(year_data)
        
        # Return structure based on year_range
        if year_range == 1:
            # Single year - return simplified format
            return {
                "company": balance_sheet["symbol"],
                **results[0]
            }
        else:
            # Multiple years - return array
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
            "error": f"Error calculating efficiency ratios: {str(e)}"
        }
