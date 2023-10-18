

import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = 'https://www.massgeneral.org/doctors?Text=*&Start={start}&MaxResults={max_results}&Sort[]=lastname&MethodName=getlisting&PageNumber={page_number}'
page_number = 1
start = 1
max_results = page_number * 10

# List to store the extracted data
data = []

while True:
    url = BASE_URL.format(start=start, max_results=max_results, page_number=page_number)
    print(f"Scraping page {page_number}: {url}")

    # Make a request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all the divs containing doctor's information
    doctor_divs = soup.find_all('div', class_='listing-item listing-item--profile')

    if not doctor_divs:
        print("No more doctors found. Exiting loop.")
        break

    for div in doctor_divs:
        # Extract doctor's name
        name = div.find('h4', class_='listing-item__title').a.text.strip()

        # Extract doctor's specialty
        specialty_tags = div.find('div', class_='listing-item__meta').find_all('p')
        specialty = specialty_tags[0].text.strip() if specialty_tags else ""

        # Extract doctor's department (Location)
        department = ""
        if len(specialty_tags) > 1:
            department = specialty_tags[1].text.strip().replace('Location:', '').strip()

        data.append([name, specialty, department])
        print(f"Saved data for doctor: {name}")

    # Increment for the next page
    page_number += 1
    start = max_results + 1
    max_results = page_number * 10

# Save the data to a CSV file
with open('doctors.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Specialty', 'Department'])  # CSV header
    writer.writerows(data)

print("Data saved to doctors.csv")


