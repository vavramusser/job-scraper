# scraper for RAND Corporation
# last updated 11/27/2025
# NOT FUNCTIONAL

import requests
from datetime import datetime

def scrape_rand():
    """Scrape RAND Corporation job listings via Workday API"""
    
    url = "https://rand.wd5.myworkdayjobs.com/wday/cxs/rand/External_Career_Site/jobs"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://rand.wd5.myworkdayjobs.com',
        'Referer': 'https://rand.wd5.myworkdayjobs.com/External_Career_Site/',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }
    
    payload = {
        'appliedFacets': {},
        'limit': 100,  # Get more jobs at once
        'offset': 0,
        'searchText': ''
    }
    
    jobs = []
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        job_postings = data.get('jobPostings', [])
        total = data.get('total', 0)
        
        print(f"Found {total} RAND job listings")
        
        for job in job_postings:
            title = job.get('title', 'No title')
            
            # Build full URL
            external_path = job.get('externalPath', '')
            job_url = f"https://rand.wd5.myworkdayjobs.com/en-US/External_Career_Site{external_path}"
            
            # Get location
            location = job.get('locationsText', 'Location not specified')
            
            # Workday doesn't include descriptions in the listing API
            # We'd need to fetch individual pages for that
            description = ''
            
            jobs.append({
                'company': 'RAND Corporation',
                'title': title,
                'url': job_url,
                'location': location,
                'description': description,
                'date_found': datetime.now().strftime('%Y-%m-%d')
            })
        
        print(f"Successfully scraped {len(jobs)} jobs from RAND")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping RAND: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error parsing RAND data: {e}")
    
    return jobs