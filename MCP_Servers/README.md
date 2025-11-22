# MCP Servers - Financial Advisor Agent

This directory contains **Model Context Protocol (MCP)** servers that provide specialized financial data and analysis tools to AI agents.

## 📁 Directory Structure

```
MCP_Servers/
├── common/                      # Shared utilities
│   ├── data_loader.py          # Financial data loading functions
│   └── __init__.py
├── fundamentals_mcp/           # Fundamental analysis server
│   ├── server.py               # FastMCP server (Port 8000)
│   └── tools/                  # Financial ratio tools
│       ├── valuation_tool.py
│       ├── profitability_tool.py
│       ├── liquidity_tool.py
│       ├── leverage_tool.py
│       ├── efficiency_tool.py
│       ├── growth_tool.py
│       └── dividend_tool.py
├── market_data_mcp/            # Technical analysis server
│   ├── server.py               # FastMCP server (Port 8001)
│   └── tools/                  # Market data tools
│       ├── indicators_tool.py
│       ├── price_tool.py
│       ├── sentiment_tool.py
│       └── trend_tool.py
├── news_sentiment_mcp/         # News & sentiment server
│   ├── server.py               # FastMCP server (Port 8002)
│   └── tools/                  # News analysis tools
├── run_all_servers.py          # Python launcher script
└── run_all_servers.ps1         # PowerShell launcher script
```

---

## 🚀 Quick Start

### Start All MCP Servers

**Option 1: Python Script (Recommended)**
```powershell
cd MCP_Servers
python run_all_servers.py
```

**Option 2: PowerShell Script**
```powershell
cd MCP_Servers
.\run_all_servers.ps1
```

### Start Individual Servers

```powershell
# Fundamentals MCP (Port 8000)
cd MCP_Servers/fundamentals_mcp
python server.py

# Market Data MCP (Port 8001)
cd MCP_Servers/market_data_mcp
python server.py

# News Sentiment MCP (Port 8002)
cd MCP_Servers/news_sentiment_mcp
python server.py
```

---

## 📊 Server Details

### 1. Fundamentals MCP Server

**Port:** `8000`  
**URL:** `http://127.0.0.1:8000/mcp`  
**Purpose:** Provides comprehensive fundamental analysis metrics

#### Available Tools

| Tool | Description | Key Metrics |
|------|-------------|-------------|
| **`get_valuation_metrics`** | Stock valuation ratios | P/E, P/B, PEG, EV/EBITDA, Price-to-Sales |
| **`get_profitability_ratios`** | Profitability analysis | Gross/Operating/Net Margins, ROE, ROA |
| **`get_liquidity_ratios`** | Short-term financial health | Current Ratio, Quick Ratio, Cash Ratio |
| **`get_leverage_ratios`** | Debt and solvency metrics | Debt-to-Equity, Interest Coverage, Debt-to-EBITDA |
| **`get_efficiency_ratios`** | Asset utilization efficiency | Asset Turnover, Inventory Turnover, Receivables Turnover |
| **`get_growth_metrics`** | Revenue and earnings growth | Revenue Growth, EPS Growth, YoY comparisons |
| **`get_dividend_metrics`** | Dividend analysis | Dividend Yield, Payout Ratio, Dividend Per Share |

#### 📊 Financial Metrics Glossary

**Valuation Metrics** - Determine if a stock is overvalued, undervalued, or fairly priced

- **P/E (Price-to-Earnings)**: Stock price ÷ Earnings per share
  - < 15: Value stock
  - 15-25: Fair value
  - \> 25: Growth/expensive stock
  - Most common valuation metric

- **P/B (Price-to-Book)**: Market cap ÷ Book value (net assets)
  - < 1.0: Potentially undervalued
  - \> 3.0: Premium to assets
  - Compares price to net asset value

- **PEG (Price/Earnings-to-Growth)**: P/E ratio ÷ Earnings growth rate
  - < 1.0: Undervalued relative to growth
  - 1.0-2.0: Fairly valued
  - \> 2.0: Overvalued relative to growth
  - Adjusts P/E for growth expectations

- **EV/EBITDA**: Enterprise value ÷ Earnings before interest, taxes, depreciation & amortization
  - < 10: Value opportunity
  - 10-15: Fair value
  - \> 15: Expensive
  - Capital-structure neutral valuation

- **Price-to-Sales**: Market cap ÷ Total revenue
  - Useful for unprofitable growth companies
  - Lower is generally better

**Profitability Metrics** - Measure efficiency in converting revenue to profit

- **Gross Margin**: (Revenue - Cost of Goods Sold) ÷ Revenue × 100
  - Measures pricing power and production efficiency
  - Higher margins = better pricing power

- **Operating Margin**: Operating income ÷ Revenue × 100
  - Core business profitability before taxes
  - Shows operational efficiency

- **Net Margin**: Net income ÷ Revenue × 100
  - Bottom-line profitability after all expenses
  - Ultimate measure of profitability

- **ROE (Return on Equity)**: Net income ÷ Shareholder equity × 100
  - Returns generated for shareholders
  - \> 15% is excellent
  - \> 20% is exceptional

- **ROA (Return on Assets)**: Net income ÷ Total assets × 100
  - Efficiency in using assets to generate profit
  - Compare within same industry

**Liquidity Metrics** - Assess ability to meet short-term obligations

- **Current Ratio**: Current assets ÷ Current liabilities
  - \> 2.0: Strong liquidity
  - 1.0-2.0: Adequate liquidity
  - < 1.0: Potential solvency issues

- **Quick Ratio (Acid Test)**: (Current assets - Inventory) ÷ Current liabilities
  - \> 1.0: Healthy liquidity
  - < 1.0: May struggle with immediate obligations
  - More conservative than current ratio

- **Cash Ratio**: Cash & equivalents ÷ Current liabilities
  - \> 0.5: Solid cash position
  - Most conservative liquidity measure
  - Shows ability to pay debts immediately

**Leverage Metrics** - Measure financial risk and debt sustainability

- **Debt-to-Equity**: Total debt ÷ Shareholder equity
  - < 1.0: Conservative capital structure
  - 1.0-2.0: Moderate leverage
  - \> 2.0: High leverage/risk
  - Lower is generally safer

- **Interest Coverage**: Operating income ÷ Interest expense
  - \> 3.0: Healthy debt service capability
  - 1.5-3.0: Adequate coverage
  - < 1.5: Risky - may struggle to pay interest

- **Debt-to-EBITDA**: Total debt ÷ EBITDA
  - < 3.0: Generally healthy
  - 3.0-4.0: Moderate debt load
  - \> 4.0: High debt burden
  - Measures years to repay debt with EBITDA

**Efficiency Metrics** - Evaluate asset utilization and operational efficiency

- **Asset Turnover**: Revenue ÷ Total assets
  - Higher = better asset utilization
  - Varies significantly by industry

- **Inventory Turnover**: Cost of Goods Sold ÷ Average inventory
  - Higher = faster inventory movement
  - Lower = potential obsolescence risk

- **Receivables Turnover**: Revenue ÷ Accounts receivable
  - Higher = faster collection of payments
  - Industry-dependent benchmark

**Growth Metrics** - Track expansion and earnings momentum

- **Revenue Growth**: YoY revenue change percentage
  - Indicates market share gains or expansion

- **EPS Growth**: YoY earnings per share change
  - Shows profitability improvement

- **Quarter-over-Quarter Growth**: Sequential period comparison
  - Reveals recent momentum trends

**Dividend Metrics** - Analyze income distribution to shareholders

- **Dividend Yield**: Annual dividend per share ÷ Stock price × 100
  - Higher yield = more income
  - 2-4% is typical for mature companies

- **Payout Ratio**: Dividends ÷ Net income × 100
  - < 50%: Sustainable with room to grow
  - 50-70%: Moderate payout
  - \> 70%: May be at risk in downturns

- **Dividend Per Share (DPS)**: Total dividends ÷ Shares outstanding
  - Tracks absolute dividend amount

#### Example Usage
```python
# Get valuation metrics for IBM
result = get_valuation_metrics("IBM")
# Returns: PE, PB, PEG, EV/EBITDA ratios

# Get profitability over 3 years
result = get_profitability_ratios("AAPL", year_range=3)
# Returns: Margins, ROE, ROA for each year
```

#### Data Sources
- **Overview Data**: Company fundamentals (OVERVIEW.json)
- **Income Statement**: Revenue, expenses, net income (INCOME_STATEMENT.json)
- **Balance Sheet**: Assets, liabilities, equity (BALANCE_SHEET.json)
- **Earnings**: EPS, quarterly earnings (EARNINGS.json)

---

### 2. Market Data MCP Server

**Port:** `8001`  
**URL:** `http://127.0.0.1:8001/mcp`  
**Purpose:** Provides technical analysis and real-time market data

#### Available Tools

| Tool | Description | Key Indicators |
|------|-------------|----------------|
| **`get_technical_indicators`** | Technical analysis metrics | RSI, MACD, SMA, EMA, Beta, 52-week range |
| **`get_price_data`** | Current and historical prices | Open, High, Low, Close, Volume |
| **`get_price_trends`** | Price trend analysis | Trend direction, momentum, support/resistance |
| **`get_market_sentiment`** | Market sentiment indicators | Analyst ratings, sentiment scores |

#### Technical Indicators Details

**RSI (Relative Strength Index)**
- Range: 0-100
- Interpretation:
  - RSI > 70: Overbought (potential sell signal)
  - RSI < 30: Oversold (potential buy signal)
  - RSI 40-60: Neutral

**MACD (Moving Average Convergence Divergence)**
- Components: MACD Line, Signal Line, Histogram
- Signals:
  - MACD crosses above Signal: Bullish
  - MACD crosses below Signal: Bearish

**Moving Averages**
- SMA 20-day: Short-term trend
- SMA 50-day: Medium-term trend
- SMA 200-day: Long-term trend
- EMA 12-day: Fast exponential average

**Beta**
- Measures volatility vs. market
- Beta = 1.0: Moves with market
- Beta > 1.0: More volatile
- Beta < 1.0: Less volatile

#### Example Usage
```python
# Get all technical indicators for IBM
result = get_technical_indicators("IBM")
# Returns: RSI, MACD, moving averages, Beta, 52-week range

# Get current price data
result = get_price_data("AAPL")
# Returns: Latest prices and volume
```

#### Data Sources
- **Intraday Data**: Real-time price series (TIME_SERIES_INTRADAY.json)
- **Overview Data**: Beta, 52-week range (OVERVIEW.json)

---

### 3. News Sentiment MCP Server

**Port:** `8002`  
**URL:** `http://127.0.0.1:8002/mcp`  
**Purpose:** News analysis and sentiment scoring

#### Status
⚠️ **Under Development** - Server placeholder created, tools implementation pending

#### Planned Tools
- `get_news_headlines`: Latest news for a company
- `get_sentiment_score`: Aggregate sentiment analysis
- `get_news_impact`: News impact on stock price

---

## 🔧 Technical Architecture

### FastMCP Framework

Each server uses **FastMCP** for HTTP-based MCP implementation:

```python
from fastmcp import FastMCP

mcp = FastMCP(
    name="Server Name",
    instructions="Server description",
    version="1.0.0"
)

# Auto-discovery registers all tool functions
auto_register_tools()
```

### Auto-Discovery Pattern

Tools are **automatically registered** from the `tools/` directory:

```python
def auto_register_tools(package_name="tools"):
    package = importlib.import_module(package_name)
    package_path = os.path.dirname(package.__file__)
    
    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        module = importlib.import_module(f"{package_name}.{module_name}")
        
        for name, func in vars(module).items():
            if inspect.isfunction(func) and not name.startswith("_"):
                mcp.tool()(func)
                print(f"[OK] Registered tool: {name}")
```

**Benefits:**
- No manual tool registration required
- Add new tools by creating files in `tools/` directory
- Functions with `_` prefix are private helpers (not registered)

### Data Loader

Shared data loading logic in `common/data_loader.py`:

```python
from common.data_loader import load_financial_data, load_time_series, load_overview

# Load multiple data types
data = load_financial_data("IBM", ['overview', 'income_statement'])

# Load intraday price data
prices = load_time_series("AAPL")
```

---

## 🔌 Integration with Agents

### Agent Connection Pattern

```python
from semantic_kernel.plugins import MCPStreamableHttpPlugin

class MarketAgent(ChatCompletionAgent):
    @classmethod
    async def create(cls, kernel):
        instance = cls(kernel)
        await instance.initialize_plugin()
        return instance
    
    async def initialize_plugin(self):
        mcp_url = os.getenv("MARKET_MCP_URL", "http://127.0.0.1:8001/mcp")
        self.mcp_plugin = await MCPStreamableHttpPlugin.create_from_url(
            name="market_data_mcp",
            url=mcp_url
        )
        self.kernel.add_plugin(self.mcp_plugin)
```

### Environment Configuration

Set MCP URLs in `.env`:

```bash
# MCP Server URLs
FUNDAMENTALS_MCP_URL=http://127.0.0.1:8000/mcp
MARKET_MCP_URL=http://127.0.0.1:8001/mcp
NEWS_MCP_URL=http://127.0.0.1:8002/mcp
```

---

## 📝 Adding New Tools

### Step 1: Create Tool File

```python
# tools/new_tool.py
from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.data_loader import load_financial_data

def get_custom_metric(company: str) -> dict:
    """
    Tool description that appears in agent context.
    
    Args:
        company: Company ticker symbol
    
    Returns:
        Dictionary with metric data
    """
    data = load_financial_data(company, ['overview'])
    return {
        "company": company,
        "metric": data["overview"].get("SomeMetric", 0)
    }
```

### Step 2: Restart Server

The tool is **automatically registered** on server restart - no manual registration needed!

---

## 🐛 Debugging

### View Registered Tools

Each server prints registered tools on startup:

```
[OK] Registered tool: get_valuation_metrics from valuation_tool
[OK] Registered tool: get_profitability_ratios from profitability_tool
...
```

### Test MCP Endpoints

```powershell
# Check server health
curl http://127.0.0.1:8000/mcp

# View available tools (requires MCP client)
# Use Semantic Kernel or MCP Inspector
```

### Common Issues

**Port Already in Use:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process by PID
taskkill /PID <pid> /F
```

**Import Errors:**
- Verify `common/data_loader.py` exists
- Check `sys.path.insert()` in tool files
- Ensure `__init__.py` files exist in all directories

**Tool Not Registering:**
- Function name must NOT start with `_`
- Must be a function (not class or variable)
- File must be in `tools/` directory

---

## 📚 Dependencies

```bash
# Core MCP Framework
fastmcp

# Data Processing
statistics  # Built-in Python module

# Common utilities use standard library only
```

---

## 🚦 Port Allocation

| Server | Port | Protocol | Status |
|--------|------|----------|--------|
| Fundamentals MCP | 8000 | HTTP/SSE | ✅ Active |
| Market Data MCP | 8001 | HTTP/SSE | ✅ Active |
| News Sentiment MCP | 8002 | HTTP/SSE | 🚧 Planned |

---

## 📖 Additional Resources

- **FastMCP Documentation**: [GitHub - fastmcp](https://github.com/jlowin/fastmcp)
- **MCP Protocol Spec**: [Model Context Protocol](https://modelcontextprotocol.io/)
- **Semantic Kernel MCP Plugin**: [SK MCP Docs](https://learn.microsoft.com/semantic-kernel)

---

## 🤝 Contributing

### Adding a New MCP Server

1. Create directory: `my_server_mcp/`
2. Add `server.py` with FastMCP instance
3. Create `tools/` directory with tool functions
4. Update `run_all_servers.py` to include new server
5. Add MCP URL to `.env` file
6. Document in this README

### Tool Development Guidelines

- **Docstrings**: Describe tool purpose, args, and returns
- **Error Handling**: Return error dict if data unavailable
- **Type Hints**: Use `typing` for parameters and returns
- **Helper Functions**: Prefix with `_` to exclude from registration
- **Data Loading**: Use `common.data_loader` for consistency

---

## 📄 License

Part of the Financial Advisor Agent project.
