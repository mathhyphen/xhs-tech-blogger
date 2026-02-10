#!/usr/bin/env python3
"""
小红书推文截图工具
使用方法：
  python tweet_capture.py <推文URL>
"""

import sys
from playwright.sync_api import sync_playwright

def capture_tweet(url: str, output: str = None):
    if not output:
        output = "tweet_screenshot.png"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 无头模式
        page = browser.new_page(viewport={"width": 600, "height": 900})
        
        print(f"打开: {url}")
        page.goto(url, wait_until="networkidle")
        
        # 等待推文
        page.wait_for_selector("article[data-testid='tweet']", timeout=10000)
        
        # 截图推文元素
        tweet = page.locator("article[data-testid='tweet']").first
        tweet.screenshot(path=output)
        
        browser.close()
        print(f"✅ 已保存: {output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tweet_capture.py <tweet_url>")
        print("Example: python tweet_capture.py https://x.com/elonmusk/status/123456")
        sys.exit(1)
    
    capture_tweet(sys.argv[1])
