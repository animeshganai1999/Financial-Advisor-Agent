import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import GroupChatOrchestration, RoundRobinGroupChatManager
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import ChatMessageContent

from agents.orchestrator_agent import OrchestratorAgent
from agents.market_agent import MarketAgent
from agents.fundamentals_agent import FundamentalsAgent
from agents.news_agent import NewsAgent

# Load environment variables from .env file
load_dotenv()

def agent_response_callback(message: ChatMessageContent) -> None:
    print(f"**{message.name}**\n{message.content}")

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
    """Main function to run the orchestrator agent with interactive loop."""
    kernel = create_kernel()

    # Initialize agents
    market_agent = await MarketAgent.create(kernel.clone())
    fundamentals_agent = await FundamentalsAgent.create(kernel.clone())
    news_agent = NewsAgent(kernel.clone())
    orchestrator_agent = await OrchestratorAgent.create(kernel.clone())
    
    # Track agents that need cleanup
    agents_with_cleanup = [market_agent, fundamentals_agent]  # Add news_agent here if it has MCP plugin
    
    runtime = None

    try:
        # Runtime setup
        runtime = InProcessRuntime()
        runtime.start()
        
        print("=" * 70)
        print("🤖 Financial Advisor Agent - Interactive Mode")
        print("=" * 70)
        print("Ask questions about stocks, technical indicators, or fundamentals.")
        print("Type 'exit' or 'quit' to stop.\n")
        
        # Track conversation history as list of (role, content) tuples
        conversation_history = []
        
        # Interactive loop
        while True:
            # Get user input
            user_query = input("🧑 You: ").strip()
            
            # Check for exit commands
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\n[INFO] Exiting Financial Advisor Agent...")
                break
            
            # Skip empty input
            if not user_query:
                continue
            
            print()  # Add spacing
            
            # Build enriched query with conversation context
            if conversation_history:
                # Include previous conversation context (last 3 exchanges)
                context_messages = []
                for role, content in conversation_history[-6:]:
                    context_messages.append(f"{role}: {content}")
                
                conversation_context = "\n".join(context_messages)
                enriched_query = f"""Previous conversation:
                {conversation_context}

                Current question: {user_query}

                Please answer the current question, taking into account the conversation history above."""
            else:
                enriched_query = user_query
            
            # Create NEW orchestration for each query to avoid state issues
            orchestration = GroupChatOrchestration(
                members = [market_agent, fundamentals_agent, orchestrator_agent],
                manager = RoundRobinGroupChatManager(max_rounds=3),
                # agent_response_callback=agent_response_callback  # Show agent responses in real-time
            )

            try:
                # print("[DEBUG] Conversation history size:", len(conversation_history))
                
                # Pass enriched query with conversation context
                response = await orchestration.invoke(enriched_query, runtime=runtime)
                
                # print("[DEBUG] Getting response value...")
                value = await response.get()
                # print(f"[DEBUG] Response length: {len(str(value))}")
                
                # Add to conversation history
                conversation_history.append(("User", user_query))
                conversation_history.append(("Assistant", str(value)))
                
                print(f"\n{'='*70}")
                print(f"***** Final Result *****")
                print(f"{'='*70}")
                print(f"{value}")
                print(f"{'='*70}\n")
            
            except Exception as e:
                print(f"\n[ERROR] Error processing query: {e}")
                import traceback
                traceback.print_exc()
                print("Please try again with a different question.\n")
    
    except KeyboardInterrupt:
        print("\n\n[INFO] Interrupted by user (Ctrl+C)")
    
    except Exception as e:
        print(f"\n[ERROR] Error during orchestration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Stop runtime first
        if runtime:
            try:
                await runtime.stop()
            except Exception as e:
                print(f"[WARN] Error stopping runtime: {e}")
        
        # Clean up all agents with MCP connections
        print("\n[INFO] Cleaning up agent connections...")
        for agent in agents_with_cleanup:
            if hasattr(agent, 'cleanup'):
                try:
                    await agent.cleanup()
                except Exception as e:
                    print(f"[WARN] Error cleaning up {agent.name}: {e}")
                    # Suppress the detailed traceback for known async generator cleanup issues
        print("[OK] Shutdown complete")

if __name__ == "__main__":
    import warnings
    
    # Suppress all runtime warnings (includes async generator, coroutine, etc.)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
