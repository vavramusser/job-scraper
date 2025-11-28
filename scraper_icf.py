# scraper for ICF International
# last updated 11/28/2025
# NOT FUNCTIONAL

import requests
from datetime import datetime
import time

def scrape_icf():
    """Scrape ICF International job listings"""
    
    base_url = "https://careers.icf.com/us/en/search-results"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }
    
    jobs = []
    page = 1
    
    try:
        while True:
            params = {
                's': page
            }
            
            print(f"Fetching ICF page {page}...")
            response = requests.get(base_url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Jobs are nested in data.jobs
            job_postings = data.get('data', {}).get('jobs', [])
            
            if not job_postings:
                break
            
            for job in job_postings:
                title = job.get('title', 'No title')
                req_id = job.get('reqId', '')
                
                # Use the applyUrl if available, otherwise construct from reqId
                job_url = job.get('applyUrl', f"https://careers.icf.com/us/en/job/{req_id}")
                
                # Get location
                location = job.get('location', 'Location not specified')
                
                # Get description teaser (short description)
                description = job.get('descriptionTeaser', '')
                
                jobs.append({
                    'company': 'ICF International',
                    'title': title,
                    'url': job_url,
                    'location': location,
                    'description': description,
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                })
            
            # ICF seems to paginate - check if we should continue
            # If we get fewer results than expected, we're probably done
            if len(job_postings) < 10:  # Assuming 10 per page
                break
            
            page += 1
            time.sleep(0.5)  # Be nice to the server
        
        print(f"Successfully scraped {len(jobs)} jobs from ICF International")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping ICF: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error parsing ICF data: {e}")
    
    return jobs