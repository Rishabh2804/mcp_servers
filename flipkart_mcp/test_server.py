#!/usr/bin/env python3
"""
Test script to verify the Flipkart MCP server implementation.
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack


async def test_server_connection():
    """Test that we can connect to the server and list tools."""
    print("Testing Flipkart MCP Server...")
    print("-" * 50)
    
    exit_stack = AsyncExitStack()
    
    try:
        # Start the server
        server_params = StdioServerParameters(
            command='python',
            args=['server.py'],
            env=None
        )
        
        stdio_transport = await exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        read, write = stdio_transport
        
        session = await exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        
        # Initialize the session
        await session.initialize()
        print("✓ Server connection established")
        
        # List available tools
        response = await session.list_tools()
        tools = response.tools
        
        print(f"\n✓ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}")
            if hasattr(tool, 'description'):
                desc_lines = tool.description.split('\n')
                print(f"    {desc_lines[0][:70]}...")
        
        # Verify expected tools
        expected_tools = ['flipkart_search', 'flipkart_compare', 'flipkart_price_filter']
        found_tools = [tool.name for tool in tools]
        
        print("\nTool Verification:")
        for expected in expected_tools:
            if expected in found_tools:
                print(f"  ✓ {expected}")
            else:
                print(f"  ✗ {expected} (MISSING!)")
        
        if set(expected_tools) == set(found_tools):
            print("\n✅ All tests passed! Server is working correctly.")
            return True
        else:
            print("\n⚠️  Some tools are missing!")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await exit_stack.aclose()


if __name__ == "__main__":
    success = asyncio.run(test_server_connection())
    exit(0 if success else 1)
