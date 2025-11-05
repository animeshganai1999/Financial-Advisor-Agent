import os, yaml
from semantic_kernel.agents import ChatCompletionAgent

class NewsAgent(ChatCompletionAgent):
    def __init__(self, kernel):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "news_prompts.yaml")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)
            instructions = prompts["system"]["goal"]
        else:
            instructions = (
                "You are the News Sentiment Agent. Analyze recent news tone, "
                "summarize investor sentiment (positive, neutral, or negative), and explain why."
            )

        super().__init__(
            name="NewsAgent",
            instructions=instructions,
            kernel=kernel
        )

        self.description = "Summarizes news sentiment and analyst tone affecting investor confidence."