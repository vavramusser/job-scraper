import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# generic function to scrape jobs from Lever Talent Acquisition Suite (ATS + CRM)
def apicall_lever(slug, company):

    print(f"\nScraping jobs from {company}")
    print(f"{'='*60}")

    api_url = f"https://jobs.lever.co/{slug}"

    jobs = []
    
    try:

        response = requests.get(api_url, timeout = 15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        job_list = soup.find_all('div', class_='posting')

        print(f"Found {len(job_list)} jobs\n")

        for job in job_list:

            # title
            title = job.find("h5").get_text(strip = True)

            # url
            url = job.find("a", class_ = "posting-title").get("href")

            # location
            location = job.find('span', class_='location').get_text(strip=True)

            # workplace (remote, hybrid, etc.)
            #workplace = job.find('span', class_='workplaceTypes').get_text(strip=True).replace('—', '').strip()
           
            # create job entry
            job = {
                'company': company,
                'title': title,
                'location': location,
                'url': url,
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }

            jobs.append(job)
        
            print(f"  - {title}")

        print(f"\nSuccessfully scraped {len(jobs)} jobs from {company}")
        print(f"{'='*60}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs from API: {e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return jobs

if __name__ == "__main__":

    apicall_lever(
        slug = "nimblerx",
        company = "Nimble Rx"
    )