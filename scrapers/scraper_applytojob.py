import requests
from bs4 import BeautifulSoup
from datetime import datetime

# generic function to scrape jobs from Apply to Job Boards
def scrape_applytojob(slug, company):

    print(f"\nScraping jobs from {company}")
    print(f"{'='*60}")

    base_url = "https://" + slug + ".applytojob.com"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    jobs = []
        
    try:

        response = requests.get(base_url, headers = headers, timeout = 15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        job_list = soup.find_all('li', class_='list-group-item')
        
        print(f"Found {len(job_list)} jobs\n")

        for job_data in job_list:
            
            # title
            title = job_data.find('a').get_text(strip = True)

            # location
            location = job_data.find('i', class_='fa-map-marker').parent.get_text(strip = True)

            # job URL
            url = job_data.find("a").get("href", "")

            # create job entry
            job = {
                #"id": id,
                "company": company,
                "title": title,
                "location": location,
                #"salary_range": salary_range,
                #"date_open": date_open,
                #"date_close": date_close,
                "date_found": datetime.now().strftime('%Y-%m-%d'),
                "url": url
            }

            jobs.append(job)
        
            print(f"  - {title}")

        print(f"\nSuccessfully scraped {len(jobs)} jobs from {company}")
        print(f"{'='*60}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs from HTML: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return jobs

if __name__ == "__main__":

    # GeoOwl
    jobs_geoowl = scrape_applytojob(
        slug = "geoowl",
        company = "GeoOwl")