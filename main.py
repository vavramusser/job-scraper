import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time

# import database functions
from database import init_db, store_jobs

# import scraper functions
from scrapers.scraper_abt import scrape_abt
from scrapers.scraper_americanforests import scrape_americanforests
from scrapers.scraper_cji import scrape_cji
from scrapers.scraper_earthdaily import scrape_earthdaily
from scrapers.scraper_earthjustice import scrape_earthjustice
from scrapers.scraper_esri import scrape_esri
from scrapers.scraper_geoowl import scrape_geoowl
from scrapers.scraper_greenpeace import scrape_greenpeace
from scrapers.scraper_phi import scrape_phi
from scrapers.scraper_planet import scrape_planet
from scrapers.scraper_innocence import scrape_innocence
from scrapers.scraper_tnc import scrape_tnc
from scrapers.scraper_rti import scrape_rti

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

    print("\nScraping American Forests...")
    americanforests_jobs = scrape_americanforests()
    print(f"Found {len(americanforests_jobs)} total American Forests jobs")
    new_americanforests_jobs = store_jobs(americanforests_jobs)
    display_new_jobs(new_americanforests_jobs)

    print("\nScraping The Center for Justice Innovation...")
    cji_jobs = scrape_cji()
    print(f"Found {len(cji_jobs)} total ACJI jobs")
    new_cji_jobs = store_jobs(cji_jobs)
    display_new_jobs(new_cji_jobs)

    print("\nScraping EarthDaily...")
    earthdaily_jobs = scrape_earthdaily()
    print(f"Found {len(earthdaily_jobs)} total EarthDaily jobs")
    new_earthdaily_jobs = store_jobs(earthdaily_jobs)
    display_new_jobs(new_earthdaily_jobs)

    print("\nScraping Earthjustice...")
    earthjustice_jobs = scrape_earthjustice()
    print(f"Found {len(earthjustice_jobs)} total Earthjustice jobs")
    new_earthjustice_jobs = store_jobs(earthjustice_jobs)
    display_new_jobs(new_earthjustice_jobs)

    print("\nScraping Esri...")
    esri_jobs = scrape_esri()
    print(f"Found {len(esri_jobs)} total Esri jobs")
    new_esri_jobs = store_jobs(esri_jobs)
    display_new_jobs(new_esri_jobs)

    print("\nScraping GeoOwl...")
    geoowl_jobs = scrape_geoowl()
    print(f"Found {len(geoowl_jobs)} total GeoOwl jobs")
    new_geoowl_jobs = store_jobs(geoowl_jobs)
    display_new_jobs(new_geoowl_jobs)

    print("\nScraping Greenpeace...")
    greenpeace_jobs = scrape_greenpeace()
    print(f"Found {len(greenpeace_jobs)} total Greenpeace jobs")
    new_greenpeace_jobs = store_jobs(greenpeace_jobs)
    display_new_jobs(new_greenpeace_jobs)

    print("\nScraping Innocence Project...")
    innocence_jobs = scrape_innocence()
    print(f"Found {len(innocence_jobs)} total Innocence Project jobs")
    new_innocence_jobs = store_jobs(innocence_jobs)
    display_new_jobs(new_innocence_jobs)

    print("\nScraping The Nature Conservancy...")
    tnc_jobs = scrape_tnc()
    print(f"Found {len(tnc_jobs)} total TNC jobs")
    new_tnc_jobs = store_jobs(tnc_jobs)
    display_new_jobs(new_tnc_jobs)

    print("\nScraping PHI...")
    phi_jobs = scrape_phi() 
    print(f"Found {len(phi_jobs)} total PHI jobs")
    new_phi_jobs = store_jobs(phi_jobs)
    display_new_jobs(new_phi_jobs)

    print("\nScraping Planet Labs...")
    planet_jobs = scrape_planet()
    print(f"Found {len(planet_jobs)} total Planet Labs jobs")
    new_planet_jobs = store_jobs(planet_jobs)
    display_new_jobs(new_planet_jobs)

    print("\nScraping RTI International...")
    rti_jobs = scrape_rti()
    print(f"Found {len(rti_jobs)} total RTI jobs")
    new_rti_jobs = store_jobs(rti_jobs)
    display_new_jobs(new_rti_jobs)
    
    print("\nScraping complete. Database saved to jobs.db")