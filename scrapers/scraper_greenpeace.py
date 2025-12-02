# scraper for Greenpeace
# last updated 12/2/2025

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_greenpeace():
    """Scrape jobs from Greenpeace Greenhouse job board"""
    url = "https://job-boards.greenhouse.io/greenpeace"
    jobs = []
    
    try:
        print(f"Fetching jobs from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all job posting rows
        job_rows = soup.find_all('tr', class_='job-post')
        
        print(f"Found {len(job_rows)} job posting(s)")
        
        for row in job_rows:
            try:
                # Find the link within the row
                link = row.find('a')
                if not link:
                    continue
                
                # Extract job URL
                job_url = link.get('href', '')
                if job_url and not job_url.startswith('http'):
                    job_url = 'https://job-boards.greenhouse.io' + job_url
                
                # Extract job title (from the first <p> with class "body body--medium")
                title_elem = link.find('p', class_='body--medium')
                title = title_elem.get_text(strip=True) if title_elem else 'N/A'
                
                # Extract location (from the <p> with class "body__secondary body--metadata")
                location_elem = link.find('p', class_='body--metadata')
                location = location_elem.get_text(strip=True) if location_elem else 'N/A'
                
                # Create job dictionary
                job = {
                    'company': 'Greenpeace',
                    'title': title,
                    'location': location,
                    'url': job_url,
                    'description': '',  # Can be scraped from individual job pages if needed
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                }
                
                jobs.append(job)
                print(f"  - {title} ({location})")
                
            except Exception as e:
                print(f"Error parsing job row: {e}")
                continue
        
        print(f"Successfully scraped {len(jobs)} Greenpeace job(s)")
        
    except requests.RequestException as e:
        print(f"Error fetching Greenpeace jobs: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return jobs

# Test the scraper
if __name__ == "__main__":
    jobs = scrape_greenpeace()
    
    print("\n" + "="*60)
    print(f"GREENPEACE JOBS FOUND: {len(jobs)}")
    print("="*60 + "\n")
    
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")
        print(f"Date Found: {job['date_found']}")
        print("-"*60)