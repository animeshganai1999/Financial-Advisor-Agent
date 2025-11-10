"""
Test script for Fundamentals MCP Server integration with Semantic Kernel.

This script demonstrates how to:
1. Initialize Semantic Kernel with Azure OpenAI
2. Connect to the Fundamentals MCP server
3. Use MCP tools to fetch financial data
4. Execute AI-powered financial analysis

Prerequisites:
- Fundamentals MCP server running on http://127.0.0.1:8000
- Azure OpenAI credentials in environment variables
"""

import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPSsePlugin
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings


async def test_mcp_connection():
    """Test basic MCP server connection and tool availability."""
    print("=" * 80)
    print("TEST 1: MCP Server Connection")
    print("=" * 80)
    
    try:
        # Initialize MCP plugin
        mcp_plugin = MCPSsePlugin(
            name="FundamentalsMCP",
            description="Financial fundamentals analysis tools",
            url="http://127.0.0.1:8000"
        )
        
        # Connect to MCP server
        await mcp_plugin.connect()
        print("✓ Successfully connected to Fundamentals MCP server")
        
        # List available tools
        print("\nAvailable MCP Tools:")
        functions = mcp_plugin.functions
        for i, (func_name, func) in enumerate(functions.items(), 1):
            print(f"  {i}. {func_name}: {func.description}")
        
        # Close connection
        await mcp_plugin.close()
        print("\n✓ Connection closed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_direct_tool_call():
    """Test direct MCP tool invocation without AI."""
    print("\n" + "=" * 80)
    print("TEST 2: Direct MCP Tool Call")
    print("=" * 80)
    
    try:
        # Connect to MCP
        mcp_plugin = MCPSsePlugin(
            name="FundamentalsMCP",
            description="Financial fundamentals analysis tools",
            url="http://127.0.0.1:8000"
        )
        await mcp_plugin.connect()
        
        # Create kernel and add plugin
        kernel = Kernel()
        kernel.add_plugin(mcp_plugin)
        
        # Test get_valuation_metrics
        print("\nCalling: get_valuation_metrics(company='IBM')")
        valuation_func = kernel.get_function("FundamentalsMCP", "get_valuation_metrics")
        result = await kernel.invoke(valuation_func, company="IBM")
        print(f"Result: {result}")
        
        # Test get_profitability_ratios
        print("\nCalling: get_profitability_ratios(company='IBM')")
        profitability_func = kernel.get_function("FundamentalsMCP", "get_profitability_ratios")
        result = await kernel.invoke(profitability_func, company="IBM")
        print(f"Result: {result}")
        
        await mcp_plugin.close()
        print("\n✓ Direct tool calls successful")
        return True
        
    except Exception as e:
        print(f"✗ Direct tool call failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_ai_powered_analysis():
    """Test AI-powered financial analysis using MCP tools."""
    print("\n" + "=" * 80)
    print("TEST 3: AI-Powered Analysis with MCP Tools")
    print("=" * 80)
    
    try:
        # Initialize Kernel
        kernel = Kernel()
        
        # Add Azure OpenAI service
        azure_openai = AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        kernel.add_service(azure_openai)
        
        # Connect to MCP and add plugin
        mcp_plugin = MCPSsePlugin(
            name="FundamentalsMCP",
            description="Financial fundamentals analysis tools",
            url="http://127.0.0.1:8000"
        )
        await mcp_plugin.connect()
        kernel.add_plugin(mcp_plugin)
        
        # Create chat history
        chat_history = ChatHistory()
        chat_history.add_system_message(
            "You are a financial analyst. Use the available fundamental analysis tools "
            "to provide detailed investment insights. Always cite specific metrics and ratios."
        )
        
        # Test query
        user_query = "Analyze IBM's financial health. Focus on profitability, valuation, and liquidity."
        print(f"\nUser Query: {user_query}")
        chat_history.add_user_message(user_query)
        
        # Configure execution settings with auto function calling
        execution_settings = AzureChatPromptExecutionSettings(
            temperature=0.7,
            max_tokens=1500,
        )
        execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
        
        # Get AI response with tool usage
        print("\nAI Analysis (with MCP tool calls):")
        print("-" * 80)
        
        response = await kernel.invoke_prompt(
            function_name="analyze_company",
            plugin_name="chat",
            prompt="{{$chat_history}}",
            chat_history=chat_history,
            settings=execution_settings
        )
        
        print(response)
        print("-" * 80)
        
        # Close MCP connection
        await mcp_plugin.close()
        print("\n✓ AI-powered analysis successful")
        return True
        
    except Exception as e:
        print(f"✗ AI-powered analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_tools():
    """Test using multiple MCP tools in sequence."""
    print("\n" + "=" * 80)
    print("TEST 4: Multiple Tool Calls")
    print("=" * 80)
    
    try:
        # Setup MCP plugin
        mcp_plugin = MCPSsePlugin(
            name="FundamentalsMCP",
            description="Financial fundamentals analysis tools",
            url="http://127.0.0.1:8000"
        )
        await mcp_plugin.connect()
        
        # Create kernel and add plugin
        kernel = Kernel()
        kernel.add_plugin(mcp_plugin)
        
        # Test multiple tools
        tools_to_test = [
            ("get_valuation_metrics", {"company": "IBM"}),
            ("get_profitability_ratios", {"company": "IBM", "year_range": 1}),
            ("get_liquidity_ratios", {"company": "IBM"}),
            ("get_leverage_ratios", {"company": "IBM"}),
            ("get_efficiency_ratios", {"company": "IBM"}),
            ("get_growth_metrics", {"company": "IBM"}),
            ("get_dividend_info", {"company": "IBM"}),
        ]
        
        results = {}
        for tool_name, params in tools_to_test:
            print(f"\nTesting: {tool_name}")
            try:
                func = kernel.get_function("FundamentalsMCP", tool_name)
                result = await kernel.invoke(func, **params)
                results[tool_name] = result
                print(f"✓ {tool_name}: Success")
                print(f"  Sample data: {str(result)[:100]}...")
            except Exception as e:
                print(f"✗ {tool_name}: Failed - {str(e)}")
        
        await mcp_plugin.close()
        
        print(f"\n✓ Tested {len(results)}/{len(tools_to_test)} tools successfully")
        return len(results) == len(tools_to_test)
        
    except Exception as e:
        print(f"✗ Multiple tool test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("\n")
    print("█" * 80)
    print("  FUNDAMENTALS MCP SERVER TEST SUITE")
    print("█" * 80)
    print("\nEnsure the MCP server is running: python server.py")
    print("Server should be at: http://127.0.0.1:8000\n")
    
    input("Press Enter to start tests...")
    
    # Run tests
    results = {
        "Connection Test": await test_mcp_connection(),
        "Direct Tool Call": await test_direct_tool_call(),
        "Multiple Tools": await test_multiple_tools(),
        "AI Analysis": await test_ai_powered_analysis(),
    }
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<50} {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())