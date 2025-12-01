# scraper for Esri
# last updated 11/30/2025

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

def get_total_pages(driver):
    """Detect the total number of pages from pagination"""
    try:
        # Wait for pagination to load
        time.sleep(2)
        
        # Look for pagination elements - try different common patterns
        # Pattern 1: Look for the last page number link
        try:
            pagination_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='?p=']")
            if pagination_links:
                # Extract page numbers from URLs
                page_numbers = []
                for link in pagination_links:
                    href = link.get_attribute('href')
                    if '?p=' in href:
                        try:
                            page_num = int(href.split('?p=')[1].split('&')[0])
                            page_numbers.append(page_num)
                        except (ValueError, IndexError):
                            continue
                
                if page_numbers:
                    max_page = max(page_numbers)
                    print(f"Detected {max_page} total pages from pagination links")
                    return max_page
        except Exception as e:
            print(f"Method 1 failed: {e}")
        
        # Pattern 2: Look for text like "Page 1 of 28"
        try:
            page_text_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'of')]")
            for element in page_text_elements:
                text = element.text
                if 'of' in text.lower():
                    # Try to extract number after "of"
                    parts = text.lower().split('of')
                    if len(parts) == 2:
                        try:
                            total = int(''.join(filter(str.isdigit, parts[1])))
                            print(f"Detected {total} total pages from text: '{text}'")
                            return total
                        except ValueError:
                            continue
        except Exception as e:
            print(f"Method 2 failed: {e}")
        
        # Pattern 3: Look for the last page button/link by finding highest number
        try:
            all_text_elements = driver.find_elements(By.XPATH, "//a | //button")
            numbers = []
            for element in all_text_elements:
                text = element.text.strip()
                if text.isdigit():
                    numbers.append(int(text))
            
            if numbers:
                # Filter out unreasonably high numbers (like years)
                reasonable_numbers = [n for n in numbers if 1 <= n <= 1000]
                if reasonable_numbers:
                    max_page = max(reasonable_numbers)
                    print(f"Detected {max_page} total pages from page numbers")
                    return max_page
        except Exception as e:
            print(f"Method 3 failed: {e}")
        
        print("Could not detect total pages, defaulting to 3")
        return 3
        
    except Exception as e:
        print(f"Error detecting total pages: {e}")
        print("Defaulting to 3 pages")
        return 3

def scrape_esri():
    """Scrape jobs from Esri careers page using Selenium with automatic ChromeDriver management"""
    
    jobs = []
    base_url = "https://www.esri.com"
    careers_base_url = "https://www.esri.com/en-us/about/careers/job-search"
    
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    
    try:
        print("Initializing Chrome driver with webdriver-manager...")
        # Automatically download and use the correct ChromeDriver version
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # First, go to page 1 to detect total number of pages
        print(f"Loading first page to detect total pages...")
        driver.get(careers_base_url)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "careers-link")))
        
        # Detect total number of pages
        total_pages = get_total_pages(driver)
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Loop through all pages
        for page_num in range(1, total_pages + 1):
            # Build URL for current page
            if page_num == 1:
                careers_url = careers_base_url
            else:
                careers_url = f"{careers_base_url}?p={page_num}"
            
            print(f"\n{'='*60}")
            print(f"Scraping page {page_num} of {total_pages}")
            print(f"URL: {careers_url}")
            print(f"{'='*60}")
            
            driver.get(careers_url)
            
            # Wait for job cards to load
            print("Waiting for job cards to load...")
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "careers-link")))
            
            # Give extra time for all cards to render
            time.sleep(2)
            
            # Scroll to load all jobs on this page (if lazy loading is used)
            print("Scrolling to load all jobs on this page...")
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 5  # Reduced since we're doing this per page
            
            while scroll_attempts < max_scrolls:
                # Scroll down
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                # Calculate new scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_attempts += 1
            
            # Find all job cards on this page
            print("Extracting job information...")
            job_cards = driver.find_elements(By.CLASS_NAME, "careers-link")
            print(f"Found {len(job_cards)} job cards on page {page_num}")
            
            for idx, card in enumerate(job_cards):
                try:
                    # Extract job URL
                    job_url = card.get_attribute('href')
                    if not job_url:
                        continue
                    
                    # Extract job title
                    try:
                        title_element = card.find_element(By.CLASS_NAME, "careers-title")
                        title = title_element.text.strip()
                    except NoSuchElementException:
                        title = "Title not found"
                    
                    # Extract location
                    try:
                        location_element = card.find_element(By.CLASS_NAME, "careers-bottomText")
                        location = location_element.text.strip()
                    except NoSuchElementException:
                        location = "Location not specified"
                    
                    # Extract description
                    try:
                        description_element = card.find_element(By.CLASS_NAME, "careers-description")
                        description = description_element.text.strip()
                    except NoSuchElementException:
                        description = ""
                    
                    # Extract category (optional)
                    try:
                        category_element = card.find_element(By.CLASS_NAME, "careers-category")
                        category = category_element.text.strip()
                        # Append category to description if exists
                        if category:
                            description = f"[{category}] {description}"
                    except NoSuchElementException:
                        pass
                    
                    job = {
                        'company': 'Esri',
                        'title': title,
                        'url': job_url,
                        'location': location,
                        'description': description,
                        'date_found': today
                    }
                    
                    jobs.append(job)
                    
                except Exception as e:
                    print(f"Error processing job card {idx + 1} on page {page_num}: {str(e)}")
                    continue
            
            print(f"Total jobs collected so far: {len(jobs)}")
            
            # Small delay between pages to be respectful
            if page_num < total_pages:
                time.sleep(2)
        
        print(f"\n{'='*60}")
        print(f"Successfully scraped {len(jobs)} Esri jobs from {total_pages} pages")
        print(f"{'='*60}")
        
    except TimeoutException:
        print("Timeout waiting for job cards to load. The page might be loading slowly or the structure has changed.")
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
    finally:
        if driver:
            driver.quit()
            print("Chrome driver closed")
    
    return jobs

# For testing
if __name__ == "__main__":
    print("Testing Esri scraper...")
    jobs = scrape_esri()
    print(f"\nTotal jobs found: {len(jobs)}")
    
    if jobs:
        print("\nFirst 3 jobs:")
        for job in jobs[:3]:
            print(f"\n{'-'*60}")
            print(f"Title: {job['title']}")
            print(f"Location: {job['location']}")
            print(f"URL: {job['url']}")
            print(f"Description: {job['description'][:100]}..." if len(job['description']) > 100 else f"Description: {job['description']}")
