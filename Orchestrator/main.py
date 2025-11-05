import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import GroupChatOrchestration, RoundRobinGroupChatManager
from semantic_kernel.agents.runtime import InProcessRuntime

from agents.orchestrator_agent import OrchestratorAgent
from agents.market_agent import MarketAgent
from agents.fundamentals_agent import FundamentalsAgent
from agents.news_agent import NewsAgent

# Load environment variables from .env file
load_dotenv()

def agent_response_callback(message):
    print(f"{message.name}: {message.content}")

def create_kernel() -> Kernel:
    """Create and configure the Semantic Kernel with Azure OpenAI."""
    kernel = Kernel()
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

    if not all([azure_endpoint, azure_api_key, azure_deployment_name]):
        raise ValueError("Azure OpenAI configuration is incomplete.")

    chat_completion = AzureChatCompletion(
        endpoint=azure_endpoint,
        api_key=azure_api_key,
        deployment_name=azure_deployment_name,
        api_version=azure_api_version
    )

    kernel.add_service(chat_completion)
    return kernel

async def main():
    """Main function to run the orchestrator agent."""
    kernel = create_kernel()

    # Initialize agents
    market_agent = MarketAgent(kernel)
    fundamentals_agent = FundamentalsAgent(kernel)
    news_agent = NewsAgent(kernel)
    orchestrator_agent = OrchestratorAgent(kernel)

    # Group chat orchestration
    orchestration = GroupChatOrchestration(
        members = [market_agent, fundamentals_agent, news_agent, orchestrator_agent],
        manager = RoundRobinGroupChatManager(max_rounds=5),
        # agent_response_callback=agent_response_callback
    )

    # Example Query
    user_query = "Should I invest in Infosys this month?"
    print(f"🧑 User: {user_query}\n")

    # Runtime setup
    runtime = InProcessRuntime()
    runtime.start()

    # Run the orchestration
    response = await orchestration.invoke(user_query, runtime=runtime)
    value = await response.get()
    
    print(f"***** Final Result *****\n{value}")

if __name__ == "__main__":
    asyncio.run(main())