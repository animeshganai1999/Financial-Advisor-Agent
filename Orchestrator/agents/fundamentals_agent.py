import os, yaml
from semantic_kernel.agents import ChatCompletionAgent

class FundamentalsAgent(ChatCompletionAgent):
    def __init__(self, kernel):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "fundamentals_prompts.yaml")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)
            instructions = prompts["system"]["goal"]
        else:
            instructions = (
                "You are the Fundamentals Agent. Summarize the company's financial health, "
                "key ratios (P/E, ROE), and long-term value outlook in 2 sentences."
            )

        super().__init__(
            name="FundamentalsAgent",
            instructions=instructions,
            kernel=kernel
        )

        self.description = "Provides financial and valuation insights about the company."