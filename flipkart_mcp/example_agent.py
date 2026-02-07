#!/usr/bin/env python3
"""
Example: Integrating Flipkart MCP Server with an AI Agent

This example shows how to build a simple AI agent that uses the Flipkart MCP server
to help users shop on Flipkart.
"""

import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class FlipkartShoppingAgent:
    """
    A simple AI agent that uses the Flipkart MCP server to help users shop.
    """
    
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()
        self.tools = []
    
    async def initialize(self):
        """Connect to the Flipkart MCP server and initialize the session."""
        print("Initializing Flipkart Shopping Agent...")
        
        server_params = StdioServerParameters(
            command='python',
            args=['server.py'],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        read, write = stdio_transport
        
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        
        await self.session.initialize()
        
        # Get available tools
        response = await self.session.list_tools()
        self.tools = response.tools
        
        print(f"✓ Connected! {len(self.tools)} tools available:")
        for tool in self.tools:
            print(f"  - {tool.name}")
        print()
    
    async def search_product(self, item: str, criterion: str = "best value"):
        """
        Search for a product on Flipkart.
        
        Args:
            item: Product to search for
            criterion: Selection criteria (lowest price, highest rating, best value, premium)
        
        Returns:
            Result from the MCP server
        """
        print(f"🔍 Searching for: {item}")
        print(f"📊 Criterion: {criterion}")
        
        response = await self.session.call_tool("flipkart_search", {
            "item": item,
            "criterion": criterion
        })
        
        result = response.content[0].text
        print(f"✅ {result}\n")
        return result
    
    async def compare_products(self, item: str, num_products: int = 3):
        """
        Compare multiple products.
        
        Args:
            item: Product to compare
            num_products: Number of products to compare
        
        Returns:
            Result from the MCP server
        """
        print(f"📊 Comparing {num_products} options for: {item}")
        
        response = await self.session.call_tool("flipkart_compare", {
            "item": item,
            "num_products": num_products
        })
        
        result = response.content[0].text
        print(f"✅ {result}\n")
        return result
    
    async def filter_by_price(self, item: str, min_price: int, max_price: int):
        """
        Filter products by price range.
        
        Args:
            item: Product to search for
            min_price: Minimum price in INR
            max_price: Maximum price in INR
        
        Returns:
            Result from the MCP server
        """
        print(f"💰 Filtering {item} between ₹{min_price} - ₹{max_price}")
        
        response = await self.session.call_tool("flipkart_price_filter", {
            "item": item,
            "min_price": min_price,
            "max_price": max_price
        })
        
        result = response.content[0].text
        print(f"✅ {result}\n")
        return result
    
    async def close(self):
        """Clean up and close the connection."""
        await self.exit_stack.aclose()
        print("Agent disconnected.")


async def example_shopping_session():
    """
    Example shopping session demonstrating the agent's capabilities.
    """
    agent = FlipkartShoppingAgent()
    
    try:
        await agent.initialize()
        
        print("=" * 60)
        print("Example 1: Search for wireless earbuds")
        print("=" * 60)
        await agent.search_product("wireless earbuds", "best value")
        
        print("=" * 60)
        print("Example 2: Find the cheapest laptop")
        print("=" * 60)
        await agent.search_product("laptop", "lowest price")
        
        print("=" * 60)
        print("Example 3: Compare smartphones")
        print("=" * 60)
        await agent.compare_products("smartphone under 20000", num_products=5)
        
        print("=" * 60)
        print("Example 4: Filter laptops by price")
        print("=" * 60)
        await agent.filter_by_price("laptop", min_price=30000, max_price=50000)
        
    finally:
        await agent.close()


async def interactive_mode():
    """
    Interactive mode for chatting with the shopping agent.
    """
    agent = FlipkartShoppingAgent()
    
    try:
        await agent.initialize()
        
        print("=" * 60)
        print("Interactive Shopping Mode")
        print("=" * 60)
        print("\nCommands:")
        print("  search <item> [criterion]  - Search for a product")
        print("  compare <item> [num]       - Compare products")
        print("  filter <item> <min> <max>  - Filter by price range")
        print("  help                       - Show this help")
        print("  exit                       - Exit the program")
        print()
        
        while True:
            command = input(">>> ").strip()
            
            if not command:
                continue
            
            if command.lower() == "exit":
                break
            
            if command.lower() == "help":
                print("\nCommands:")
                print("  search <item> [criterion]  - Search for a product")
                print("  compare <item> [num]       - Compare products")
                print("  filter <item> <min> <max>  - Filter by price range")
                print("  help                       - Show this help")
                print("  exit                       - Exit the program\n")
                continue
            
            parts = command.split()
            cmd = parts[0].lower()
            
            try:
                if cmd == "search" and len(parts) >= 2:
                    item = " ".join(parts[1:-1]) if len(parts) > 2 else parts[1]
                    criterion = parts[-1] if len(parts) > 2 else "best value"
                    await agent.search_product(item, criterion)
                
                elif cmd == "compare" and len(parts) >= 2:
                    num = int(parts[-1]) if parts[-1].isdigit() else 3
                    item = " ".join(parts[1:-1]) if parts[-1].isdigit() else " ".join(parts[1:])
                    await agent.compare_products(item, num)
                
                elif cmd == "filter" and len(parts) >= 4:
                    item = " ".join(parts[1:-2])
                    min_price = int(parts[-2])
                    max_price = int(parts[-1])
                    await agent.filter_by_price(item, min_price, max_price)
                
                else:
                    print("Invalid command. Type 'help' for usage.\n")
            
            except Exception as e:
                print(f"Error: {e}\n")
    
    finally:
        await agent.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(example_shopping_session())
