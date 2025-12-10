import requests
from datetime import datetime

# generic function to scrape jobs from Workday HCM
def apicall_workday(company_slug, page_slug, region, company):
    
    print(f"\nScraping jobs from {company}")
    print(f"{'='*60}")

    api_url = f"https://{company_slug}.{region}.myworkdayjobs.com/wday/cxs/{company_slug}/{page_slug}/jobs"
    base_job_url = f"https://{company_slug}.{region}.myworkdayjobs.com/{page_slug}"

    jobs = []
    offset = 0
    limit = 20
    total_jobs = None

    while True:

        payload = {
            "appliedFacets": {},
            "limit": limit,
            "offset": offset,
            "searchText": ""
        }

        try:

            response = requests.post(api_url, json = payload, timeout = 15)
            response.raise_for_status()
            data = response.json()

            if total_jobs is None:
                total_jobs = data.get('total', 0)
                print(f"Total jobs available: {total_jobs}\n")

            job_list = data.get('jobPostings', [])
            print(f"Found {len(job_list)} jobs\n")

            if not job_list:
                break

            for job_data in job_list:

                # title
                title = job_data.get('title', '')
                    
                # post date
                #job_data.get('postedOn', '')
                
                job = {
                    'company': company,
                    'title': title,
                    'location': job_data.get('locationsText', ''),
                    'date_open': job_data.get('postedOn', ''),
                    'date_found': datetime.now().strftime('%Y-%m-%d'),
                    'url': base_job_url + job_data.get('externalPath', '')
                }

                jobs.append(job)

                print(f"  - {title}")

            # check if we've got all jobs
            if len(jobs) >= total_jobs:
                break

            # move to next page
            offset += limit

        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs from API: {e}")
            break
    
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    
    print(f"\nSuccessfully scraped {len(jobs)} jobs from {company}")
    print(f"{'='*60}")

    return jobs


if __name__ == "__main__":

    apicall_workday(
        company_slug = "ijm",
        page_slug = "careers-ijm",
        region = "wd5",
        company = "International Justice Mission (IJM)")