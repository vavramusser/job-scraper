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

    api_url = f"https://apply.workable.com/api/v3/accounts/{url_extension}/jobs"

    params = {}
    method = "POST"

    jobs = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
               'Accept': 'application/json'
    }
    
    try:
        
        response = requests.post(api_url, json = {}, headers = headers, timeout = 15)
        response.raise_for_status()
        data = response.json()
        job_list = data.get('results', [])
        print(f"Found {len(job_list)} jobs\n")

        for job_data in job_list:

            # job ID
            id = job_data.get("shortcode", "")
            
            # title
            title = job_data.get("title", "Not Specified")

            # location
            location_data = job_data.get("location", {})
            city = location_data.get("city", "")
            region = location_data.get("region", "")
            country = location_data.get("country", "")
            location_parts = [p for p in [city, region, country] if p]
            location = ', '.join(location_parts) if location_parts else 'Not specified'

            # salary range

            # open date
            published = job_data.get("published", "")
            if published:
                date_open = datetime.fromisoformat(published.replace('Z', '+00:00')).date()
            else:
                date_open = None
                        
           # job URL
            shortcode = job_data.get("shortcode", "")
            url = f"https://apply.workable.com/innocence-project/j/{shortcode}/" if shortcode else ""

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

    apicall_workable(
        url_extension = "blue-tiger",
        company = "Blue Tiger")

    apicall_workable(
        url_extension = "bme-strategies",
        company = "BME Strategies")
    
    apicall_workable(
        url_extension = "claritasrx",
        company = "Claritas Rx")
    
    apicall_workable(
        url_extension = "innocence-project",
        company = "Innocence Project")

    apicall_workable(
        url_extension = "murmuration",
        company = "Murmuration")