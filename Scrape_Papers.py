from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfReader
import requests
import os

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (Linux only)

# Initialize the WebDriver
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()


def filter(path):

    # List all files in the directory
    files = os.listdir(path)

    for file in files:

        # Check if the file is a PDF
        if not file.endswith('.pdf'):

            # Construct the full path to the file
            file_path = os.path.join(path, file)
            
            # Remove the file
            os.remove(file_path)
            print(f"Deleted {file_path} as it's not a PDF.")


def scrape_info(driver, query_text, paper_links):

    # Navigate to Google Scholar
    driver.get("https://scholar.google.com")

    # Perform a search
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query_text + " arxiv")
    search_box.submit()

    # Scrape results (get the links of the search results)
    links = driver.find_elements(By.XPATH, "//h3[@class='gs_rt']/a")
    for link in links:
        if 'arxiv.org' in link.get_attribute('href'):
            paper_links.append(link.get_attribute('href'))
            print(link.get_attribute('href'))

            # Extract PDF text
            pdf_link = link.get_attribute('href').replace('abs', 'pdf')
            pdf_response = requests.get(pdf_link)

            paper_title = link.text
            
            # Save the PDF with the paper title in the Downloads folder
            file_path = os.path.join('Downloads', paper_title + '.pdf')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(pdf_response.content)

    # Close the driver 
    driver.quit()

# Run the scraping function
paper_links = []
scrape_info(driver, "Recurrent Neural network", paper_links)
filter('Downloads')
