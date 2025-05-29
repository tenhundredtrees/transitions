import requests
from bs4 import BeautifulSoup
import time
import random
import json

def safe_request(url, headers=None):
    """Make a safe request with random delay and user agent"""
    if headers is None:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        headers = {'User-Agent': random.choice(user_agents)}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        time.sleep(random.uniform(3, 7))  # Slower crawl to avoid blocking
        return response
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def search_local_newspaper_contacts():
    """Search for local newspaper journalist contacts"""
    
    newspaper_websites = [
        "https://www.jagran.com/gorakhpur",
        "https://www.amarujala.com/gorakhpur",
        "https://www.bhaskar.com/gorakhpur",
        "https://www.livehindustan.com/gorakhpur"
    ]
    
    journalists = {}
    
    for site in newspaper_websites:
        print(f"Searching {site} for journalist contacts...")
        response = safe_request(site)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for contact pages or staff pages
            contact_links = soup.find_all('a', href=True, string=lambda text: text and 
                                        any(word in text.lower() for word in ['contact', 'staff', 'team', 'bureau']))
            
            for link in contact_links[:3]:  # Check first 3 contact-type links
                href = link['href']
                if not href.startswith('http'):
                    href = site + href
                
                print(f"Checking contact page: {href}")
                contact_response = safe_request(href)
                if contact_response:
                    contact_soup = BeautifulSoup(contact_response.text, 'html.parser')
                    
                    # Look for names and phone numbers
                    text_content = contact_soup.get_text()
                    lines = text_content.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        # Look for lines with phone numbers and potential names
                        if any(char.isdigit() for char in line) and len(line) < 100:
                            if 'gorakhpur' in line.lower() or 'bureau' in line.lower():
                                journalists[site] = line
                                break
    
    return journalists

def search_government_information_contacts():
    """Search for government information department contacts"""
    
    govt_info_contacts = {
        "District Information Officer": {
            "department": "Information & Public Relations Department",
            "location": "Gorakhpur",
            "contact_method": "Call District Collector office for current contact",
            "phone": "0551-2334455",
            "role": "Coordinates with local media"
        },
        "Government Press Reporter": {
            "department": "UP Information Department",
            "location": "Gorakhpur Bureau",
            "contact_method": "Contact through state information dept",
            "role": "Government news coordination"
        }
    }
    
    return govt_info_contacts

def search_press_club_contacts():
    """Search for press club information"""
    
    press_clubs = {
        "Gorakhpur Press Club": {
            "type": "Main press club",
            "location": "Gorakhpur city",
            "research_method": "Visit in person or call local journalists",
            "potential_contacts": "President, Secretary of press club",
            "note": "Press clubs maintain journalist directories"
        },
        "District Press Club": {
            "type": "District level organization",
            "location": "Near collectorate or court area",
            "research_method": "Ask district administration for contact"
        }
    }
    
    return press_clubs

def search_online_news_portals():
    """Search for online news portal journalists"""
    
    online_portals = [
        "gorakhpurnews.com",
        "eastmojo.com",
        "newstrack.com",
        "patrika.com"
    ]
    
    portal_contacts = {}
    
    for portal in online_portals:
        url = f"https://{portal}"
        print(f"Checking {url} for Gorakhpur bureau...")
        
        response = safe_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for "about us" or "contact" pages
            about_links = soup.find_all('a', href=True, string=lambda text: text and 
                                      any(word in text.lower() for word in ['about', 'contact', 'bureau']))
            
            if about_links:
                portal_contacts[portal] = {
                    "status": "Has contact page",
                    "research_needed": "Manual check of contact page",
                    "focus": "Look for Gorakhpur/Eastern UP bureau"
                }
            else:
                portal_contacts[portal] = {
                    "status": "No obvious contact page found",
                    "research_needed": "Direct search or social media check"
                }
    
    return portal_contacts

def create_journalist_research_report():
    """Create comprehensive journalist research report"""
    
    print("Starting Gorakhpur journalist research...")
    
    # Search various sources
    newspaper_contacts = search_local_newspaper_contacts()
    govt_contacts = search_government_information_contacts()
    press_club_info = search_press_club_contacts()
    online_portal_contacts = search_online_news_portals()
    
    # Compile comprehensive report
    report = {
        "district": "Gorakhpur",
        "state": "Uttar Pradesh", 
        "research_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "newspaper_contacts": newspaper_contacts,
        "government_information_contacts": govt_contacts,
        "press_club_information": press_club_info,
        "online_portal_contacts": online_portal_contacts,
        "manual_research_needed": {
            "press_club_visit": "Visit Gorakhpur Press Club for member directory",
            "government_contact": "Call District Information Officer for journalist list",
            "social_media_search": "Search Facebook/Twitter for Gorakhpur journalists",
            "direct_calls": "Call newspaper offices directly",
            "field_research": "Visit newspaper offices in person"
        },
        "contact_strategy": [
            "Call District Collector: 0551-2334455 - Ask for District Information Officer contact",
            "Visit local newspaper offices in Gorakhpur city",
            "Contact known journalists for referrals",
            "Check with local press club for member list",
            "Search social media for active Gorakhpur journalists"
        ]
    }
    
    return report

if __name__ == "__main__":
    # Generate journalist research report
    report = create_journalist_research_report()
    
    # Save to JSON file
    with open('gorakhpur_journalist_research.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\nJournalist research report saved to gorakhpur_journalist_research.json")
    print("\nSummary:")
    print(f"- Newspaper contacts found: {len(report['newspaper_contacts'])}")
    print(f"- Government contacts mapped: {len(report['government_information_contacts'])}")
    print(f"- Press clubs identified: {len(report['press_club_information'])}")
    print(f"- Online portals checked: {len(report['online_portal_contacts'])}")
    print(f"- Manual research tasks: {len(report['manual_research_needed'])}")
