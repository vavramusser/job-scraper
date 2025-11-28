# scraper for Abt Global
# last updated 11/27/2025

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def scrape_abt():
    """Scrape Abt Global job listings via Oracle API"""
    
    url = "https://egpy.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
    
    params = {
        'onlyData': 'true',
        'expand': 'requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations',
        'finder': 'findReqs;siteNumber=CX_3001,facetsList=LOCATIONS;WORK_LOCATIONS;TITLES;CATEGORIES;POSTING_DATES,limit=100,sortBy=POSTING_DATES_DESC'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }
    
    jobs = []
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # The job listings are in items[0].requisitionList
        if 'items' in data and len(data['items']) > 0:
            requisitions = data['items'][0].get('requisitionList', [])
            
            print(f"Found {len(requisitions)} Abt job listings, fetching details...")
            
            for req in requisitions:
                # Build the job URL
                job_id = req.get('Id')
                job_url = f"https://egpy.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/JoinAbt/job/{job_id}"
                
                # Get location from API
                location = req.get('PrimaryLocation', 'Location not specified')
                title = req.get('Title', 'No title')
                
                # Try to fetch description from individual job page
                description = ''
                try:
                    job_response = requests.get(job_url, headers=headers, timeout=10)
                    job_response.raise_for_status()
                    job_soup = BeautifulSoup(job_response.content, 'html.parser')
                    
                    # Look for description content
                    desc_div = job_soup.find('div', class_='job-details__description-content')
                    if desc_div:
                        description = desc_div.get_text(separator='\n', strip=True)
                    
                    print(f"  ✓ Fetched: {title}")
                    time.sleep(0.5)  # Be nice to the server
                    
                except Exception as e:
                    print(f"  ⚠ Could not fetch description for {title}: {e}")
                    # Continue anyway with empty description
                
                jobs.append({
                    'company': 'Abt Global',
                    'title': title,
                    'url': job_url,
                    'location': location,
                    'description': description,
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                })
        
        print(f"Successfully scraped {len(jobs)} jobs from Abt Global")
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Abt Global: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error parsing Abt Global data: {e}")
    
    return jobs