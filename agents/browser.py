"""
Browser Agent for IDA OS v3.0
Handles autonomous web browsing using Playwright.
"""
import asyncio
from playwright.async_api import async_playwright
from agents.base import BaseAgent
from logger import log_info, log_error

class BrowserAgent(BaseAgent):
    def __init__(self, brain):
        super().__init__("Browser", brain)

    async def run(self, task: str, context: str = ""):
        log_info(f"BrowserAgent: Starting task: {task}")
        
        # Decide the URL and action from the task
        # In a production OS, this would be more complex
        url = self._extract_url(task)
        if not url:
            return {"status": "error", "message": "No URL found in task"}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                log_info(f"BrowserAgent: Navigating to {url}")
                await page.goto(url, timeout=30000)
                
                # Get page title and text content
                title = await page.title()
                content = await page.evaluate("() => document.body.innerText")
                
                # Take a screenshot for the record (optional)
                # await page.screenshot(path=f"logs/browser_{int(asyncio.get_event_loop().time())}.png")
                
                await browser.close()
                
                # Truncate content for the LLM
                summary = content[:2000] + "..." if len(content) > 2000 else content
                
                return {
                    "status": "success",
                    "url": url,
                    "title": title,
                    "content": summary
                }
            except Exception as e:
                log_error(f"BrowserAgent failed on {url}", e)
                await browser.close()
                return {"status": "error", "message": str(e)}

    def _extract_url(self, task: str):
        import re
        urls = re.findall(r'(https?://[^\s]+)', task)
        if urls:
            return urls[0]
        
        # Fallback: if it's just a domain or search query
        if "google.com" in task.lower():
            return "https://www.google.com"
        
        # Default search if no URL
        query = task.replace(" ", "+")
        return f"https://www.google.com/search?q={query}"
