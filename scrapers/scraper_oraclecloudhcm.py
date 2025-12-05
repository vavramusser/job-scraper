import requests
from datetime import datetime
import time

# generic function to scrape jobs from Oracle Cloud HCM (Human Capital Management) Boards
def scrape_oracle(tenant_id, region, site_number, company):
        
    params = {
        'onlyData': 'true',
        'expand': 'requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations',
        'finder': f'findReqs;siteNumber={site_number},facetsList=LOCATIONS;WORK_LOCATIONS;TITLES;CATEGORIES;POSTING_DATES,limit=100,sortBy=POSTING_DATES_DESC'
    }

    print(f"\nScraping jobs from {company}")
    print(f"{'='*60}")

    base_url = f"https://{tenant_id}.fa.{region}.oraclecloud.com"
    api_url = f"{base_url}/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
    
    jobs = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
        
    try:

        response = requests.get(api_url, params = params, headers = headers, timeout = 15)
        response.raise_for_status()
        data = response.json()
        job_list = data['items'][0].get('requisitionList', [])
        
        print(f"Found {len(job_list)} jobs\n")

        for job_data in job_list:

            # job ID
            id = job_data.get("Id", "")
            
            # title
            title = job_data.get("Title", "Not Specified")

            # location
            location = job_data.get("PrimaryLocation", "")

            # open and close date
            date_open_raw = job_data.get("PostedDate")
            date_open = datetime.strptime(date_open_raw, "%Y-%m-%d").date() if date_open_raw else None
            date_close_raw = job_data.get("PostingEndDate")
            date_close = datetime.strptime(date_close_raw, "%Y-%m-%d").date() if date_close_raw else None

            # job URL
            url = f"{base_url}/hcmUI/CandidateExperience/en/sites/{site_number.replace('CX_', '')}/job/{id}"

            # create job entry
            job = {
                "id": id,
                "company": company,
                "title": title,
                "location": location,
                #"salary_range": salary_range,
                "date_open": date_open,
                "date_close": date_close,
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

    # Abt Global
    jobs_abt = scrape_oracle(
        tenant_id = "egpy",
        region = "us2",
        site_number = "CX_3001",
        company = "Abt Global"
    )

    # DC Water
    jobs_dcwater = scrape_oracle(
        tenant_id = "elxb",
        region = "us2",
        site_number = "CX_3001",
        company = "DC Water"
    )