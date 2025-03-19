import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sqlite3

def scrape_linkedin_jobs(pages=5):
    jobs_data = []
    
    base_url = "https://www.linkedin.com/jobs/search/?keywords=ai%20ml%20data%20science%20india&start="

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    for page in range(pages):
        url = base_url + str(page * 25)  # LinkedIn paginates results in multiples of 25
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page + 1}. Status code: {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_listings = soup.find_all('div', class_='base-search-card')  # Adjust if necessary

        for job in job_listings:
            title_element = job.find('h3', class_='base-search-card__title')
            company_element = job.find('h4', class_='base-search-card__subtitle')
            location_element = job.find('span', class_='job-search-card__location')
            link_element = job.find('a', class_='base-card__full-link')

            jobs_data.append({
                'Title': title_element.text.strip() if title_element else "N/A",
                'Company': company_element.text.strip() if company_element else "N/A",
                'Location': location_element.text.strip() if location_element else "N/A",
                'Link': link_element['href'] if link_element else "N/A"
            })

        time.sleep(2)  # Avoid rate limiting

    return jobs_data

# Run the scraper
jobs = scrape_linkedin_jobs()
df = pd.DataFrame(jobs)

# Save to CSV
df.to_csv('linkedin_aiml_data_science_jobs.csv', index=False)

# Save to SQLite
conn = sqlite3.connect('linkedin_jobs.db')
df.to_sql('aiml_data_science_jobs', conn, if_exists='replace', index=False)
conn.close()

print("Scraping completed and data saved successfully.")
