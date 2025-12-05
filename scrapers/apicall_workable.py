import requests
from datetime import datetime
import time

# generic function to scrape jobs from Workable
def apicall_workable(url_extension, company):

    params = {
        "origin": "embed"
    }

    print(f"\nScraping jobs from {company}")
    print(f"{'='*60}")

    api_url_base = "https://apply.workable.com/api/v1/widget/accounts/"
    api_url = api_url_base + url_extension

    jobs = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
               'Accept': 'application/json'
    }
    
    try:
        
        response = requests.get(api_url, params = params, headers = headers, timeout = 15)
        response.raise_for_status()
        data = response.json()
        job_list = data.get('jobs', [])

        print(f"Found {len(job_list)} jobs\n")

        for job_data in job_list:

            # job ID
            id = job_data.get("shortcode", "")
            
            # title
            title = job_data.get("title", "Not Specified")

            # location
            city = job_data.get("city", "")
            state = job_data.get("state", "")
            country = job_data.get("country_id", "")
            location_parts = [p for p in [city, state, country] if p]
            location = ', '.join(location_parts) if location_parts else 'Not specified'

            # salary range

            # open date
            date_open = datetime.strptime(job_data.get("published_on", ""), "%Y-%m-%d").date()
           
           # job URL
            url = job_data.get("url")

            # create job entry
            job = {
                "id": id,
                "company": company,
                "title": title,
                "location": location,
                "date_open": date_open,
                "date_found": datetime.now().strftime('%Y-%m-%d'),
                "url": url
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

    # Innocence Project
    urlextension_innocenceproject = "675118"
    jobs_earthdaily = apicall_workable(urlextension_innocenceproject, "Innnocence Project")