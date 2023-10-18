
from selenium.webdriver.chrome.service import Service


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

url = "https://www.mayoclinic.org/appointments/find-a-doctor/search-results?searchterm=#edd114075cc94f35b9bccc081668c123"
csv_file = "scraped_data.csv"

service = Service(executable_path='C:/Users/FuZ/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

all_data = []

wait = WebDriverWait(driver, 10)
page_count = 1  # To keep track of the current page number

while True:
    print(f"Scraping page {page_count}...")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    current_page_data = []  # To store data scraped from the current page
    for item in soup.select('ol.result-items li'):
        name_element = item.select_one('h4 a')
        name = name_element.text if name_element else 'N/A'
        
        specialties = ', '.join([spec.text for spec in item.select('ol.speciality li')])
        locations = ', '.join([loc.text for loc in item.select('ol.location li')])
        
        areas_of_focus = None
        focus_element = item.select_one('.areas-of-focus .ellipsis-container p')
        if focus_element:
            areas_of_focus = focus_element.text
        
        data = {
            'Name': name,
            'Specialities': specialties,
            'Locations': locations,
            'Areas of Focus': areas_of_focus
        }
        
        current_page_data.append(data)
    
    all_data.extend(current_page_data)
    
    # Writing the current page data to CSV
    df = pd.DataFrame(current_page_data)
    if page_count == 1:
        df.to_csv(csv_file, mode='a', index=False)  # Create file for first page
    else:
        df.to_csv(csv_file, mode='a', index=False, header=False)  # Append to existing file without header for subsequent pages

    print(f"Written {len(current_page_data)} records from page {page_count} to {csv_file}.")
    
    # Check for the existence of the next page button.
    next_page_button = driver.find_elements(By.CSS_SELECTOR, '#pagination-next')
    
    if not next_page_button:
        print("No more pages to scrape. Exiting...")
        break
    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pagination-next'))).click()
    print("Moving to the next page...")
    
    time.sleep(2)  # Give the page a couple of seconds to load.
    page_count += 1

driver.quit()

print(f"Total records written to {csv_file}: {len(all_data)}")
