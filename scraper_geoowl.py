import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_geoowl():
    """Scrape GeoOwl job listings from HTML"""
    
    url = "https://geoowl.applytojob.com"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    jobs = []
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all job list items
        job_items = soup.find_all('li', class_='list-group-item')
        
        print(f"Found {len(job_items)} GeoOwl job listings")
        
        for item in job_items:
            # Get title and URL
            link = item.find('a')
            if not link:
                continue
                
            title = link.get_text(strip=True)
            job_url = link.get('href', '')
            
            # Get location - find the li with fa-map-marker icon
            location = 'Location not specified'
            location_item = item.find('i', class_='fa-map-marker')
            if location_item and location_item.parent:
                location = location_item.parent.get_text(strip=True)
            
            # No description available on listing page
            description = ''
            
            jobs.append({
                'company': 'GeoOwl',
                'title': title,
                'url': job_url,
                'location': location,
                'description': description,
                'date_found': datetime.now().strftime('%Y-%m-%d')
            })
        
        print(f"Successfully scraped {len(jobs)} jobs from GeoOwl")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping GeoOwl: {e}")
    except Exception as e:
        print(f"Error parsing GeoOwl data: {e}")
    
    return jobs