# scraper for Center for Naval Analysis (CNA)
# last updated 11/27/2025
# NOT FUNCTIONAL

import requests
from datetime import datetime

def scrape_cna():
    """Scrape CNA job listings via Dayforce API"""
    
    url = "https://jobs.dayforcehcm.com/api/geo/cna/jobposting/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Origin': 'https://jobs.dayforcehcm.com',
        'Referer': 'https://jobs.dayforcehcm.com/en-US/cna/CANDIDATEPORTAL',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }
    
    payload = {
        'clientNamespace': 'cna',
        'jobBoardCode': 'CANDIDATEPORTAL',
        'cultureCode': 'en-US',
        'distanceUnit': 0,
        'paginationStart': 0
    }
    
    jobs = []
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Job listings are in the 'jobPostings' array
        job_postings = data.get('jobPostings', [])
        
        for job in job_postings:
            job_id = job.get('jobPostingId')
            job_url = f"https://jobs.dayforcehcm.com/en-US/cna/CANDIDATEPORTAL/jobs/{job_id}"
            
            # Get location from postingLocations array
            locations = job.get('postingLocations', [])
            if locations:
                # Use the formatted address from first location
                location = locations[0].get('formattedAddress', 'Location not specified')
            else:
                location = 'Location not specified'
            
            jobs.append({
                'company': 'CNA',
                'title': job.get('jobTitle', 'No title'),
                'url': job_url,
                'location': location,
                'date_found': datetime.now().strftime('%Y-%m-%d')
            })
        
        print(f"Successfully scraped {len(jobs)} jobs from CNA")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping CNA: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error parsing CNA data: {e}")
    
    return jobs