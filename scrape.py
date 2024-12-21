from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
SBR_WEBDRIVER = 'https://brd-customer-hl_e1ad4dbb-zone-ai_scrapper:qz9pm525pook@brd.superproxy.io:9515'


def scrape_website(website):
    print("Launching Chrome browser...")
    
    options = ChromeOptions()
    try:
        with Remote(command_executor=SBR_WEBDRIVER, options=options) as driver:
            driver.get(website)
            
            # CAPTCHA handling (if supported by your proxy)
            print('Waiting for CAPTCHA to solve...')
            # Adjust this section based on your proxy's CAPTCHA API
            # Ensure you implement a valid method for CAPTCHA solving
            
            print('Navigated! Scraping page content...')
            html = driver.page_source
            return html
    except Exception as e:
        print(f"Error during scraping: {e}")
        return None

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]





    