# scraper for Research Triangle Institute (RTI)
# last updated 11/27/2025

import requests
from datetime import datetime
import time

def scrape_rti():
    """Scrape RTI International job listings"""
    
    base_url = "https://careers.rti.org/api/jobs"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }
    
    jobs = []
    page = 1
    
    try:
        while True:
            params = {
                'page': page,
                'sortBy': 'relevance',
                'descending': 'false',
                'internal': 'false'
            }
            
            print(f"Fetching RTI page {page}...")
            response = requests.get(base_url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            total_count = data.get('totalCount', 0)
            job_postings = data.get('jobs', [])
            
            if not job_postings:
                break
            
            for job in job_postings:
                job_data = job.get('data', {})
                
                title = job_data.get('title', 'No title')
                slug = job_data.get('slug', '')
                
                # Build job URL
                job_url = f"https://careers.rti.org/jobs/{slug}"
                
                # Get location
                location = job_data.get('location_name', 'Location not specified')
                
                # Get description
                description = job_data.get('description', '')
                
                jobs.append({
                    'company': 'RTI International',
                    'title': title,
                    'url': job_url,
                    'location': location,
                    'description': description,
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                })
            
            # Check if we've got all jobs
            if len(jobs) >= total_count:
                break
            
            page += 1
            time.sleep(0.5)  # Be nice to the server
        
        print(f"Successfully scraped {len(jobs)} jobs from RTI International")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping RTI: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error parsing RTI data: {e}")
    
    return jobs
