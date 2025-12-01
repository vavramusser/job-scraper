# scraper for Innocence Project
# last updated 11/28/2025

import requests
from datetime import datetime

def scrape_innocence():
    """Scrape Innocence Project job listings via Workable API"""
    
    url = "https://apply.workable.com/api/v1/widget/accounts/675118"
    
    params = {
        'origin': 'embed'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': '*/*',
    }
    
    jobs = []
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse JSON response directly
        data = response.json()
        
        job_postings = data.get('jobs', [])
        
        print(f"Found {len(job_postings)} Innocence Project job listings")
        
        for job in job_postings:
            title = job.get('title', 'No title')
            
            # Get job URL
            job_url = job.get('url', '')
            
            # Get location - build from city, state
            city = job.get('city', '')
            state = job.get('state', '')
            country = job.get('country', '')
            
            if city and state:
                location = f"{city}, {state}"
            elif state:
                location = state
            elif country:
                location = country
            else:
                location = 'Location not specified'
            
            # Workable doesn't provide descriptions in this API
            description = ''
            
            jobs.append({
                'company': 'Innocence Project',
                'title': title,
                'url': job_url,
                'location': location,
                'description': description,
                'date_found': datetime.now().strftime('%Y-%m-%d')
            })
        
        print(f"Successfully scraped {len(jobs)} jobs from Innocence Project")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Innocence Project: {e}")
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing Innocence Project data: {e}")
    
    return jobs