import os, yaml
from semantic_kernel.agents import ChatCompletionAgent

class OrchestratorAgent(ChatCompletionAgent):
    @classmethod
    async def create(cls, kernel):
        """Factory method to create and initialize OrchestratorAgent"""
        instance = cls(kernel)
        return instance
    
    def __init__(self, kernel):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "orchestrator_prompts.yaml")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)
            instructions = prompts["system"]["goal"]
        else:
            instructions = """You are the Chief Investment Orchestrator.
            
            Your role:
            1. Review responses from MarketAgent (technical analysis) and FundamentalsAgent (financial metrics)
            2. Synthesize their insights into a cohesive investment summary
            3. Provide a clear final recommendation: Buy, Hold, or Avoid

            Response format:
            - **Market Analysis**: Brief summary of technical indicators
            - **Fundamental Analysis**: Brief summary of financial metrics
            - **Overall Assessment**: Combined outlook (1-2 sentences)
            - **Recommendation**: Buy/Hold/Avoid with reasoning

            Be concise, balanced, and investor-oriented."""

        super().__init__(
            name="OrchestratorAgent",
            instructions=instructions,
            kernel=kernel
        )

        self.description = "Synthesizes insights from Market and Fundamentals agents to provide final investment recommendations."