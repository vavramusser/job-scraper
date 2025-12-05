import requests
from bs4 import BeautifulSoup
from datetime import datetime

# generic function to scrape jobs from Greenhouse Boards
def scrape_greenhouse(slug, company):

    print(f"\nScraping jobs from {company}")
    print(f"{'='*60}")

    base_url = "https://job-boards.greenhouse.io/" + slug
    
    jobs = []
        
    try:

        response = requests.get(base_url, timeout = 15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        job_list = soup.find_all('tr', class_='job-post')
        
        print(f"Found {len(job_list)} jobs\n")

        for job_data in job_list:
            
            # title
            title = job_data.find('a').find('p', class_='body--medium').get_text(strip = True)

            # location
            location = job_data.find('a').find('p', class_='body--metadata').get_text(strip = True)

            # job URL
            url = job_data.find('a').get('href', '')

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

    # Greenpeace
    jobs_greenpeace = scrape_greenhouse(
        slug = "greenpeace",
        company = "Greenpeace"
    )