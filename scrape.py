import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def scrape_website(website_url : str):
    print("Launching chrome browser...")

    chromer_driver_path : str = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chromer_driver_path), options=options)

    try:
        driver.get(website_url)
        print("Page loaded...")
        html = driver.page_source

        return html
    finally:
        driver.quit()


def extract_body_content(html_content) -> str:
    soup = BeautifulSoup(html_content, "html.parser")

    # Get rid of everything but the body
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content) -> str:
    soup = BeautifulSoup(body_content, "html.parser")
    
    # Get rid of style and script tags of the html content
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    # Get rid of blank spaces and unnessesary new lines
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    # Split up the content in small parts, bc the LLM has a token limit of 8.000 charackters
    return[
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
