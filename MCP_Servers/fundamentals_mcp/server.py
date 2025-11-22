import importlib
import pkgutil
import os
import inspect
from fastmcp import FastMCP

# Initialize MCP instance
mcp = FastMCP(
    name="Fundamentals MCP",
    instructions="Provides financial ratios and market indicators",
    version="1.0.0"
)

# Automatically discover and register all tool functions in the `tools` package
def auto_register_tools(package_name="tools"):
    package = importlib.import_module(package_name)
    package_path = os.path.dirname(package.__file__)
    
    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        module = importlib.import_module(f"{package_name}.{module_name}")
        
        for name, func in vars(module).items():
            # Only register actual functions (not classes, modules, etc.)
            if inspect.isfunction(func) and not name.startswith("_"):
                # Register the function as a tool using the decorator pattern
                registered_func = mcp.tool()(func)
                print(f"[OK] Registered tool: {name} from {module_name}")

auto_register_tools()

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
    # mcp.run()