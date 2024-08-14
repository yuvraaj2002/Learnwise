from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (Linux only)


# Initialize the WebDriver
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

def scrape_info(driver, query_text,data):

    # Navigate to Google Scholar
    driver.get("https://scholar.google.com")

    # Perform a search
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query_text + " arxiv")
    search_box.submit()

    # Scrape results (get the links of the search results)
    links = driver.find_elements(By.XPATH, "//h3[@class='gs_rt']/a")
    for link in links:
        data[] = link.get_attribute('href')  

    # Close the driver
    driver.quit()

# Run the scraping function
data = dict()
scrape_info(driver, "Large Language Model",data)
