import requests
from bs4 import BeautifulSoup

print("="*60)
print("DIAGNOSTIC TEST FOR CENTER FOR JUSTICE INNOVATION SCRAPER")
print("="*60)

url = "https://innovatingjustice.applytojob.com/apply"

print(f"\n1. Testing connection to {url}...")
try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    print(f"   ✓ Status Code: {response.status_code}")
    print(f"   ✓ Content Length: {len(response.content)} bytes")
    
    print("\n2. Checking for API key in page source...")
    if 'apikey=' in response.text:
        # Find the API key
        start = response.text.find('apikey=') + 7
        end = start + 50
        snippet = response.text[start:end]
        print(f"   ✓ Found API key pattern: apikey={snippet}")
    else:
        print("   ✗ No API key found in page source")
    
    print("\n3. Parsing HTML structure...")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check for job listings
    job_items = soup.find_all('li', class_='list-group-item')
    print(f"   Found {len(job_items)} <li class='list-group-item'> elements")
    
    if len(job_items) > 0:
        print("\n4. Examining first job item structure:")
        first_item = job_items[0]
        print(f"   HTML: {str(first_item)[:500]}...")
        
        # Try to extract info
        heading = first_item.find('h4', class_='list-group-item-heading')
        if heading:
            print(f"\n   ✓ Found heading: {heading.get_text(strip=True)[:50]}")
            link = heading.find('a')
            if link:
                print(f"   ✓ Found link: {link.get('href', 'NO HREF')}")
        else:
            print("   ✗ No heading found")
        
        list_inline = first_item.find('ul', class_='list-inline')
        if list_inline:
            print(f"   ✓ Found list-inline with {len(list_inline.find_all('li'))} items")
        else:
            print("   ✗ No list-inline found")
    else:
        print("\n4. No job items found - checking page structure...")
        
        # Look for any job-related content
        all_links = soup.find_all('a', href=True)
        job_links = [a for a in all_links if 'apply' in a.get('href', '').lower()]
        print(f"   Found {len(job_links)} links with 'apply' in href")
        
        if job_links:
            print(f"\n   Sample link: {job_links[0].get('href')}")
            print(f"   Sample text: {job_links[0].get_text(strip=True)[:50]}")
        
        # Check page title
        title = soup.find('title')
        if title:
            print(f"\n   Page title: {title.get_text()}")
        
        # Look for any list items
        all_li = soup.find_all('li')
        print(f"\n   Total <li> elements on page: {len(all_li)}")
        
        if all_li:
            print(f"   First <li> classes: {all_li[0].get('class', [])}")

except Exception as e:
    print(f"\n   ✗ ERROR: {e}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)