import requests
from datetime import datetime
import time

# generic function to scrape jobs from Resumator API
def apicall_resumator(apikey, company):

    params = {
        "apikey": apikey
    }

    print(f"\nScraping jobs from {company}")
    print(f"{'='*60}")

    api_url = "https://api.resumatorapi.com/v1/jobs/status/open?"

    jobs = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
               'Accept': 'application/json'
    }
    
    try:
        
        response = requests.get(api_url, params = params, headers = headers, timeout = 15)
        response.raise_for_status()
        data = response.json()

        print(f"Found {len(data)} jobs\n")

        for job_data in data:

            # job ID
            id = job_data.get("id", "")
            
            # title
            title = job_data.get("title", "Not Specified")

            # location
            city = job_data.get("city", "")
            state = job_data.get("state", "")
            country = job_data.get("country_id", "")
            location_parts = [p for p in [city, state, country] if p]
            location = ', '.join(location_parts) if location_parts else 'Not specified'

            # salary range
            salary_min = int(job_data.get("minimum_salary", ""))
            salary_max = int(job_data.get("maximum_salary", ""))
            salary_range = (
                f"${salary_min:,} - ${salary_max:,}" if salary_min > 0 and salary_max > 0
                else "Not specified"
            )

            # open date
            date_open = datetime.strptime(job_data.get("original_open_date", ""), "%Y-%m-%d").date()

            # job URL
            board_code = job_data.get("board_code", "")
            if board_code:
                url = f"https://earthdaily.applytojob.com/apply/{board_code}"
            else:
                url = f"https://earthdaily.applytojob.com/apply/{id}"

            # create job entry
            job = {
                "id": id,
                "company": company,
                "title": title,
                "location": location,
                "salary_range": salary_range,
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

    # Earth Daily
    apikey_earthdaily = "mJbxSpDuFZEZ2pqWz8SssgHOfFd3iMYX"
    jobs_earthdaily = apicall_resumator(apikey_earthdaily, "Earth Daily")