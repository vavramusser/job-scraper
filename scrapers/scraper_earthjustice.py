# scraper for Earth Justice
# last updated 11/29/2025

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_earthjustice():
    """Scrape Earthjustice job listings from HTML"""
    
    url = "https://earthjustice.org/about/jobs"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    jobs = []
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main jobs container
        jobs_container = soup.find('div', {'data-node': 'eqc9k3sjw4tr'})

        if not jobs_container:
            print("Could not find jobs container with data-node")
            return jobs

        print(f"Found jobs container")
        
        # Find all job links - they're in <p class="m-0"> tags with <a> inside
        job_paragraphs = jobs_container.find_all('p', class_='m-0')
        
        print(f"Found {len(job_paragraphs)} Earthjustice job listings")
        
        for p in job_paragraphs:
            link = p.find('a')
            if not link:
                continue
            
            title = link.get_text(strip=True)
            job_url = link.get('href', '')
            
            # Location is in the next paragraph with class "p_size--small"
            location = 'Location not specified'
            next_p = p.find_next_sibling('p', class_='p_size--small')
            if next_p:
                location = next_p.get_text(strip=True)
            
            # No description available on listing page
            description = ''
            
            jobs.append({
                'company': 'Earthjustice',
                'title': title,
                'url': job_url,
                'location': location,
                'description': description,
                'date_found': datetime.now().strftime('%Y-%m-%d')
            })
        
        print(f"Successfully scraped {len(jobs)} jobs from Earthjustice")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Earthjustice: {e}")
    except Exception as e:
        print(f"Error parsing Earthjustice data: {e}")
    
    return jobs