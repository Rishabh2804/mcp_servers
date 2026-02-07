# Flipkart MCP Server - Quick Start Guide

This guide will help you get started with the Flipkart MCP Server in just a few minutes.

## What is This?

The Flipkart MCP Server is a **Model Context Protocol** server that enables AI agents to shop on Flipkart autonomously. It provides:

- 🔍 Smart product search with AI-powered selection
- 💰 Price filtering capabilities
- 📊 Product comparison features
- 🤖 Natural language interface

## Prerequisites

- Python 3.8+
- A Gemini API key ([Get one free](https://makersuite.google.com/app/apikey))

## Installation (2 minutes)

```bash
# 1. Navigate to the directory
cd flipkart_mcp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install browser
playwright install chromium

# 4. Set your API key
export GEMINI_API_KEY="your-api-key-here"
```

## Quick Test (30 seconds)

Test that everything is working:

```bash
python test_server.py
```

You should see: ✅ All tests passed!

## Usage Options

### Option 1: Interactive Client (Recommended for beginners)

```bash
python client.py
```

Then type queries like:
- "Search for wireless earbuds with best value"
- "Find the cheapest laptop"

### Option 2: Example Agent (Learn by example)

```bash
# See demonstrations
python example_agent.py

# Try interactive mode
python example_agent.py --interactive
```

### Option 3: Integrate with Your Agent

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Connect to server
server_params = StdioServerParameters(
    command='python',
    args=['server.py']
)

# Use in your agent code...
```

See `example_agent.py` for a complete integration example.

## Available Tools

The server provides three MCP tools:

1. **flipkart_search** - Search and select products
   - Parameters: `item` (string), `criterion` (string)
   - Criteria: "lowest price", "highest rating", "best value", "premium"

2. **flipkart_compare** - Compare multiple products
   - Parameters: `item` (string), `num_products` (int)

3. **flipkart_price_filter** - Filter by price range
   - Parameters: `item` (string), `min_price` (int), `max_price` (int)

## How It Works

```
┌──────────────┐
│  Your Query  │  "Find wireless earbuds"
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  MCP Server  │  Selects the right tool
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Browser    │  Automates Flipkart
│  Automation  │  Takes screenshots
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Gemini AI   │  Analyzes products
│   Analysis   │  Selects best match
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Result    │  Returns selection
└──────────────┘
```

## Common Use Cases

### Budget Shopping
```
Query: "Find the cheapest smartphone"
Tool: flipkart_search(item="smartphone", criterion="lowest price")
```

### Quality Focus
```
Query: "Find the best rated headphones"
Tool: flipkart_search(item="headphones", criterion="highest rating")
```

### Balanced Choice
```
Query: "Search for laptop with best value"
Tool: flipkart_search(item="laptop", criterion="best value")
```

### Price Range
```
Query: "Filter laptops between 30000 and 50000"
Tool: flipkart_price_filter(item="laptop", min_price=30000, max_price=50000)
```

### Comparison Shopping
```
Query: "Compare smartphones under 20000"
Tool: flipkart_compare(item="smartphone under 20000", num_products=5)
```

## Troubleshooting

### "GEMINI_API_KEY environment variable is required"
**Solution:** Set your API key:
```bash
export GEMINI_API_KEY="your-key-here"
```

### "Browser doesn't launch"
**Solution:** Install Playwright browsers:
```bash
playwright install chromium
```

### "Connection failed"
**Solution:** Make sure the server is running:
```bash
python server.py
```

## Next Steps

1. ✅ Complete the Quick Test above
2. 📖 Read the full [README.md](README.md) for detailed documentation
3. 💡 Check [USAGE.md](USAGE.md) for more examples
4. 🤖 Study [example_agent.py](example_agent.py) to learn integration
5. 🔧 Customize `flipkart_browser.py` for your specific needs

## Support

- Check the [main README](README.md) for detailed documentation
- Review [USAGE.md](USAGE.md) for practical examples
- See [example_agent.py](example_agent.py) for integration patterns

## Important Notes

⚠️ **Browser Mode**: The browser runs in visible mode (not headless) so you can see what's happening

⚠️ **Rate Limits**: Be mindful of Flipkart's rate limits - avoid excessive rapid requests

⚠️ **Screenshots**: Review screenshots in the `screenshots/` directory to verify selections

⚠️ **API Key**: Keep your Gemini API key secure - never commit it to version control

## License

Part of the mcp_servers repository. See main repository for license details.

---

**Ready to start?** Run `python client.py` and try your first query! 🚀
