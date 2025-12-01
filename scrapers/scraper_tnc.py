# scraper for The Nature Conservancy (TNC)
# last updated 12/1/2025

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

def scrape_tnc_api():
    """
    Scrape using The Nature Conservancy API endpoint
    Job data is embedded in the HTML page as JavaScript (phApp.ddo object)
    """
    
    api_url = "https://careers.tnc.org/us/en/search-results"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        print(f"Fetching from: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print(f"✓ Successfully fetched HTML (status 200)")
            
            # Look for the phApp.ddo JavaScript object in the HTML
            html_content = response.text
            
            # Find the phApp.ddo object
            if 'phApp.ddo' in html_content:
                print("✓ Found phApp.ddo object in page")
                
                # Extract the JSON data after "phApp.ddo = "
                start_marker = 'phApp.ddo = '
                start_idx = html_content.find(start_marker)
                
                if start_idx != -1:
                    start_idx += len(start_marker)
                    
                    # Find the end of the JSON object (look for }; pattern)
                    # We need to find the matching closing brace
                    brace_count = 0
                    end_idx = start_idx
                    in_json = False
                    
                    for i in range(start_idx, len(html_content)):
                        char = html_content[i]
                        if char == '{':
                            brace_count += 1
                            in_json = True
                        elif char == '}':
                            brace_count -= 1
                            if in_json and brace_count == 0:
                                end_idx = i + 1
                                break
                    
                    if end_idx > start_idx:
                        json_str = html_content[start_idx:end_idx]
                        
                        try:
                            data = json.loads(json_str)
                            print("✓ Successfully parsed phApp.ddo JSON")
                            return data, True
                        except json.JSONDecodeError as e:
                            print(f"✗ Failed to parse JSON: {e}")
                            print(f"JSON snippet: {json_str[:200]}")
                            return None, False
                else:
                    print("✗ Could not find start of phApp.ddo object")
                    return None, False
            else:
                print("✗ phApp.ddo not found in HTML")
                return None, False
        else:
            print(f"✗ Status code: {response.status_code}")
            return None, False
            
    except Exception as e:
        print(f"✗ Error fetching page: {e}")
        return None, False

def parse_tnc_api_data(data):
    """Parse job data from phApp.ddo object"""
    jobs = []
    
    try:
        # The job data is in eagerLoadRefineSearch.data.jobs
        if 'eagerLoadRefineSearch' in data:
            eager_load = data['eagerLoadRefineSearch']
            if 'data' in eager_load and 'jobs' in eager_load['data']:
                job_list = eager_load['data']['jobs']
            else:
                job_list = []
        else:
            # Try alternative structures
            job_list = data.get('jobs', [])
        
        print(f"Found {len(job_list)} jobs in data")
        
        for job_data in job_list:
            try:
                # Extract job information
                title = job_data.get('title', 'Not specified')
                job_id = job_data.get('jobId', job_data.get('reqId', ''))
                
                # Build URL - use applyUrl if available, otherwise construct it
                job_url = job_data.get('applyUrl', '')
                if not job_url and job_id:
                    # Construct URL from jobId if applyUrl not available
                    job_url = f"https://careers.tnc.org/us/en/job/{job_id}"
                
                # Get location
                location = job_data.get('location', '')
                if not location:
                    city = job_data.get('city', '')
                    state = job_data.get('state', '')
                    location_parts = [p for p in [city, state] if p]
                    location = ', '.join(location_parts) if location_parts else 'Not specified'
                
                # Get category/department
                category = job_data.get('category', 'Not specified')
                job_type = job_data.get('type', '')
                
                # Build description
                description_parts = []
                if category and category != 'Not specified':
                    description_parts.append(f"Category: {category}")
                if job_type:
                    description_parts.append(f"Type: {job_type}")
                
                # Get description teaser if available
                desc_teaser = job_data.get('descriptionTeaser', '')
                if desc_teaser:
                    description_parts.append(desc_teaser[:200])
                
                description = " | ".join(description_parts) if description_parts else "No description available"
                
                # Create job entry
                job = {
                    'company': 'The Nature Conservancy',
                    'title': title,
                    'location': location,
                    'url': job_url,
                    'description': description[:500],  # Limit to 500 chars
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                }
                
                jobs.append(job)
                
            except Exception as e:
                print(f"Error parsing job: {e}")
                continue
        
    except Exception as e:
        print(f"Error parsing data structure: {e}")
        import traceback
        traceback.print_exc()
    
    return jobs

def scrape_tnc():
    """Main scraper for The Nature Conservancy jobs"""
    
    print("="*60)
    print("Scraping The Nature Conservancy Jobs")
    print("="*60)
    
    all_jobs = []
    page = 0
    page_size = 10  # From the HTML, size is 10
    
    while True:
        # Construct URL with pagination
        if page == 0:
            url = "https://careers.tnc.org/us/en/search-results"
        else:
            url = f"https://careers.tnc.org/us/en/search-results?from={page * page_size}"
        
        print(f"\nFetching page {page + 1}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"✗ Failed to fetch page {page + 1}")
                break
            
            # Extract phApp.ddo from HTML
            html_content = response.text
            
            if 'phApp.ddo' not in html_content:
                print("✗ No job data found on page")
                break
            
            # Extract JSON
            start_marker = 'phApp.ddo = '
            start_idx = html_content.find(start_marker)
            
            if start_idx == -1:
                break
            
            start_idx += len(start_marker)
            
            # Find end of JSON object
            brace_count = 0
            end_idx = start_idx
            in_json = False
            
            for i in range(start_idx, len(html_content)):
                char = html_content[i]
                if char == '{':
                    brace_count += 1
                    in_json = True
                elif char == '}':
                    brace_count -= 1
                    if in_json and brace_count == 0:
                        end_idx = i + 1
                        break
            
            if end_idx <= start_idx:
                break
            
            json_str = html_content[start_idx:end_idx]
            data = json.loads(json_str)
            
            # Parse jobs from this page
            page_jobs = parse_tnc_api_data(data)
            
            if not page_jobs:
                print("No more jobs found")
                break
            
            all_jobs.extend(page_jobs)
            print(f"✓ Found {len(page_jobs)} jobs on page {page + 1}")
            
            # Check if there are more pages
            if 'eagerLoadRefineSearch' in data:
                total_hits = data['eagerLoadRefineSearch'].get('totalHits', 0)
                print(f"Progress: {len(all_jobs)}/{total_hits} jobs")
                
                if len(all_jobs) >= total_hits:
                    print("✓ All jobs fetched!")
                    break
            else:
                # If we can't determine total, stop after getting fewer than expected
                if len(page_jobs) < page_size:
                    break
            
            page += 1
            
            # Safety limit
            if page > 20:
                print("Reached safety limit of 20 pages")
                break
            
        except Exception as e:
            print(f"✗ Error fetching page {page + 1}: {e}")
            break
    
    if all_jobs:
        print(f"\n✓ Successfully scraped {len(all_jobs)} total jobs from The Nature Conservancy")
    else:
        print("\n✗ No jobs found")
    
    return all_jobs

# Test the scraper
if __name__ == "__main__":
    jobs = scrape_tnc()
    
    if jobs:
        print("\n" + "="*60)
        print(f"TOTAL JOBS FOUND: {len(jobs)}")
        print("="*60)
        
        for job in jobs[:5]:  # Show first 5 jobs
            print(f"\nCompany: {job['company']}")
            print(f"Title: {job['title']}")
            print(f"Location: {job['location']}")
            print(f"URL: {job['url']}")
            print(f"Description: {job['description']}")
            print("-"*60)
        
        if len(jobs) > 5:
            print(f"\n... and {len(jobs) - 5} more jobs")
    else:
        print("\nNo jobs found. See instructions above.")