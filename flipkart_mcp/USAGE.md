# Flipkart MCP Server - Usage Examples

This document provides practical examples of using the Flipkart MCP Server.

## Quick Start

1. **Install Dependencies**
   ```bash
   cd flipkart_mcp
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Set Up API Key**
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. **Run the Interactive Client**
   ```bash
   python client.py
   ```

## Example Queries

### Basic Product Search

**Query:** "Search for wireless earbuds with best value"

This will:
- Search Flipkart for wireless earbuds
- Analyze products based on price-to-quality ratio
- Select and click on the best value option

### Finding the Cheapest Product

**Query:** "Find the cheapest laptop"

This will:
- Search for laptops
- Sort by price
- Select the lowest-priced option

### High-Quality Search

**Query:** "Find the highest rated headphones"

This will:
- Search for headphones
- Analyze ratings and reviews
- Select the top-rated product

### Product Comparison

**Query:** "Compare smartphones under 20000"

This will:
- Search for smartphones in that price range
- Capture screenshots of multiple products
- Save comparison screenshots

### Price Range Filtering

**Query:** "Filter laptops between 30000 and 50000 rupees"

This will:
- Search for laptops
- Apply price filters
- Show products in the specified range

## Programmatic Usage

You can also use the MCP server programmatically from Python:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

async def search_product():
    exit_stack = AsyncExitStack()
    
    try:
        # Connect to server
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
        
        await session.initialize()
        
        # Call a tool
        response = await session.call_tool("flipkart_search", {
            "item": "wireless mouse",
            "criterion": "best value"
        })
        
        print(response.content[0].text)
        
    finally:
        await exit_stack.aclose()

asyncio.run(search_product())
```

## Integration with AI Agents

### Claude Desktop Integration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or equivalent:

```json
{
  "mcpServers": {
    "flipkart": {
      "command": "python",
      "args": ["/absolute/path/to/flipkart_mcp/server.py"]
    }
  }
}
```

### Custom Agent Integration

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Your agent code here
# Use the Flipkart MCP server as one of your agent's tools
```

## Tips for Best Results

1. **Be Specific**: Include product details in your search
   - Good: "wireless earbuds with noise cancellation"
   - Better: "Sony wireless earbuds with active noise cancellation"

2. **Use Clear Criteria**:
   - "lowest price" - For budget shopping
   - "highest rating" - For quality focus
   - "best value" - For balanced choice
   - "premium" - For high-end products

3. **Price Filters**: Use realistic ranges
   - ₹5,000 - ₹10,000 for budget items
   - ₹30,000 - ₹50,000 for mid-range laptops
   - ₹1,00,000+ for premium products

4. **Check Screenshots**: Review captured screenshots in the `screenshots/` directory to see what the AI analyzed

## Troubleshooting

### Browser doesn't launch
Make sure Playwright is installed:
```bash
playwright install chromium
```

### API Key Issues
Set your own Gemini API key:
```bash
export GEMINI_API_KEY="your-key-here"
```

### Connection Errors
Verify the server is accessible:
```bash
python test_server.py
```

## Notes

- The browser runs in visible mode (headless=False) for transparency
- Screenshots are saved to help debug and verify selections
- Rate limiting may apply - avoid rapid consecutive searches
- Selectors may need updates if Flipkart changes their UI
