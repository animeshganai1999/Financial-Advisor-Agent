import os
import yaml
from dotenv import load_dotenv
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin

# Load environment variables
load_dotenv()


class MarketAgent(ChatCompletionAgent):
    """
    Market Data Agent - Expert in Technical Analysis and Market Trends.
    
    This agent specializes in analyzing stock market data and technical indicators:
    - Latest Price Information (current price, volume, price changes)
    - Technical Indicators (RSI, MACD, SMA, EMA, Beta)
    - Price Trend Analysis (support/resistance, momentum, volatility)
    - Market Sentiment (bullish/bearish signals, buying/selling pressure)
    
    The agent connects to the Market Data MCP server to fetch real-time market data
    and provides expert analysis on price trends, momentum, and short-term outlook.
    """
    
    def __init__(self, kernel):
        """
        Initialize the Market Data Agent.
        
        Args:
            kernel: Semantic Kernel instance with AI services configured
        """
        # Load YAML configuration
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "market_prompts.yaml")
        with open(prompt_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        system = config.get("system", {})
        self._prompt_template = config["prompts"]["analyze_market"]

        # Build comprehensive system instruction
        full_instruction = (
            f"Role: {system.get('role', 'Market Technical Analyst')}\n\n"
            f"Goal: {system.get('goal', 'Analyze stock market behavior using technical indicators')}\n\n"
            f"Style: {system.get('style', 'Professional and concise')}\n\n"
            f"Capabilities:\n"
            f"You have access to a comprehensive Market Data MCP plugin that provides:\n"
            f"- Latest price and volume data via get_latest_price()\n"
            f"- Technical indicators (RSI, MACD, SMA, EMA, Beta) via get_technical_indicators()\n"
            f"- Price trend analysis (support/resistance, momentum) via get_price_trend_summary()\n"
            f"- Market sentiment analysis (bullish/bearish signals) via get_market_sentiment()\n\n"
            f"Guidelines:\n"
            f"- Identify trend direction (bullish, bearish, sideways)\n"
            f"- Cite specific indicator values (RSI, MACD, moving averages)\n"
            f"- Explain what the indicators suggest for short-term outlook\n"
            f"- Highlight key support and resistance levels\n"
            f"- Assess market sentiment and momentum\n"
            f"- Keep analysis concise and actionable\n"
        )

        super().__init__(
            name="MarketAgent",
            instructions=full_instruction,
            kernel=kernel
        )

        # Agent description for orchestrator
        self.description = (
            "Expert technical analyst specializing in market data and price trends. "
            "Analyzes technical indicators (RSI, MACD, moving averages), price patterns, "
            "support/resistance levels, and market sentiment. "
            "Provides short-term outlook and momentum analysis."
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
            Fully initialized MarketAgent instance
            
        Example:
            agent = await MarketAgent.create(kernel)
        """
        agent = cls(kernel)
        await agent.initialize_plugin()
        return agent

    async def initialize_plugin(self):
        """
        Initialize and connect to the Market Data MCP server asynchronously.
        
        This method establishes a connection to the MCP streamable-http server running at
        http://127.0.0.1:8001/mcp and registers all available market data tools.
        
        Raises:
            ConnectionError: If unable to connect to the MCP server
        """
        if self._plugin_initialized:
            print(f"[INFO] {self.name} MCP plugin already initialized")
            return
            
        try:
            # Get MCP URL from environment variable
            mcp_url = os.getenv("MARKETDATA_MCP_URL", "http://127.0.0.1:8001/mcp")
            
            # Create and connect to MCP plugin
            self._mcp_plugin = MCPStreamableHttpPlugin(
                name="MarketDataMCP",
                description="Provides stock market data, technical indicators, price trends, and market sentiment analysis.",
                url=mcp_url
            )
            
            # Connect to the MCP server
            await self._mcp_plugin.connect()
            
            # Register plugin with kernel
            self.kernel.add_plugin(self._mcp_plugin)
            
            self._plugin_initialized = True
            print(f"[OK] {self.name} connected to Market Data MCP server")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize Market Data MCP plugin: {str(e)}")
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
            except RuntimeError as e:
                if "cancel scope" in str(e):
                    # Known issue with MCP SDK async cleanup - safe to ignore
                    print(f"[OK] {self.name} MCP connection closed (with async cleanup warning)")
                else:
                    raise
            except Exception as e:
                print(f"[ERROR] Error during cleanup: {str(e)}")