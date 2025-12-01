# scraper for Center for Justice Innovation (CJI)
# last updated 12/1/2025

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_cji():
    """Scrape job listings from Center for Justice Innovation"""
    url = "https://innovatingjustice.applytojob.com/apply"
    jobs = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all job list items
        job_items = soup.find_all('li', class_='list-group-item')
        
        print(f"Found {len(job_items)} job listings")
        
        for item in job_items:
            try:
                # Get the job title and link
                heading = item.find('h4', class_='list-group-item-heading')
                if not heading:
                    continue
                
                link = heading.find('a')
                if not link:
                    continue
                
                title = link.get_text(strip=True)
                job_url = link.get('href', '')
                
                # Get location and department from the list-inline
                location = "Not specified"
                department = "Not specified"
                
                list_inline = item.find('ul', class_='list-inline')
                if list_inline:
                    list_items = list_inline.find_all('li')
                    
                    for li in list_items:
                        # Location has fa-map-marker icon
                        if li.find('i', class_='fa-map-marker'):
                            location = li.get_text(strip=True)
                        # Department has fa-sitemap icon
                        elif li.find('i', class_='fa-sitemap'):
                            department = li.get_text(strip=True)
                
                # Create job entry
                job = {
                    'company': 'Center for Justice Innovation',
                    'title': title,
                    'location': location,
                    'url': job_url,
                    'description': f"Department: {department}",
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                }
                
                jobs.append(job)
                
            except Exception as e:
                print(f"Error parsing job entry: {e}")
                continue
        
        print(f"Successfully scraped {len(jobs)} jobs from Center for Justice Innovation")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return jobs

# Test the scraper
if __name__ == "__main__":
    print("Testing Center for Justice Innovation scraper...")
    jobs = scrape_cji()
    
    print("\n" + "="*60)
    print(f"TOTAL JOBS FOUND: {len(jobs)}")
    print("="*60)
    
    for job in jobs[:5]:  # Show first 5 jobs
        print(f"\nCompany: {job['company']}")
        print(f"Title: {job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")
        print(f"Description: {job['description']}")
        print(f"Date Found: {job['date_found']}")
        print("-"*60)
    
    if len(jobs) > 5:
        print(f"\n... and {len(jobs) - 5} more jobs")