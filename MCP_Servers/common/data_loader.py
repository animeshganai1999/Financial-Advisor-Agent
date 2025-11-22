"""
Shared financial data loader utility for all MCP servers.

This module handles loading financial data for companies.
Currently loads from local JSON files in MOC_Data folder.
TODO: Replace with actual API calls to fetch real-time data.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


def load_financial_data(company: str, data_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Load financial data for a company.
    
    Currently loads from local JSON files in MOC_Data folder.
    TODO: Replace with actual API calls to fetch real-time data.
    
    Args:
        company: Company ticker symbol (e.g., 'IBM', 'AAPL')
        data_types: List of data types to load. Options:
                   - 'balance_sheet': Balance sheet data
                   - 'income_statement': Income statement data
                   - 'overview': Company overview with key metrics
                   - 'earnings': Earnings data
                   - 'time_series': Intraday price data
                   If None, loads all available data types.
        
    Returns:
        Dictionary with requested financial data
        Keys are the data types (e.g., 'balance_sheet', 'income_statement')
        
    Raises:
        FileNotFoundError: If required data files are not found
        ValueError: If invalid data_type is specified
        
    Example:
        # Load specific data types
        data = load_financial_data('IBM', ['balance_sheet', 'income_statement'])
        
        # Load all data
        data = load_financial_data('IBM')
    """
    # TODO: Replace this with actual API calls
    # Example API endpoints:
    # - Alpha Vantage: https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={company}
    # - Financial Modeling Prep: https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}
    # - Yahoo Finance API
    # - Polygon.io
    # - Finnhub
    
    base_dir = Path(__file__).parent.parent.parent / "MOC_Data"
    
    # Mapping of data types to file names
    file_mapping = {
        'balance_sheet': 'BALANCE_SHEET.json',
        'income_statement': 'INCOME_STATEMENT.json',
        'overview': 'OVERVIEW.json',
        'earnings': 'EARNINGS.json',
        'time_series': 'TIME_SERIES_INTRADAY.json'
    }
    
    # If no data types specified, load all
    if data_types is None:
        data_types = list(file_mapping.keys())
    
    # Validate data types
    invalid_types = set(data_types) - set(file_mapping.keys())
    if invalid_types:
        raise ValueError(f"Invalid data types: {invalid_types}. Valid types are: {list(file_mapping.keys())}")
    
    result = {}
    missing_files = []
    
    # Load each requested data type
    for data_type in data_types:
        file_name = file_mapping[data_type]
        file_path = base_dir / file_name
        
        if not file_path.exists():
            missing_files.append(f"{file_name} at {file_path}")
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                result[data_type] = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_name}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading {file_name}: {str(e)}")
    
    # Check if any required files were missing
    if missing_files:
        raise FileNotFoundError(f"Required data files not found: {', '.join(missing_files)}")
    
    return result


# Convenience functions for specific data types

def load_balance_sheet(company: str) -> Dict[str, Any]:
    """Load only balance sheet data."""
    data = load_financial_data(company, ['balance_sheet'])
    return data['balance_sheet']


def load_income_statement(company: str) -> Dict[str, Any]:
    """Load only income statement data."""
    data = load_financial_data(company, ['income_statement'])
    return data['income_statement']


def load_overview(company: str) -> Dict[str, Any]:
    """Load only company overview data."""
    data = load_financial_data(company, ['overview'])
    return data['overview']


def load_earnings(company: str) -> Dict[str, Any]:
    """Load only earnings data."""
    data = load_financial_data(company, ['earnings'])
    return data['earnings']


def load_time_series(company: str) -> Dict[str, Any]:
    """Load only time series/price data."""
    data = load_financial_data(company, ['time_series'])
    return data['time_series']
