import os, yaml
from semantic_kernel.agents import ChatCompletionAgent

class OrchestratorAgent(ChatCompletionAgent):
    def __init__(self, kernel):
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "orchestrator_prompts.yaml")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)
            instructions = prompts["system"]["goal"]

        super().__init__(name="OrchestratorAgent",
            instructions=instructions,
            kernel=kernel)

        self.description = "Coordinates other agents and produces final investment recommendations."