# scraper for Public Health Institute (PHI)
# last updated 11/27/2025

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def scrape_phi():
    """Scrape PHI job listings"""
    url = "https://www.phi.org/employment/current-opportunities"
    jobs = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # Get main listing page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all job posting links
        job_links = soup.find_all('a', class_='-fw:5')
        
        print(f"Found {len(job_links)} PHI job listings, fetching details...")
        
        for link in job_links:
            try:
                title = link.text.strip()
                job_url = link['href']
                
                # Only process job posting URLs
                if '/employment/current-opportunities/' in job_url:
                    # Fetch individual job page
                    job_response = requests.get(job_url, headers=headers, timeout=10)
                    job_response.raise_for_status()
                    job_soup = BeautifulSoup(job_response.content, 'html.parser')
                    
                    # Extract location
                    location = 'Location not specified'
                    location_tag = job_soup.find('strong', class_='-t:6', string='Location:')
                    
                    if location_tag:
                        if location_tag.next_sibling:
                            location = location_tag.next_sibling.strip()
                    
                    # Extract full description (get all text from main content area)
                    # You may need to adjust this selector based on PHI's page structure
                    description = ''
                    content_area = job_soup.find('div', class_='post-content')
                    if content_area:
                        description = content_area.get_text(separator='\n', strip=True)
                    
                    jobs.append({
                        'company': 'PHI',
                        'title': title,
                        'url': job_url,
                        'location': location,
                        'description': description,
                        'date_found': datetime.now().strftime('%Y-%m-%d')
                    })
                    
                    print(f"  ✓ Fetched: {title}")
                    
                    # Be nice to the server - small delay between requests
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"Error fetching job details for {title}: {e}")
                continue
                
    except Exception as e:
        print(f"Error scraping PHI: {e}")
    
    return jobs