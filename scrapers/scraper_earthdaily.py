# scraper for Earth Daily
# last updated 12/1/2025

import requests
from datetime import datetime

def scrape_earthdaily():
    """Scrape job listings from Earth Daily using their API"""
    api_url = "https://api.resumatorapi.com/v1/jobs/status/open?apikey=mJbxSpDuFZEZ2pqWz8SssgHOfFd3iMYX"
    jobs = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"API returned {len(data)} jobs")
        
        for job_data in data:
            try:
                # Extract job information from API response
                title = job_data.get('title', 'Not specified')
                job_id = job_data.get('id', '')
                
                # Build the job URL
                # Format appears to be: https://earthdaily.applytojob.com/apply/{job_id}/{title-slug}
                board_code = job_data.get('board_code', '')
                if board_code:
                    job_url = f"https://earthdaily.applytojob.com/apply/{board_code}"
                else:
                    job_url = f"https://earthdaily.applytojob.com/apply/{job_id}"
                
                # Get location
                city = job_data.get('city', '')
                state = job_data.get('state', '')
                country = job_data.get('country', '')
                
                # Build location string
                location_parts = [p for p in [city, state, country] if p]
                location = ', '.join(location_parts) if location_parts else 'Not specified'
                
                # Get department/category
                categories = job_data.get('categories', {})
                department = categories.get('Department', 'Not specified') if categories else 'Not specified'
                
                # Get description if available
                description = job_data.get('description', '')
                if not description and department != 'Not specified':
                    description = f"Department: {department}"
                
                # Create job entry
                job = {
                    'company': 'Earth Daily Analytics',
                    'title': title,
                    'location': location,
                    'url': job_url,
                    'description': description[:500] if description else f"Department: {department}",  # Limit description length
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                }
                
                jobs.append(job)
                print(f"Found job: {title} - {location}")
                
            except Exception as e:
                print(f"Error parsing job entry: {e}")
                continue
        
        print(f"\nSuccessfully scraped {len(jobs)} jobs from Earth Daily")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Earth Daily jobs from API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return jobs

# Test the scraper
if __name__ == "__main__":
    print("Testing Earth Daily scraper...")
    jobs = scrape_earthdaily()
    
    print("\n" + "="*60)
    print(f"TOTAL JOBS FOUND: {len(jobs)}")
    print("="*60)
    
    for job in jobs:
        print(f"\nCompany: {job['company']}")
        print(f"Title: {job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")
        print(f"Description: {job['description'][:100]}..." if len(job['description']) > 100 else f"Description: {job['description']}")
        print(f"Date Found: {job['date_found']}")
        print("-"*60)