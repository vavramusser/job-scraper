import requests
from datetime import datetime

# generic function to scrape jobs from UKG Pro (fka UtilPro) Human Capital Management (HCM)
def apicall_ultipro(company_id, board_id, company):

    print(f"Scraping jobs from {company}")
    print(f"{'='*60}")
    
    api_url = f"https://recruiting.ultipro.com/{company_id}/JobBoard/{board_id}/JobBoardView/LoadSearchResults"

    jobs = []

    # request payload - requesting up to 50 jobs
    payload = {
        "opportunitySearch": {
            "Top": 50,
            "Skip": 0,
            "QueryString": ""
        },
        "matchCriteria": {
            "PreferredJobs": [],
            "Educations": [],
            "LicenseAndCertifications": [],
            "Skills": [],
            "hasNoLicenses": False
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:

        response = requests.post(api_url, json = payload, headers = headers, timeout = 15)
        response.raise_for_status()
        data = response.json()
        job_list = data.get('opportunities', [])

        print(f"Found {len(job_list)} jobs\n")

        for job_data in job_list:

            # title
            title = job_data.get('Title', 'Not Specified')

            # location
            location = "Not specified"
            locations = job_data.get('Locations', [])
            
            if locations:

                # check for remote location first
                remote_loc = next((loc for loc in locations if loc.get('LocalizedName') == 'Remote'), None)
                if remote_loc:
                    location = "Remote"
                else:
                    # use first location with address
                    for loc in locations:
                        if loc.get('DisplayAddress') and loc.get('Address'):
                            addr = loc['Address']
                            city = addr.get('City', '')
                            state_code = addr.get('State', {}).get('Code', '')
                            if city and state_code:
                                location = f"{city}, {state_code}"
                                break
                            elif city:
                                location = city
                                break
                    
                    # if still no location, just use localized name or description
                    if location == "Not specified":
                        first_loc = locations[0]
                        location = (first_loc.get('LocalizedName') or 
                                  first_loc.get('LocalizedDescription') or 
                                  "Not specified")
            
            # job URL
            job_id = job_data['Id']
            url = f"https://recruiting.ultipro.com/{company_id}/JobBoard/{board_id}/OpportunityDetail?opportunityId={job_id}"
            
            # create job entry
            job = {
                "id": job_data['Id'],
                'company': company,
                'title': title,
                'location': location,
                'url': url,
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
            
            jobs.append(job)

            print(f"  - {title}")

        print(f"\nSuccessfully scraped {len(jobs)} jobs from {company}")
        print(f"{'='*60}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs from API: {e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return jobs


if __name__ == "__main__":

    # National Committee for Quality Assurance (NCQA)
    test_jobs = apicall_ultipro(
        company_id = "NAT1056NCFQA",
        board_id = "d207d599-5f3a-4f5a-a1be-bada9a5675b1",
        company = "National Committee for Quality Assurance (NCQA)"
    )