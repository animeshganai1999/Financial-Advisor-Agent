import os
import yaml
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin


class FundamentalsAgent(ChatCompletionAgent):
    """
    Fundamentals Analysis Agent - Expert in Financial Analysis and Company Valuation.
    
    This agent specializes in analyzing fundamental financial data including:
    - Valuation Metrics (P/E, P/B, PEG, EV/EBITDA)
    - Profitability Ratios (Gross Margin, Operating Margin, Net Margin, ROE, ROA)
    - Liquidity Ratios (Current Ratio, Quick Ratio, Cash Ratio)
    - Leverage Ratios (Debt-to-Equity, Interest Coverage, Debt-to-EBITDA)
    - Efficiency Ratios (Inventory Turnover, Asset Turnover, Receivable Turnover)
    - Growth Metrics (Revenue Growth, EPS Growth, Operating Income Growth)
    - Dividend Information (Yield, Payout Ratio, Ex-Dividend Date)
    - Technical Indicators (Moving Averages, Beta, 52-week High/Low)
    
    The agent connects to the Fundamentals MCP server to fetch real-time financial data
    and provides expert analysis on company fundamentals, investment quality, and valuation.
    """
    
    def __init__(self, kernel):
        """
        Initialize the Fundamentals Agent.
        
        Args:
            kernel: Semantic Kernel instance with AI services configured
        """
        # Load YAML configuration
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "fundamentals_prompts.yaml")
        with open(prompt_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        system = config.get("system", {})
        self._prompt_template = config["prompts"]["analyze_fundamentals"]

        # Build comprehensive system instruction
        full_instruction = (
            f"Role: {system.get('role', 'Financial Fundamentals Analyst')}\n\n"
            f"Goal: {system.get('goal', 'Analyze company fundamentals and provide investment insights')}\n\n"
            f"Style: {system.get('style', 'Professional, data-driven, and analytical')}\n\n"
            f"Capabilities:\n"
            f"You have access to a comprehensive Fundamentals MCP plugin that provides:\n"
            f"- Valuation metrics (P/E, P/B, PEG, EV/EBITDA) via get_valuation_metrics()\n"
            f"- Profitability ratios (margins, ROE, ROA) via get_profitability_ratios()\n"
            f"- Liquidity ratios (current, quick, cash) via get_liquidity_ratios()\n"
            f"- Leverage ratios (debt metrics) via get_leverage_ratios()\n"
            f"- Efficiency ratios (turnover metrics) via get_efficiency_ratios()\n"
            f"- Growth metrics (YoY growth rates) via get_growth_metrics()\n"
            f"- Dividend information via get_dividend_info()\n"
            f"- Technical indicators via get_technical_indicators()\n\n"
            f"Guidelines:\n"
            f"- Always cite specific metrics and ratios in your analysis\n"
            f"- Compare metrics against industry benchmarks when relevant\n"
            f"- Explain what the numbers mean for investors\n"
            f"- Highlight both strengths and concerns\n"
            f"- Provide context for unusual values\n"
            f"- Support recommendations with data\n"
        )

        super().__init__(
            name="FundamentalsAgent",
            instructions=full_instruction,
            kernel=kernel
        )

        # Agent description for orchestrator
        self.description = (
            "Expert financial analyst specializing in fundamental analysis. "
            "Analyzes valuation metrics, profitability ratios, liquidity, leverage, "
            "efficiency, growth metrics, dividends, and technical indicators. "
            "Provides comprehensive investment analysis based on company fundamentals."
        )
        
        # Store plugin reference for cleanup
        self._mcp_plugin = None
        self._plugin_initialized = False

    @classmethod
    async def create(cls, kernel):
        """
        Factory method to create and initialize the agent asynchronously.
        
        This is the recommended way to instantiate the agent as it properly
        initializes the MCP plugin connection.
        
        Args:
            kernel: Semantic Kernel instance with AI services configured
            
        Returns:
            Fully initialized FundamentalsAgent instance
            
        Example:
            agent = await FundamentalsAgent.create(kernel)
        """
        agent = cls(kernel)
        await agent.initialize_plugin()
        return agent

    async def initialize_plugin(self):
        """
        Initialize and connect to the Fundamentals MCP server asynchronously.
        
        This method establishes a connection to the MCP streamable-http server running at
        http://127.0.0.1:8000/mcp and registers all available fundamental analysis tools.
        
        Raises:
            ConnectionError: If unable to connect to the MCP server
        """
        if self._plugin_initialized:
            print(f"[INFO] {self.name} MCP plugin already initialized")
            return
            
        try:
            # Create and connect to MCP plugin
            self._mcp_plugin = MCPStreamableHttpPlugin(
                name="FundamentalsMCP",
                description="Provides comprehensive fundamental financial metrics and ratios for companies.",
                url="http://127.0.0.1:8000/mcp"
            )
            
            # Connect to the MCP server
            await self._mcp_plugin.connect()
            
            # Register plugin with kernel
            self.kernel.add_plugin(self._mcp_plugin)
            
            self._plugin_initialized = True
            print(f"[OK] {self.name} connected to Fundamentals MCP server")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize Fundamentals MCP plugin: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    async def cleanup(self):
        """
        Clean up resources and close MCP connection.
        
        Should be called when the agent is no longer needed.
        """
        if self._mcp_plugin and self._plugin_initialized:
            try:
                await self._mcp_plugin.close()
                self._plugin_initialized = False
                self._mcp_plugin = None
                print(f"[OK] {self.name} MCP connection closed")
            except Exception as e:
                print(f"[ERROR] Error during cleanup: {str(e)}")
    