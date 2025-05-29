import requests
from bs4 import BeautifulSoup
import time
import random

# Define a function to make a request with a random user-agent string to mimic a real user
def make_request(url):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    ]
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Function to parse the Gorakhpur edition page for contact details
def parse_gorakhpur_edition():
    url = 'https://www.jagran.com/gorakhpur'
    html_content = make_request(url)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Search for a "Contact Us" link in the Gorakhpur edition page
    contact_us_link = soup.find('a', href=True, text=lambda text: text and "Contact Us" in text)
    
    if contact_us_link:
        contact_us_url = contact_us_link['href']
        if not contact_us_url.startswith('http'):
            contact_us_url = 'https://www.jagran.com' + contact_us_url
        
        # Make another request to the "Contact Us" link found
        contact_us_html = make_request(contact_us_url)
        contact_us_soup = BeautifulSoup(contact_us_html, 'html.parser')
        # Return the "Contact Us" page content
        return contact_us_soup.text.strip()
    
    return "No 'Contact Us' link found on the Gorakhpur edition page."

if __name__ == "__main__":
    try:
        gorakhpur_contact_details = parse_gorakhpur_edition()
        if gorakhpur_contact_details:
            print("Gorakhpur Contact Details:")
            print(gorakhpur_contact_details)
        else:
            print("No contact details found for Gorakhpur in the Dainik Jagran Gorakhpur edition page.")
    except Exception as e:
        print("An error occurred: {}".format(e))
