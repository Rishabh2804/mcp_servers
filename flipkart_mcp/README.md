# Flipkart MCP Server

A Model Context Protocol (MCP) server for autonomous shopping on Flipkart, India's leading e-commerce platform.

## 🎯 Features

- **Smart Product Search**: Search for products on Flipkart with AI-powered selection based on various criteria
- **Price Filtering**: Filter products by price range
- **Product Comparison**: Compare multiple products side-by-side
- **Multiple Selection Criteria**: Choose products by lowest price, highest rating, best value, or premium options
- **Visual Analysis**: Uses Gemini AI to analyze product listings from screenshots

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Playwright browser automation

## 🚀 Installation

1. Navigate to the flipkart_mcp directory:
```bash
cd flipkart_mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Set up your Gemini API key (optional - a default key is provided for testing):
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## 🎮 Usage

### Running the Client

The easiest way to interact with the Flipkart MCP server is through the client:

```bash
python client.py
```

### Example Queries

Once the client is running, you can use natural language queries like:

- "Search for wireless earbuds with best value"
- "Find the cheapest laptop"
- "Compare smartphones under 20000"
- "Filter laptops between 30000 and 50000 rupees"
- "Find the highest rated headphones"

### Available Tools

The MCP server exposes three tools:

#### 1. flipkart_search
Search for a product and select the best match based on criteria.

**Parameters:**
- `item` (string): Product name or description
- `criterion` (string, optional): Selection criteria
  - "lowest price" - Find the cheapest option
  - "highest rating" - Find the best rated product
  - "best value" - Balance between price and quality (default)
  - "premium" - Select high-end options

**Example:**
```python
await client.session.call_tool("flipkart_search", {
    "item": "wireless earbuds",
    "criterion": "best value"
})
```

#### 2. flipkart_compare
Compare multiple products for the same search query.

**Parameters:**
- `item` (string): Product to search and compare
- `num_products` (int, optional): Number of products to compare (default: 3)

**Example:**
```python
await client.session.call_tool("flipkart_compare", {
    "item": "smartphone under 20000",
    "num_products": 5
})
```

#### 3. flipkart_price_filter
Search and filter products by price range.

**Parameters:**
- `item` (string): Product to search for
- `min_price` (int): Minimum price in Indian Rupees (₹)
- `max_price` (int): Maximum price in Indian Rupees (₹)

**Example:**
```python
await client.session.call_tool("flipkart_price_filter", {
    "item": "laptop",
    "min_price": 30000,
    "max_price": 50000
})
```

## 🏗️ Architecture

The Flipkart MCP server follows the standard MCP architecture:

```
┌─────────────┐
│   Client    │  (client.py)
│             │  - Handles user interaction
│             │  - Connects to MCP server
└──────┬──────┘
       │
       │ MCP Protocol (stdio)
       │
┌──────▼──────┐
│   Server    │  (server.py)
│             │  - Exposes MCP tools
│             │  - Routes requests
└──────┬──────┘
       │
       │
┌──────▼──────┐
│   Browser   │  (flipkart_browser.py)
│   Module    │  - Playwright automation
│             │  - Gemini AI analysis
└─────────────┘
```

## 📸 Screenshots

The server captures screenshots during operation and saves them in the `screenshots/` directory:
- `flipkart_search.jpg` - Initial search results
- `flipkart_result_1.jpg` through `flipkart_result_10.jpg` - Scrolled results
- `flipkart_product_page.jpg` - Selected product page
- `flipkart_comparison.jpg` - Product comparison view
- `flipkart_before_filter.jpg` / `flipkart_after_filter.jpg` - Price filtering

## 🔧 Customization

### Using Your Own Gemini API Key

For production use, it's recommended to use your own Gemini API key:

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set it as an environment variable:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

### Modifying Selection Criteria

You can extend the selection criteria in `flipkart_browser.py` by modifying the `analyze_and_select_item()` function to include additional logic for product analysis.

## 🤝 Integration with AI Agents

This MCP server can be integrated with any AI agent that supports the Model Context Protocol. Simply configure your agent to connect to this server via stdio transport.

### Example Integration with Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "flipkart": {
      "command": "python",
      "args": ["/path/to/flipkart_mcp/server.py"]
    }
  }
}
```

## ⚠️ Important Notes

1. **Browser Automation**: The server launches a visible browser window (headless=False) to interact with Flipkart. This is intentional for transparency and debugging.

2. **Rate Limiting**: Be mindful of Flipkart's rate limits. Excessive automated requests may result in temporary blocks.

3. **Selector Stability**: Flipkart may change their website structure. If the automation breaks, selectors in `flipkart_browser.py` may need updating.

4. **API Key**: A demo Gemini API key is included for testing, but use your own key for production.

## 🐛 Troubleshooting

### Browser doesn't launch
- Ensure Playwright is properly installed: `playwright install chromium`
- Check that you have sufficient permissions to launch browsers

### Screenshots not captured
- Verify the `screenshots/` directory exists
- Check file permissions in the directory

### MCP connection fails
- Ensure the server is running with `python server.py`
- Check that stdio transport is properly configured

## 📄 License

This project is part of the mcp_servers repository. Please refer to the main repository for licensing information.

## 🙏 Acknowledgments

- Built using [Model Context Protocol](https://modelcontextprotocol.io/)
- Browser automation powered by [Playwright](https://playwright.dev/)
- AI analysis powered by [Google Gemini](https://ai.google.dev/)
