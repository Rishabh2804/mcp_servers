import asyncio
from typing import Optional
from contextlib import AsyncExitStack
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
import os

# Initialize Gemini client - API key is required
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable is required. "
        "Get your API key from https://makersuite.google.com/app/apikey and set it with: "
        "export GEMINI_API_KEY='your-key-here'"
    )
gemini = genai.Client(api_key=api_key)


def get_result(query, tools):
    """
    Use Gemini to determine which tool to use and extract arguments from the query.
    
    Args:
        query: User's natural language query
        tools: Available MCP tools
        
    Returns:
        dict: Contains 'tool' name and 'args' dictionary
    """
    tools_with_desc = {
        tool.name: tool.description
        for tool in tools
    }
    
    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""Given the user query: "{query}"
        
        Available tools with descriptions:
        {tools_with_desc}
        
        Your task:
        1. Choose the tool that best matches the user's intent
        2. Extract the required arguments from the query
        3. Return a JSON object with:
           - "tool": the tool name
           - "args": dictionary of argument names and values
        
        Important:
        - Return ONLY valid JSON
        - Do NOT include markdown code blocks or backticks
        - Match argument names exactly as shown in tool descriptions
        - For criterion, choose from: "lowest price", "highest rating", "best value", "premium"
        
        Example response format:
        {{"tool": "flipkart_search", "args": {{"item": "laptop", "criterion": "best value"}}}}
        """,
    )
    
    # Clean up response and parse
    result_text = response.text.strip()
    # Remove markdown code blocks
    result_text = result_text.replace('```json', '').replace('```', '').strip()
    # Remove 'json' prefix if present
    if result_text.startswith('json'):
        result_text = result_text[4:].strip()
    
    try:
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing Gemini response as JSON: {e}")
        print(f"Response was: {result_text}")
        raise


class MCPClient:
    """MCP Client for connecting to Flipkart MCP Server."""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
    
    async def connect_with_server(self, query):
        """
        Connect to the MCP server and process the query.
        
        Args:
            query: User's natural language query about Flipkart shopping
            
        Returns:
            dict: Tool name and arguments to use
        """
        server_params = StdioServerParameters(
            command='python',
            args=['server.py'],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.read, self.write = stdio_transport
        
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read, self.write)
        )
        
        await self.session.initialize()
        
        # Get available tools
        response = await self.session.list_tools()
        tools = response.tools
        
        # Use Gemini to determine which tool to use
        result = get_result(query, tools)
        
        return result


async def main():
    """Main entry point for the Flipkart MCP client."""
    client = MCPClient()
    
    print("=" * 60)
    print("Flipkart MCP Client")
    print("=" * 60)
    print("\nWelcome! I can help you shop on Flipkart.")
    print("\nExample queries:")
    print("  - Search for wireless earbuds with best value")
    print("  - Find the cheapest laptop")
    print("  - Compare smartphones under 20000")
    print("  - Filter laptops between 30000 and 50000 rupees")
    print("\nType 'exit' to quit\n")
    print("=" * 60)
    
    try:
        user_inp = input("\nYour query: ")
        
        while user_inp.lower() != 'exit':
            try:
                # Connect and get tool selection
                result = await client.connect_with_server(user_inp)
                tool_name = result['tool']
                args = result['args']
                
                print(f"\n📋 Using tool: {tool_name}")
                print(f"📦 Arguments: {args}")
                print("\n🔄 Executing...")
                
                # Call the selected tool
                response = await client.session.call_tool(tool_name, args)
                
                print(f"\n✅ Result: {response.content[0].text}")
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try rephrasing your query or type 'exit' to quit.")
            
            user_inp = input("\nYour query: ")
    
    finally:
        await client.exit_stack.aclose()
        print("\n👋 Thank you for using Flipkart MCP Client!")


if __name__ == "__main__":
    asyncio.run(main())
