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

# main execution
if __name__ == "__main__":
    
    print("Initializing job scraper...\n")
    init_db()

    ####################################
    ##### API-Based Internal Sites #####
    ####################################

    ### ADP Workforce Now API Calls ###
    # American Forests
    store_jobs(apicall_adpworkforcenow(
        cid = "f4cdd59b-bdcf-4e58-9e68-112518aa9a0a",
        ccId = "19000101_000003",
        company = "American Forests"))
    # CDC Foundation
    store_jobs(apicall_adpworkforcenow(
        cid = "014dfa20-d261-4f83-8d77-5edb4e15f0f8",
        ccId = "19000101_000001",
        company = "CDC Foundation"))
    # Everyone for Gun Safety
    store_jobs(apicall_adpworkforcenow(
        cid = "575de07a-c083-4788-8cd8-24b17ba8cca5",
        ccId = "19000101_000001",
        company = "Everyone for Gun Safety"))
    # Fair Labor Association
    store_jobs(apicall_adpworkforcenow(
        cid = "c6f14a31-8de0-45d7-b429-a90525d403c0",
        ccId = "19000101_000001",
        company = "Fair Labor Association"))
    # Pokagon Band
    #store_jobs(apicall_adpworkforcenow(
    #    cid = "0528a983-eff0-40d1-9539-1ae4fdee6aff",
    #    ccId = "",
    #    company = "Pokagon Band"))
    # United Hospital Fund
    store_jobs(apicall_adpworkforcenow(
        cid = "2e3a3301-b551-4bff-aac6-dbbad84e8de7",
        ccId = "19000101_000001",
        company = "United Hospital Fund"))
    
    ### Resumator API Calls ###
    # Earth Daily
    store_jobs(apicall_resumator(
        apikey = "mJbxSpDuFZEZ2pqWz8SssgHOfFd3iMYX",
        company = "Earth Daily"))

    ### Workable API Calls ###
    # Innocence Project
    store_jobs(apicall_workable(
        url_extension = "675118",
        company = "Innnocence Project"))


    #################################
    ##### Hosted External Sites #####
    #################################

    ### Apply to Job ###
    # GeoOwl
    store_jobs(scrape_applytojob(
        slug = "geoowl",
        company = "GeoOwl"))
    # Center for Justice Innovation
    store_jobs(scrape_applytojob(
        slug = "innovatingjustice",
        company = "Center for Justice Innovation"))
    
    ### Greenhouse ###
    # Greenpeace
    store_jobs(scrape_greenhouse(
        slug = "greenpeace",
        company = "Greenpeace"))
    # Pro Publica
    store_jobs(scrape_greenhouse(
        slug = "propublica",
        company = "Pro Publica"))
    # Vera Institute of Justice
    store_jobs(scrape_greenhouse(
        slug = "verainstituteofjustice",
        company = "Vera Institute of Justice"))
    
    ### Oracle Cloud HCM (Human Capital Management) ###
    # Abt Global
    store_jobs(scrape_oracle(
        tenant_id = "egpy",
        region = "us2",
        site_number = "CX_3001",
        company = "Abt Global"))
    # DC Water
    store_jobs(scrape_oracle(
        tenant_id = "elxb",
        region = "us2",
        site_number = "CX_3001",
        company = "DC Water"))
    
    ### UKG Pro (fka UtilPro) Human Capital Management (HCM) ###
    # National Committee for Quality Assurance (NCQA)
    store_jobs(apicall_ultipro(
        company_id = "NAT1056NCFQA",
        board_id = "d207d599-5f3a-4f5a-a1be-bada9a5675b1",
        company = "National Committee for Quality Assurance (NCQA)"))


    ###########################
    ##### Unique Scrapers #####
    ###########################

    # Earth Justice
    earthjustice_jobs = scrape_earthjustice()
    print(f"Found {len(earthjustice_jobs)} total Earthjustice jobs")
    new_earthjustice_jobs = store_jobs(earthjustice_jobs)

    # Esri
    esri_jobs = scrape_esri()
    print(f"Found {len(esri_jobs)} total Esri jobs")
    new_esri_jobs = store_jobs(esri_jobs)

    # The Nature Conservancy
    tnc_jobs = scrape_tnc()
    print(f"Found {len(tnc_jobs)} total TNC jobs")
    new_tnc_jobs = store_jobs(tnc_jobs)

    # Public Health Institute (PHI)
    phi_jobs = scrape_phi() 
    print(f"Found {len(phi_jobs)} total PHI jobs")
    new_phi_jobs = store_jobs(phi_jobs)

    # Planet Labs
    planet_jobs = scrape_planet()
    print(f"Found {len(planet_jobs)} total Planet Labs jobs")
    new_planet_jobs = store_jobs(planet_jobs)

    # Research Triangle Institue (RTI)
    rti_jobs = scrape_rti()
    print(f"Found {len(rti_jobs)} total RTI jobs")
    new_rti_jobs = store_jobs(rti_jobs)
    
    print("\nScraping complete.")