import json
import sys

def load_companies(filename='companies.json'):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"companies": []}

def save_companies(data, filename='companies.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def company_exists(data, company_name):
    """Check if company already exists (case-insensitive)"""
    existing = [c['company'].lower() for c in data['companies']]
    return company_name.lower() in existing

def add_company_interactive():
    """Interactive prompt to add a new company"""
    data = load_companies()
    
    print("\n=== Add New Company ===\n")
    
    company = input("Company name: ").strip()
    
    # Check for duplicates
    if company_exists(data, company):
        print(f"\n⚠️  WARNING: '{company}' already exists!")
        overwrite = input("Do you want to view the existing entry? (y/n): ").lower()
        if overwrite == 'y':
            existing = [c for c in data['companies'] if c['company'].lower() == company.lower()][0]
            print(f"\nExisting entry:\n{json.dumps(existing, indent=2)}")
        return
    
    # Select scraper type
    print("\nAvailable scraper types:")
    scrapers = [
        "workday",
        "adp_workforce",
        "workable", 
        "resumator",
        "ultipro",
        "applytojob",
        "greenhouse",
        "oracle",
        "lever",
        "unique_earthjustice",
        "unique_esri",
        "unique_phi",
        "unique_planet",
        "unique_tnc",
        "unique_rti"
    ]
    for i, s in enumerate(scrapers, 1):
        print(f"  {i}. {s}")
    
    choice = int(input("\nSelect scraper type (number): "))
    scraper = scrapers[choice - 1]
    
    # Get parameters based on scraper type
    params = {}
    
    if scraper == "adp_workforce":
        params['cid'] = input("cid: ").strip()
        params['ccId'] = input("ccId: ").strip()
    elif scraper == "workable":
        params['url_extension'] = input("url_extension: ").strip()
    elif scraper == "resumator":
        params['apikey'] = input("apikey: ").strip()
    elif scraper == "ultipro":
        params['company_id'] = input("company_id: ").strip()
        params['board_id'] = input("board_id: ").strip()
    elif scraper in ["applytojob", "greenhouse"]:
        params['slug'] = input("slug: ").strip()
    elif scraper == "oracle":
        params['tenant_id'] = input("tenant_id: ").strip()
        params['region'] = input("region: ").strip()
        params['site_number'] = input("site_number: ").strip()
    elif scraper == "lever":
        params["slug"] = input("slug: ").strip()
    elif scraper == "workday":
        params["company_slug"] = input("company_slug: ").strip()
        params["page_slug"] = input("page_slug: ").strip()
        params["region"] = input("region: ").strip()

    # unique scrapers don't need params
    
    notes = input("Notes (optional): ").strip()
    
    # Build entry
    entry = {
        "company": company,
        "scraper": scraper,
        "params": params
    }
    if notes:
        entry["notes"] = notes
    
    # Add to data
    data['companies'].append(entry)
    
    # Save
    save_companies(data)
    
    print(f"\n✅ Successfully added '{company}'!")
    print(f"Total companies: {len(data['companies'])}")

def list_companies():
    """List all companies in the database"""
    data = load_companies()
    print(f"\n=== Companies ({len(data['companies'])} total) ===\n")
    for i, company in enumerate(data['companies'], 1):
        print(f"{i}. {company['company']} ({company['scraper']})")

def search_companies(search_term):
    """Search for companies by name"""
    data = load_companies()
    matches = [c for c in data['companies'] if search_term.lower() in c['company'].lower()]
    
    if matches:
        print(f"\n=== Found {len(matches)} match(es) ===\n")
        for company in matches:
            print(json.dumps(company, indent=2))
    else:
        print(f"\n❌ No matches found for '{search_term}'")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "list":
            list_companies()
        elif command == "search" and len(sys.argv) > 2:
            search_companies(sys.argv[2])
        elif command == "add":
            add_company_interactive()
        else:
            print("Usage: python add_company.py [add|list|search <term>]")
    else:
        add_company_interactive()