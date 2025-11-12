#!/usr/bin/env python3
"""
FIX: Add this to web_scraper_pro.py to fix ChromeDriver issues on Windows
"""

# At the top, add these imports:
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Replace the setup_driver() method with this:

def setup_driver(self) -> webdriver.Chrome:
    """Setup Chrome driver with optimized options - WINDOWS FIX"""
    try:
        chrome_options = Options()

        # Headless mode
        chrome_options.add_argument("--headless=new")  # New headless mode

        # Core stability options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        # Windows-specific fixes
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Memory optimization
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-notifications")

        # User agent
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        # Additional Windows fixes
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Use webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.set_page_load_timeout(self.config.timeout)

        self.logger.info("✓ Chrome driver initialized successfully (Windows)")
        return driver

    except Exception as e:
        self.logger.error(f"Failed to initialize Chrome driver: {e}")
        self.logger.error(
            "\nTroubleshooting steps:\n"
            "  1. Install webdriver-manager: pip install webdriver-manager\n"
            "  2. Update Chrome: Download from https://www.google.com/chrome/\n"
            "  3. Try without headless: Comment out --headless argument\n"
            "  4. Run as Administrator\n"
        )
        sys.exit(1)
