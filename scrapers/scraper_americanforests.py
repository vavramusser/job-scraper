# scraper for American Forests
# last updated 11/30/2025

import requests
from datetime import datetime
import time

def scrape_americanforests():
    """Scrape jobs from American Forests via their API endpoint"""
    api_url = "https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions"
    
    params = {
        'cid': 'f4cdd59b-bdcf-4e58-9e68-112518aa9a0a',
        'ccId': '19000101_000003',
        'lang': 'en_US',
        'locale': 'en_US',
        '$top': '100',  # Increased to get more jobs
        'isWidget': 'true'
    }
    
    jobs = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # The jobs should be in the 'jobRequisitions' key
        job_list = data.get('jobRequisitions', [])
        
        print(f"Found {len(job_list)} total jobs in API response")
        
        for job_data in job_list:
            try:
                # Extract job details from the API response
                title = job_data.get('requisitionTitle', 'Unknown Title')
                
                # Location might be in different fields
                location_list = job_data.get('requisitionLocations', [])
                if location_list:
                    # Build location string from first location
                    loc = location_list[0]
                    city = loc.get('cityName', '')
                    state = loc.get('stateProvCode', '')
                    country = loc.get('countryCode', '')
                    location_parts = [p for p in [city, state, country] if p]
                    location = ', '.join(location_parts) if location_parts else 'Location not specified'
                else:
                    location = 'Location not specified'
                
                # Get job type if available
                job_type = job_data.get('requisitionJobType', '')
                if job_type:
                    location = f"{job_type} | {location}"
                
                # Construct job URL - might need to build from requisition ID
                req_id = job_data.get('requisitionId', '')
                if req_id:
                    job_url = f"https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=f4cdd59b-bdcf-4e58-9e68-112518aa9a0a&ccId=19000101_000003&jobId={req_id}"
                else:
                    job_url = "https://www.americanforests.org/job-opportunities"
                
                job = {
                    'company': 'American Forests',
                    'title': title,
                    'location': location,
                    'url': job_url,
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                }
                
                jobs.append(job)
                print(f"Scraped: {title} - {location}")
                
            except Exception as e:
                print(f"Error parsing job data: {e}")
                continue
        
    except requests.RequestException as e:
        print(f"Error fetching American Forests jobs from API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return jobs

if __name__ == "__main__":
    jobs = scrape_americanforests()
    print(f"\nTotal jobs scraped: {len(jobs)}")
    for job in jobs:
        print(f"\n{job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")


if __name__ == "__main__":
    jobs = scrape_americanforests()
    print(f"\nTotal jobs scraped: {len(jobs)}")
    for job in jobs:
        print(f"\n{job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")


if __name__ == "__main__":
    jobs = scrape_americanforests()
    print(f"\nTotal jobs scraped: {len(jobs)}")
    for job in jobs:
        print(f"\n{job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")