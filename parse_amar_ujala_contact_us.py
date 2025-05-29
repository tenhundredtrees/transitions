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

# Function to parse the "Contact Us" page for Amar Ujala
def parse_amar_ujala_contact_us():
    url = 'https://www.amarujala.com/contact-us'
    html_content = make_request(url)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Search for the string "Gorakhpur" in the entire HTML content
    gorakhpur_mention = soup.find(string=lambda text: "Gorakhpur" in str(text).lower())

    if gorakhpur_mention:
        # If "Gorakhpur" is found, return the parent element's text for more context
        parent_element = gorakhpur_mention.find_parent()
        if parent_element:
            return parent_element.text.strip()
        else:
            return gorakhpur_mention.strip()
    
    return "No mention of Gorakhpur found in the 'Contact Us' page."

if __name__ == "__main__":
    try:
        gorakhpur_contact_details = parse_amar_ujala_contact_us()
        if gorakhpur_contact_details:
            print("Amar Ujala Gorakhpur Contact Details:")
            print(gorakhpur_contact_details)
        else:
            print("No contact details found for Gorakhpur in Amar Ujala 'Contact Us' page.")
    except Exception as e:
        print("An error occurred: {}".format(e))
