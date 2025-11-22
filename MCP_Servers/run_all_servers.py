"""
MCP Servers Launcher
Runs all MCP servers concurrently in a single process.
"""

import asyncio
import subprocess
import sys
from pathlib import Path


async def run_fundamentals_server():
    """Run Fundamentals MCP server on port 8000"""
    print("[INFO] Starting Fundamentals MCP Server on http://127.0.0.1:8000")
    try:
        server_path = Path(__file__).parent / "fundamentals_mcp" / "server.py"
        process = await asyncio.create_subprocess_exec(
            sys.executable, str(server_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Stream output
        async def stream_output(stream, prefix):
            while True:
                line = await stream.readline()
                if not line:
                    break
                print(f"[Fundamentals] {line.decode().rstrip()}")
        
        await asyncio.gather(
            stream_output(process.stdout, "[Fundamentals]"),
            stream_output(process.stderr, "[Fundamentals]")
        )
    except Exception as e:
        print(f"[ERROR] Fundamentals MCP Server error: {e}")


async def run_market_data_server():
    """Run Market Data MCP server on port 8001"""
    print("[INFO] Starting Market Data MCP Server on http://127.0.0.1:8001")
    try:
        server_path = Path(__file__).parent / "market_data_mcp" / "server.py"
        process = await asyncio.create_subprocess_exec(
            sys.executable, str(server_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Stream output
        async def stream_output(stream, prefix):
            while True:
                line = await stream.readline()
                if not line:
                    break
                print(f"[MarketData] {line.decode().rstrip()}")
        
        await asyncio.gather(
            stream_output(process.stdout, "[MarketData]"),
            stream_output(process.stderr, "[MarketData]")
        )
    except Exception as e:
        print(f"[ERROR] Market Data MCP Server error: {e}")


# Uncomment when news_sentiment_mcp is ready
# async def run_news_server():
#     """Run News Sentiment MCP server on port 8002"""
#     print("[INFO] Starting News Sentiment MCP Server on http://127.0.0.1:8002")
#     try:
#         server_path = Path(__file__).parent / "news_sentiment_mcp" / "server.py"
#         process = await asyncio.create_subprocess_exec(
#             sys.executable, str(server_path),
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE
#         )
#         
#         # Stream output
#         async def stream_output(stream, prefix):
#             while True:
#                 line = await stream.readline()
#                 if not line:
#                     break
#                 print(f"[News] {line.decode().rstrip()}")
#         
#         await asyncio.gather(
#             stream_output(process.stdout, "[News]"),
#             stream_output(process.stderr, "[News]")
#         )
#     except Exception as e:
#         print(f"[ERROR] News Sentiment MCP Server error: {e}")


async def main():
    """Run all MCP servers concurrently"""
    print("="*60)
    print("Starting All MCP Servers...")
    print("="*60)
    
    # Create tasks for all servers
    tasks = [
        asyncio.create_task(run_fundamentals_server()),
        asyncio.create_task(run_market_data_server()),
        # Uncomment when news_sentiment_mcp is ready
        # asyncio.create_task(run_news_server()),
    ]
    
    print("\n[OK] All servers started successfully!")
    print("[INFO] Press Ctrl+C to stop all servers\n")
    print("="*60)
    
    try:
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\n\n[INFO] Shutting down all MCP servers...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        print("[OK] All servers stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[OK] Shutdown complete")
