import requests
from datetime import datetime
import time

# generic function to scrape jobs from ADP Workforce Now
def apicall_adpworkforcenow(cid, ccId, company):

    params = {
    'cid': cid,          # unique identifier for company within ADP Workforce system
    'ccId': ccId,         # specific career cernter / job board identifier within ADP
    'lang': 'en_US',     # language for job listings
    'locale': 'en_US',   # regional settings for formatting
    '$top': '100',       # maximum number of jobs to return
    'isWidget': 'true'   # tells API that this is an embedded widget request
    }

    print(f"\nScraping jobs from {company}")
    print(f"{'='*60}")

    api_url = "https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions"

    jobs = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
               'Accept': 'application/json'
    }
    
    try:
        
        response = requests.get(api_url, params = params, headers = headers, timeout = 15)
        response.raise_for_status()
        data = response.json()
        job_list = data.get('jobRequisitions', [])

        print(f"Found {len(job_list)} jobs\n")

        for job_data in job_list:

            # job ID
            id = job_data.get("itemID", "")
            
            # title
            title = job_data.get("requisitionTitle", "Not Specified")

            # location
            location_list = job_data.get('requisitionLocations', [])
            location_data = location_list[0]
            city = location_data.get("cityName", "")
            state = location_data.get('stateProvCode', '')
            country = location_data.get('countryCode', '')
            location_parts = [p for p in [city, state, country] if p]
            location_shortname = location_data.get("nameCode").get("shortName")
            location = ', '.join(location_parts) if location_parts else (location_shortname if location_shortname else 'Not specified')

            # salary range
            salary_min = int(job_data.get("payGradeRange").get("minimumRate").get("amountValue"))
            salary_max = int(job_data.get("payGradeRange").get("maximumRate").get("amountValue"))
            salary_range = (
                f"${salary_min:,} - ${salary_max:,}" if salary_min > 0 and salary_max > 0
                else "Not specified"
            )
            
            # open date
            date_open = date_open = datetime.strptime(job_data.get("postDate", ""), "%Y-%m-%dT%H:%M:%S.%f%z").date()

            # job URL
            jobId = job_data.get("customFieldGroup").get("stringFields")[0].get("stringValue")
            if jobId:
                url = f"https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid={cid}&ccId={ccId}&jobId={jobId}"
            else:
                url = "https://www.americanforests.org/job-opportunities"

            # create job entry
            job = {
                "id": id,
                "company": company,
                "title": title,
                "location": location,
                "salary_range": salary_range,
                "date_open": date_open,
                "date_close": "Unspecified",
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

    # American Forests
    cid_americanforests = "f4cdd59b-bdcf-4e58-9e68-112518aa9a0a"
    ccId_americanforests = "19000101_000003"  
    jobs_americanforests = apicall_adpworkforcenow(cid_americanforests, ccId_americanforests, "American Forests")