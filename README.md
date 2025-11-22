# Financial Advisor Agent

> **AI-powered multi-agent system for comprehensive stock analysis and investment recommendations**

A sophisticated financial analysis platform that combines **Semantic Kernel**, **Azure OpenAI**, and **Model Context Protocol (MCP)** to provide intelligent stock research through specialized AI agents.

---

## 🎯 Overview

The Financial Advisor Agent orchestrates multiple specialized AI agents to analyze stocks from different perspectives:

- **💹 Market Agent**: Technical analysis with indicators (RSI, MACD, moving averages, Beta)
- **📊 Fundamentals Agent**: Financial metrics analysis (P/E, ROE, debt ratios, profitability)
- **📰 News Agent**: Sentiment analysis from news and market reports *(planned)*
- **🎯 Orchestrator Agent**: Synthesizes insights and provides final Buy/Hold/Avoid recommendations

Each agent connects to dedicated **MCP servers** that provide real-time financial data and analysis tools.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query                                │
│           "Should I invest in IBM?"                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Orchestrator (main.py)                          │
│    GroupChatOrchestration + InProcessRuntime                 │
│         Azure OpenAI (gpt-4o)                                │
└─────────┬───────────┬────────────┬──────────────────────────┘
          │           │            │
          ▼           ▼            ▼
    ┌─────────┐ ┌──────────┐ ┌──────────────┐
    │ Market  │ │Fundamen- │ │ Orchestrator │
    │ Agent   │ │tals Agent│ │    Agent     │
    └────┬────┘ └────┬─────┘ └──────────────┘
         │           │
         │           │
         ▼           ▼
    ┌─────────┐ ┌──────────┐
    │Market   │ │Fundamen- │
    │Data MCP │ │tals MCP  │
    │:8001    │ │:8000     │
    └─────────┘ └──────────┘
         │           │
         └─────┬─────┘
               ▼
       ┌──────────────┐
       │ Financial    │
       │ Data (JSON)  │
       │ - Prices     │
       │ - Financials │
       │ - Earnings   │
       └──────────────┘
```

### Communication Flow

1. **User sends query** → Orchestrator receives it
2. **Round 1**: Market Agent analyzes technical indicators using Market Data MCP
3. **Round 2**: Fundamentals Agent analyzes financial metrics using Fundamentals MCP
4. **Round 3**: Orchestrator Agent synthesizes both analyses into final recommendation
5. **Result**: Comprehensive investment analysis with Buy/Hold/Avoid decision

**Shared Memory**: `GroupChatOrchestration` maintains chat history visible to all agents

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.12+
python --version

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create `.env` file in the root directory:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# MCP Server URLs
FUNDAMENTALS_MCP_URL=http://127.0.0.1:8000/mcp
MARKET_MCP_URL=http://127.0.0.1:8001/mcp
NEWS_MCP_URL=http://127.0.0.1:8002/mcp
```

### Run the System

**Terminal 1: Start MCP Servers**
```powershell
cd MCP_Servers
python run_all_servers.py
```

**Terminal 2: Run Orchestrator**
```powershell
cd Orchestrator
python main.py
```

---

## 📁 Project Structure

```
Financial-Advisor-Agent/
├── README.md                    # This file
├── .env                         # Environment configuration
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies
│
├── MCP_Servers/                 # Model Context Protocol servers
│   ├── README.md                # Detailed MCP documentation
│   ├── run_all_servers.py       # Launch all servers
│   ├── run_all_servers.ps1      # PowerShell launcher
│   │
│   ├── common/                  # Shared utilities
│   │   ├── data_loader.py       # Financial data loading
│   │   └── __init__.py
│   │
│   ├── fundamentals_mcp/        # Fundamental analysis (Port 8000)
│   │   ├── server.py
│   │   └── tools/
│   │       ├── valuation_tool.py      # P/E, P/B, PEG, EV/EBITDA
│   │       ├── profitability_tool.py  # Margins, ROE, ROA
│   │       ├── liquidity_tool.py      # Current/Quick/Cash ratios
│   │       ├── leverage_tool.py       # Debt ratios
│   │       ├── efficiency_tool.py     # Asset turnover
│   │       ├── growth_tool.py         # Revenue/EPS growth
│   │       └── dividend_tool.py       # Dividend metrics
│   │
│   ├── market_data_mcp/         # Technical analysis (Port 8001)
│   │   ├── server.py
│   │   └── tools/
│   │       ├── indicators_tool.py     # RSI, MACD, SMA, EMA, Beta
│   │       ├── price_tool.py          # Price data
│   │       ├── sentiment_tool.py      # Market sentiment
│   │       └── trend_tool.py          # Trend analysis
│   │
│   └── news_sentiment_mcp/      # News analysis (Port 8002) [Planned]
│       ├── server.py
│       └── tools/
│
├── Orchestrator/                # Main orchestration logic
│   ├── main.py                  # Entry point
│   └── agents/
│       ├── market_agent.py          # Technical analysis agent
│       ├── fundamentals_agent.py    # Financial metrics agent
│       ├── news_agent.py            # News sentiment agent [Stub]
│       ├── orchestrator_agent.py    # Synthesis agent
│       └── prompts/                 # Agent instruction prompts
│           ├── market_prompts.yaml
│           ├── fundamentals_prompts.yaml
│           ├── news_prompts.yaml
│           └── orchestrator_prompts.yaml
│
├── MOC_Data/                    # Mock financial data (JSON)
│   ├── OVERVIEW.json            # Company overview & ratios
│   ├── INCOME_STATEMENT.json    # Revenue, expenses, profits
│   ├── BALANCE_SHEET.json       # Assets, liabilities, equity
│   ├── EARNINGS.json            # Quarterly earnings data
│   └── TIME_SERIES_INTRADAY.json # Price history
│
└── Test/                        # Testing scripts
    └── main.py
```

---

## 🤖 Agent Details

### Market Agent
- **Purpose**: Technical analysis and market trend evaluation
- **Tools**: RSI, MACD, SMA/EMA, Beta, 52-week range, price trends
- **MCP Server**: `market_data_mcp` (Port 8001)
- **Output**: Technical indicators with overbought/oversold signals

### Fundamentals Agent
- **Purpose**: Financial health and valuation analysis
- **Tools**: 7 categories covering 30+ financial metrics
  - Valuation (P/E, P/B, PEG, EV/EBITDA)
  - Profitability (Margins, ROE, ROA)
  - Liquidity (Current/Quick/Cash ratios)
  - Leverage (Debt ratios, Interest coverage)
  - Efficiency (Asset turnover metrics)
  - Growth (Revenue/EPS growth)
  - Dividends (Yield, payout ratio)
- **MCP Server**: `fundamentals_mcp` (Port 8000)
- **Output**: Comprehensive fundamental analysis

### Orchestrator Agent
- **Purpose**: Synthesize all agent insights into final recommendation
- **Input**: Chat history from Market Agent and Fundamentals Agent
- **Output**: 
  - Market Analysis summary
  - Fundamental Analysis summary
  - Overall Assessment
  - **Recommendation**: Buy / Hold / Avoid with reasoning

---

## 🛠️ Key Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Semantic Kernel** | AI orchestration framework | Latest |
| **Azure OpenAI** | LLM for agent reasoning | gpt-4o |
| **FastMCP** | Model Context Protocol server | Latest |
| **Python** | Core language | 3.12+ |
| **Asyncio** | Asynchronous execution | Built-in |
| **YAML** | Agent prompt configuration | Built-in |

---

## 📊 Financial Data Coverage

### Available Metrics

**Technical Indicators**
- RSI (Relative Strength Index): 0-100 scale, overbought/oversold detection
- MACD (Moving Average Convergence Divergence): Trend momentum
- SMA/EMA: Short/medium/long-term trend analysis
- Beta: Volatility vs. market benchmark
- 52-Week Range: Annual high/low price levels

**Fundamental Ratios** (30+ metrics)
- Valuation: P/E, P/B, PEG, EV/EBITDA, Price-to-Sales
- Profitability: Gross/Operating/Net Margins, ROE, ROA
- Liquidity: Current, Quick, Cash ratios
- Leverage: Debt-to-Equity, Interest Coverage, Debt-to-EBITDA
- Efficiency: Asset, Inventory, Receivables Turnover
- Growth: Revenue Growth, EPS Growth, YoY trends
- Dividends: Yield, Payout Ratio, Dividend Per Share

See `MCP_Servers/README.md` for detailed metric definitions and interpretation guidelines.

---

## 🎮 Usage Examples

### Example 1: Technical Analysis Query
```python
user_query = "Give me technical indicators for IBM"

# System automatically routes to Market Agent only
# Output: RSI, MACD, SMA, EMA, Beta, 52-week range
```

### Example 2: Fundamental Analysis Query
```python
user_query = "What's AAPL's P/E ratio and profitability?"

# System routes to Fundamentals Agent
# Output: Valuation metrics, margin analysis, ROE/ROA
```

### Example 3: Comprehensive Analysis
```python
user_query = "Should I invest in MSFT? Provide complete analysis."

# All agents participate:
# Round 1: Market Agent → Technical indicators
# Round 2: Fundamentals Agent → Financial metrics
# Round 3: Orchestrator → Synthesized recommendation
```

---

## 🔧 Configuration

### Customizing Agent Behavior

Edit YAML prompt files in `Orchestrator/agents/prompts/`:

```yaml
# fundamentals_prompts.yaml
system:
  goal: >
    Analyze fundamental financial health using metrics like P/E, ROE, 
    debt ratios, and profitability margins.
  style: "Data-driven, objective, conservative"
```

### Adding New MCP Tools

1. Create tool file in `MCP_Servers/{server}/tools/new_tool.py`
2. Define function with docstring and type hints
3. Restart MCP server (auto-discovery registers new tool)
4. Tool becomes available to agents automatically

---

## 🔍 How Agents Communicate

**Shared Memory Pattern**: `GroupChatOrchestration` maintains conversation history

```python
orchestration = GroupChatOrchestration(
    members = [market_agent, fundamentals_agent, orchestrator_agent],
    manager = RoundRobinGroupChatManager(max_rounds=3)
)
```

**Turn-by-turn flow**:
1. Market Agent sees: User query → Responds with technical data
2. Fundamentals Agent sees: User query + Market response → Adds financial data
3. Orchestrator sees: All previous messages → Synthesizes final answer

No explicit message passing needed - chat history is shared context.

---

## 🚨 Troubleshooting

### Common Issues

**MCP Server Connection Errors**
```
RuntimeError: Attempted to exit cancel scope in a different task
```
- **Solution**: Agents implement `cleanup()` method with proper async handling
- MCP plugin connections cleaned up in `finally` block

**Port Already in Use**
```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <pid> /F
```

**Import Errors in MCP Tools**
- Verify `sys.path.insert()` includes parent directories
- Check `__init__.py` files exist in all packages
- Ensure `common/data_loader.py` is accessible

**Agent Not Finding Tools**
- Check MCP server console for "[OK] Registered tool:" messages
- Verify tool functions don't start with `_` (reserved for helpers)
- Confirm `.env` has correct MCP URLs

---

## 📈 Roadmap

- [x] Market Agent with technical indicators
- [x] Fundamentals Agent with financial ratios
- [x] Orchestrator Agent for synthesis
- [x] MCP auto-discovery pattern
- [x] Async cleanup for MCP connections
- [ ] News Sentiment Agent implementation
- [ ] Real-time data integration (Alpha Vantage API)
- [ ] Portfolio tracking and optimization
- [ ] Backtesting framework
- [ ] Web UI dashboard
- [ ] Multi-stock comparison analysis

---

## 📚 Additional Documentation

- **[MCP Servers README](MCP_Servers/README.md)**: Detailed MCP server documentation with metric glossary
- **[FastMCP Documentation](https://github.com/jlowin/fastmcp)**: MCP framework reference
- **[Semantic Kernel Docs](https://learn.microsoft.com/semantic-kernel)**: Agent orchestration guide

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Adding new financial analysis tools
- Implementing News Sentiment Agent
- Performance optimization
- Test coverage expansion
- Documentation improvements

---

## 📄 License

This project is for educational and research purposes.

---

## 🙏 Acknowledgments

- **Microsoft Semantic Kernel** for agent orchestration framework
- **FastMCP** for streamlined MCP server implementation
- **Azure OpenAI** for powerful language model capabilities

---

**Built with ❤️ for intelligent financial analysis**

