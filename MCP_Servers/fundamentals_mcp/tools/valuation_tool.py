from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path to import common module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_financial_data


def get_valuation_metrics(company: str) -> dict:
    """
    Determine stock valuation through key pricing multiples and ratios.
    
    Valuation metrics help assess if a stock is overvalued, undervalued, or fairly priced:
    - P/E (Price-to-Earnings): Stock price / EPS - most common valuation metric (<15 value, 15-25 fair, >25 growth/expensive)
    - P/B (Price-to-Book): Market cap / Book value - compares price to net asset value (<1.0 may indicate undervaluation)
    - PEG (P/E to Growth): P/E / earnings growth rate - adjusts P/E for growth (<1.0 undervalued, >2.0 overvalued)
    - EV/EBITDA: Enterprise value / EBITDA - capital-structure neutral valuation (<10 value, >15 expensive)
    
    Compare ratios to industry peers and historical averages for context.
    
    Args:
        company: Company ticker symbol or name (e.g., 'AMZN', 'WMT')
    
    Returns:
        Dictionary containing P/E, P/B, PEG, and EV/EBITDA ratios
    """
    try:
        # Load required financial data
        financial_data = load_financial_data(company, ['overview'])
        overview = financial_data["overview"]
        
        # Extract valuation metrics from overview
        pe_ratio = float(overview.get("PERatio", 0))
        pb_ratio = float(overview.get("PriceToBookRatio", 0))
        peg_ratio = float(overview.get("PEGRatio", 0))
        ev_to_ebitda = float(overview.get("EVToEBITDA", 0))
        
        # Additional valuation metrics
        price_to_sales = float(overview.get("PriceToSalesRatioTTM", 0))
        trailing_pe = float(overview.get("TrailingPE", 0))
        forward_pe = float(overview.get("ForwardPE", 0))
        
        return {
            "company": overview["Symbol"],
            "PE": pe_ratio,
            "PB": pb_ratio,
            "PEG": peg_ratio,
            "EV_EBITDA": ev_to_ebitda,
            "PriceToSales": price_to_sales,
            "TrailingPE": trailing_pe,
            "ForwardPE": forward_pe,
            "MarketCap": float(overview.get("MarketCapitalization", 0))
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
            "error": f"Error fetching valuation metrics: {str(e)}"
        }
