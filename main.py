import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time

# import database functions
from database import init_db, store_jobs

# import site-specific scraper functions
from scraper_abt import scrape_abt
#from scraper_cna import scrape_cna
from scraper_phi import scrape_phi
#from scraper_rand import scrape_rand
from scraper_rti import scrape_rti

# display new jobs
def display_new_jobs(jobs):
    """Print new jobs to console"""
    if not jobs:
        print("No new jobs found.")
        return
    
    print(f"\n{'='*60}")
    print(f"FOUND {len(jobs)} NEW JOB(S)")
    print(f"{'='*60}\n")
    
    for job in jobs:
        print(f"Company: {job['company']}")
        print(f"Title: {job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}")
        print(f"Date Found: {job['date_found']}")
        print(f"{'-'*60}\n")

# main execution
if __name__ == "__main__":
    print("Initializing job scraper...")
    init_db()
    
    print("\nScraping Abt Global...")
    abt_jobs = scrape_abt()
    print(f"Found {len(abt_jobs)} total Abt jobs")
    new_abt_jobs = store_jobs(abt_jobs)
    display_new_jobs(new_abt_jobs)

    print("Scraping PHI...")
    phi_jobs = scrape_phi() 
    print(f"Found {len(phi_jobs)} total PHI jobs")
    new_phi_jobs = store_jobs(phi_jobs)
    display_new_jobs(new_phi_jobs)

    print("\nScraping RTI International...")
    rti_jobs = scrape_rti()
    print(f"Found {len(rti_jobs)} total RTI jobs")
    new_rti_jobs = store_jobs(rti_jobs)
    display_new_jobs(new_rti_jobs)
    
    print("\nScraping complete. Database saved to jobs.db")