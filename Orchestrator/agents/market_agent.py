import os, yaml
from semantic_kernel.agents import ChatCompletionAgent

class MarketAgent(ChatCompletionAgent):
    def __init__(self, kernel):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "market_prompts.yaml")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)
            instructions = prompts["system"]["goal"]
        else:
            instructions = (
                "You are the Market Data Agent. Analyze stock price trends, "
                "momentum indicators (RSI, MACD), and describe the short-term trend clearly."
            )

        super().__init__(
            name="MarketAgent",
            instructions=instructions,
            kernel=kernel
        )

        self.description = "Analyzes market indicators (RSI, MACD, trends) for short-term outlook."