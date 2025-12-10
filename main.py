import json

# import database functions
from database import init_db, store_jobs

# import scrapers
from scrapers.apicall_adpworkforcenow import apicall_adpworkforcenow
from scrapers.apicall_resumator import apicall_resumator
from scrapers.apicall_ultipro import apicall_ultipro
from scrapers.apicall_workable import apicall_workable
from scrapers.scraper_applytojob import scrape_applytojob
from scrapers.scraper_greenhouse import scrape_greenhouse
from scrapers.scraper_oraclecloudhcm import scrape_oracle

# unique srapers
from scrapers.scraper_earthjustice import scrape_earthjustice
from scrapers.scraper_esri import scrape_esri
from scrapers.scraper_phi import scrape_phi
from scrapers.scraper_planet import scrape_planet
from scrapers.scraper_tnc import scrape_tnc
from scrapers.scraper_rti import scrape_rti

# scraper mapping
SCRAPERS = {
    'adp_workforce': lambda params: apicall_adpworkforcenow(
        cid=params['cid'], 
        ccId=params['ccId'], 
        company=params['company']
    ),
    'workable': lambda params: apicall_workable(
        url_extension=params['url_extension'], 
        company=params['company']
    ),
    'resumator': lambda params: apicall_resumator(
        apikey=params['apikey'],
        company=params['company']
    ),
    'ultipro': lambda params: apicall_ultipro(
        company_id=params['company_id'],
        board_id=params['board_id'],
        company=params['company']
    ),
    'applytojob': lambda params: scrape_applytojob(
        slug=params['slug'],
        company=params['company']
    ),
    'greenhouse': lambda params: scrape_greenhouse(
        slug=params['slug'],
        company=params['company']
    ),
    'oracle': lambda params: scrape_oracle(
        tenant_id=params['tenant_id'],
        region=params['region'],
        site_number=params['site_number'],
        company=params['company']
    ),
    'unique_earthjustice': lambda params: scrape_earthjustice(),
    'unique_esri': lambda params: scrape_esri(),
    'unique_phi': lambda params: scrape_phi(),
    'unique_planet': lambda params: scrape_planet(),
    'unique_tnc': lambda params: scrape_tnc(),
    'unique_rti': lambda params: scrape_rti(),
}

# main execution
if __name__ == "__main__":

    def run_scrapers_from_json(json_file='companies.json'):
        """Run all scrapers defined in the JSON config file"""
        init_db()
        
        # Load companies from JSON
        with open(json_file, 'r') as f:
            config = json.load(f)
        
        print(f"Loaded {len(config['companies'])} companies from {json_file}\n")
        
        # Run each scraper
        for entry in config['companies']:
            company = entry['company']
            scraper = entry['scraper']
            params = entry.get('params', {})
            params['company'] = company  # Add company name to params
            
            if scraper in SCRAPERS:
                try:
                    jobs = SCRAPERS[scraper](params)
                    if jobs:  # only store if we got results
                        new_jobs = store_jobs(jobs)
                        print(f"Stored {len(new_jobs)} new jobs from {company}")
                except Exception as e:
                    print(f"Error scraping {company}: {e}")
            else:
                print(f"⚠️  Unknown scraper type '{scraper}' for {company}")
        
        print("\nScraping complete.")

    if __name__ == "__main__":
        run_scrapers_from_json()
    
    print("Initializing job scraper...\n")
    init_db()