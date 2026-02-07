from flipkart_browser import search_and_select_product, compare_products, filter_by_price
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('flipkart-shopping')


@mcp.tool()
async def flipkart_search(item: str, criterion: str = "best value"):
    """
    Search for a product on Flipkart and select the best option based on criterion.
    
    Args:
        item: The product name or description to search for on Flipkart (e.g., "laptop", "mobile phone", "headphones")
        criterion: The selection criteria - options include:
            - "lowest price" - Find the cheapest option
            - "highest rating" - Find the best rated product
            - "best value" - Balance between price and quality (default)
            - "premium" - Select high-end/premium options
            
    Returns:
        str: Name of the selected product
        
    Example:
        flipkart_search(item="wireless earbuds", criterion="best value")
    """
    result = await search_and_select_product(item, criterion)
    return f"Selected: {result}"


@mcp.tool()
async def flipkart_compare(item: str, num_products: int = 3):
    """
    Compare multiple products on Flipkart for the same search query.
    
    Args:
        item: The product to search and compare
        num_products: Number of products to compare (default: 3)
        
    Returns:
        str: Confirmation message that comparison screenshots have been captured
        
    Example:
        flipkart_compare(item="smartphone under 20000", num_products=5)
    """
    result = await compare_products(item, num_products)
    return result


@mcp.tool()
async def flipkart_price_filter(item: str, min_price: int, max_price: int):
    """
    Search for a product on Flipkart and apply price range filter.
    
    Args:
        item: The product to search for
        min_price: Minimum price in Indian Rupees (₹)
        max_price: Maximum price in Indian Rupees (₹)
        
    Returns:
        str: Confirmation of applied price filter
        
    Example:
        flipkart_price_filter(item="laptop", min_price=30000, max_price=50000)
    """
    result = await filter_by_price(item, min_price, max_price)
    return result


if __name__ == "__main__":
    mcp.run(transport='stdio')
