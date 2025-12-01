# scraper for Planet Labs
# last updated 11/30/2025

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import time

def scrape_planet():
    """Scrape jobs from Planet Labs careers page using Selenium"""
    
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    jobs = []
    driver = None
    
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to Planet Labs careers page
        url = "https://www.planet.com/company/careers"
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for the page to load and job listings to appear
        wait = WebDriverWait(driver, 15)
        
        # Wait for the department buttons container to load
        print("Waiting for page to load...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[id^='dep_']")))
        
        # Give extra time for all jobs to render
        time.sleep(3)
        
        # Try to close any cookie banners or popups
        try:
            # Look for common close button patterns
            close_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='close'], button[aria-label*='close'], button[aria-label*='Close']")
            for btn in close_buttons:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(0.5)
                except:
                    pass
        except:
            pass
        
        # Find all department buttons
        department_buttons = driver.find_elements(By.CSS_SELECTOR, "button[id^='dep_']")
        print(f"Found {len(department_buttons)} departments")
        
        # Click each department button to reveal jobs
        for idx, button in enumerate(department_buttons):
            try:
                # Get department name (button text without the count)
                dept_text = button.text
                # Remove the number in parentheses if present
                department = dept_text.split('\n')[0] if '\n' in dept_text else dept_text.rsplit(' ', 1)[0]
                
                print(f"Clicking department: {department}")
                
                # Use JavaScript click to avoid click interception issues
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)  # Wait for jobs to load
                
                # Find the sibling div that contains the job listings
                # It should be the next sibling after the button
                try:
                    # Get the next sibling div using JavaScript
                    sibling_div = driver.execute_script(
                        "return arguments[0].nextElementSibling;", 
                        button
                    )
                    
                    if sibling_div:
                        # Find all job buttons within this sibling div
                        # Jobs are in buttons with class containing specific patterns
                        job_buttons = sibling_div.find_elements(By.CSS_SELECTOR, "button.css-1n36k1b")
                        
                        print(f"  Found {len(job_buttons)} jobs in {department}")
                        
                        for job_btn in job_buttons:
                            try:
                                # Get the full text from the button
                                full_text = job_btn.text.strip()
                                
                                if not full_text:
                                    continue
                                
                                # Split by newline - first line is title, second is location
                                lines = full_text.split('\n')
                                job_title = lines[0].strip() if len(lines) > 0 else ""
                                location = lines[1].strip() if len(lines) > 1 else "Location not specified"
                                
                                # Try to get job ID from button attributes
                                job_url = "https://www.planet.com/company/careers"
                                
                                # Check for data attributes or id that might contain job info
                                button_id = job_btn.get_attribute('id')
                                data_job_id = job_btn.get_attribute('data-job-id')
                                
                                if button_id:
                                    job_url = f"https://www.planet.com/company/careers#{button_id}"
                                elif data_job_id:
                                    job_url = f"https://www.planet.com/company/careers#{data_job_id}"
                                else:
                                    # Fallback: use title as identifier
                                    job_slug = job_title.lower().replace(' ', '-').replace(',', '').replace('&', 'and')
                                    job_url = f"https://www.planet.com/company/careers#{job_slug}"
                                
                                if job_title:
                                    jobs.append({
                                        'company': 'Planet Labs',
                                        'title': job_title,
                                        'location': location,
                                        'url': job_url,
                                        'description': '',
                                        'date_found': datetime.now().strftime('%Y-%m-%d')
                                    })
                                    print(f"    {job_title} - {location}")
                            
                            except Exception as e:
                                print(f"    Error processing job: {e}")
                                continue
                
                except Exception as e:
                    print(f"  Error finding jobs for {department}: {e}")
                
            except Exception as e:
                print(f"Error clicking department button: {e}")
                continue
        
        print(f"\nTotal jobs scraped: {len(jobs)}")
        
    except TimeoutException:
        print("Timeout waiting for page elements to load")
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        if driver:
            driver.quit()
    
    return jobs


if __name__ == "__main__":
    # Test the scraper
    jobs = scrape_planet()
    print(f"\nScraped {len(jobs)} jobs from Planet Labs")
    
    # Print first few jobs as sample
    for job in jobs[:3]:
        print(f"\n{job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")