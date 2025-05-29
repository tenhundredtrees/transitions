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
        # Random delay between 2-5 seconds to avoid being blocked
        time.sleep(random.uniform(2, 5))
        return response
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def search_gorakhpur_government_contacts():
    """Search for Gorakhpur district government contacts"""
    search_urls = [
        "https://gorakhpur.nic.in/",
        "https://up.gov.in/en/districts/gorakhpur",
        "https://gorakhpur.gov.in/"
    ]
    
    contacts = {}
    
    for url in search_urls:
        print(f"Searching {url}...")
        response = safe_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for contact information
            contact_divs = soup.find_all(['div', 'section', 'p'], 
                                       text=lambda text: text and any(word in text.lower() 
                                       for word in ['contact', 'phone', 'email', 'office']))
            
            for div in contact_divs[:5]:  # Limit to first 5 matches
                text = div.get_text(strip=True)
                if any(char.isdigit() for char in text) and len(text) < 200:
                    contacts[url] = text
                    break
    
    return contacts

def search_block_offices():
    """Search for block-wise office contacts"""
    gorakhpur_blocks = [
        "Gorakhpur", "Gola", "Sahjanwa", "Chauri Chaura", "Khajni",
        "Bansgaon", "Campierganj", "Chargawan", "Pipraich", "Padrauna",
        "Kauriram", "Pharenda", "Jungle Kaudia", "Nichlaul", "Gagaha"
    ]
    
    block_contacts = {}
    
    for block in gorakhpur_blocks:
        print(f"Searching for {block} block office...")
        search_terms = [
            f"{block} block office gorakhpur contact",
            f"{block} tehsil office gorakhpur phone",
            f"{block} BDO office gorakhpur"
        ]
        
        # This would ideally search government directories
        # For now, creating placeholder structure
        block_contacts[block] = {
            "BDO_Office": f"Block Development Office, {block}",
            "Estimated_Contact": f"Will need to call district office for {block} specific contacts",
            "Search_Status": "Requires manual verification"
        }
    
    return block_contacts

def search_ngo_contacts():
    """Search for NGO contacts in Gorakhpur"""
    ngo_search_terms = [
        "NGO Gorakhpur Uttar Pradesh contact",
        "social organization Gorakhpur contact details",
        "development organization Gorakhpur phone"
    ]
    
    # This would search NGO directories and websites
    ngos = {
        "Research_Required": "Need to search NGO directories, GuideStar India, etc.",
        "Potential_Sources": [
            "Credibility Alliance directory",
            "GiveIndia.org",
            "NGO directory websites",
            "Local chamber of commerce"
        ]
    }
    
    return ngos

def create_contact_research_report():
    """Create a comprehensive contact research report"""
    
    print("Starting Gorakhpur contact research...")
    
    # Government contacts
    govt_contacts = search_gorakhpur_government_contacts()
    
    # Block offices
    block_contacts = search_block_offices()
    
    # NGO contacts
    ngo_contacts = search_ngo_contacts()
    
    # Compile report
    report = {
        "district": "Gorakhpur",
        "state": "Uttar Pradesh",
        "research_date": time.strftime("%Y-%m-%d"),
        "government_contacts": govt_contacts,
        "block_offices": block_contacts,
        "ngo_contacts": ngo_contacts,
        "next_steps": [
            "Call district collector office for official directory",
            "Visit government websites for updated contact lists",
            "Contact local journalists for ground-level contacts",
            "Reach out to existing contacts in UP for referrals"
        ]
    }
    
    return report

if __name__ == "__main__":
    # Generate contact research report
    report = create_contact_research_report()
    
    # Save to JSON file
    with open('gorakhpur_contact_research.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("Contact research report saved to gorakhpur_contact_research.json")
    print("\nSummary:")
    print(f"- Government contacts found: {len(report['government_contacts'])}")
    print(f"- Blocks mapped: {len(report['block_offices'])}")
    print(f"- Next steps identified: {len(report['next_steps'])}")
