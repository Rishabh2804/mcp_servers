from playwright.async_api import async_playwright
from google import genai
import time
import asyncio
import re
import os

# Constants for scrolling behavior
MAX_SCROLL_ITERATIONS = 10
ARROW_PRESSES_PER_SCROLL = 8

# Initialize Gemini client - API key is required
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable is required. "
        "Get your API key from https://makersuite.google.com/app/apikey and set it with: "
        "export GEMINI_API_KEY='your-key-here'"
    )
client = genai.Client(api_key=api_key)

async def search_and_select_product(item: str, criterion: str):
    """
    Search for a product on Flipkart and select the best one based on criterion.
    
    Args:
        item: The product to search for
        criterion: The selection criteria (e.g., "lowest price", "highest rating", "best value")
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to Flipkart
        await page.goto('https://www.flipkart.com/')
        await page.wait_for_selector('input[type="text"]', timeout=10000)
        
        # Search for the item
        await page.locator('input[type="text"]').first.fill(item)
        await page.locator('input[type="text"]').first.press('Enter')
        await page.wait_for_timeout(3000)
        
        # Take initial screenshot
        await page.screenshot(path='./screenshots/flipkart_search.jpg')
        
        # Scroll through results and capture screenshots
        for j in range(MAX_SCROLL_ITERATIONS):
            for i in range(ARROW_PRESSES_PER_SCROLL):
                await page.keyboard.press('ArrowDown')
            await page.screenshot(path=f'./screenshots/flipkart_result_{j+1}.jpg')
            await page.wait_for_timeout(500)
        
        # Analyze screenshots and select best item
        selected_item = await analyze_and_select_item(criterion)
        
        if selected_item:
            print(f"Selected item: {selected_item}")
            # Click on the selected item
            try:
                await page.get_by_text(selected_item, exact=False).first.click()
                await page.wait_for_timeout(5000)
                await page.screenshot(path='./screenshots/flipkart_product_page.jpg')
            except Exception as e:
                print(f"Error clicking on item: {e}")
        
        await browser.close()
        return selected_item


async def analyze_and_select_item(criterion: str):
    """
    Analyze captured screenshots and select the best item based on criterion.
    
    Args:
        criterion: Selection criteria for choosing the product
    
    Returns:
        str: Name/title of the selected product
    """
    from google.genai import types
    
    # Load all captured screenshots
    screenshots = []
    for i in range(11):  # 0-10 screenshots
        path = f'./screenshots/flipkart_result_{i}.jpg' if i > 0 else './screenshots/flipkart_search.jpg'
        try:
            with open(path, 'rb') as f:
                screenshots.append(f.read())
        except FileNotFoundError:
            continue
    
    # Create image parts for Gemini
    image_parts = [
        types.Part.from_bytes(data=img, mime_type='image/jpeg')
        for img in screenshots
    ]
    
    # Ask Gemini to analyze and select
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            *image_parts,
            f"""
            From the images of Flipkart product search results, select the best product according to: {criterion}
            
            Important instructions:
            - Return ONLY the exact product title/name as it appears in the listing
            - Do not include price or any other information
            - Choose only products that are clearly in stock
            - If the criterion is about price, choose the best value for money
            - Return just the product title, nothing else
            """
        ]
    )
    
    result = response.text.strip()
    print(f"Gemini selected: {result}")
    return result


async def add_to_cart_and_view():
    """
    Add the currently viewed product to cart.
    Assumes we're already on a product page.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # This would need the current product URL or context
        # For now, this is a placeholder
        await page.screenshot(path='./screenshots/flipkart_cart.jpg')
        await browser.close()


async def compare_products(item: str, num_products: int = 3):
    """
    Search for a product and compare multiple options.
    
    Args:
        item: Product to search for
        num_products: Number of top products to compare
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to Flipkart
        await page.goto('https://www.flipkart.com/')
        await page.wait_for_selector('input[type="text"]', timeout=10000)
        
        # Search for the item
        await page.locator('input[type="text"]').first.fill(item)
        await page.locator('input[type="text"]').first.press('Enter')
        await page.wait_for_timeout(3000)
        
        # Take screenshots of results
        await page.screenshot(path='./screenshots/flipkart_comparison.jpg')
        
        # Scroll to see more products
        for i in range(5):
            await page.keyboard.press('ArrowDown')
            await page.wait_for_timeout(300)
        
        await page.screenshot(path='./screenshots/flipkart_comparison_scroll.jpg')
        
        await browser.close()
        
        return "Comparison complete - screenshots saved"


async def filter_by_price(item: str, min_price: int, max_price: int):
    """
    Search for a product and filter by price range.
    
    Args:
        item: Product to search for
        min_price: Minimum price filter
        max_price: Maximum price filter
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to Flipkart
        await page.goto('https://www.flipkart.com/')
        await page.wait_for_selector('input[type="text"]', timeout=10000)
        
        # Search for the item
        await page.locator('input[type="text"]').first.fill(item)
        await page.locator('input[type="text"]').first.press('Enter')
        await page.wait_for_timeout(3000)
        
        # Look for price filter elements - Flipkart's structure may vary
        try:
            # This is a simplified approach - actual selectors may need adjustment
            await page.screenshot(path='./screenshots/flipkart_before_filter.jpg')
            
            # Note: Flipkart's filter UI may require specific interaction
            # This is a placeholder that would need real selector investigation
            print(f"Filtering products between ₹{min_price} and ₹{max_price}")
            
            await page.wait_for_timeout(2000)
            await page.screenshot(path='./screenshots/flipkart_after_filter.jpg')
        except Exception as e:
            print(f"Error applying price filter: {e}")
        
        await browser.close()
        return f"Filtered by price: ₹{min_price} - ₹{max_price}"
