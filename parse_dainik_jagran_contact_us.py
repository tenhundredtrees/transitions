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

# Function to parse the "Contact Us" page for Dainik Jagran
def parse_dainik_jagran_contact_us():
    url = 'https://www.jagran.com/contact-us'
    html_content = make_request(url)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the Gorakhpur office details in the parsed HTML. This part is highly dependent on the structure of the "Contact Us" page.
    # Based on a visual check of the "Contact Us" page, you need to identify the part where the Gorakhpur office details are mentioned.
    # For instance, if the "Contact Us" page has a table where office details are listed for different cities, you need to find the row for "Gorakhpur."
    
    # An example (this part might need a more specific parsing logic based on the actual HTML structure):
    # Let us assume that the "Contact Us" page has a table where one of the columns is the city name and another column is the contact details.
    # The actual parsing logic needs to be adjusted based on the real structure of the "Contact Us" page.
    
    # For demonstration, here is a very general way to find all the "div" elements which might contain the office details:
    contact_details = []
    for div in soup.find_all('div', class_='contact-details'):  # Assume 'contact-details' is the class used for the contact details divs, this is a placeholder class name.
        # Look for a specific div that mentions "Gorakhpur" in it.
        if "Gorakhpur" in div.text:
            contact_details.append(div.text.strip())
    
    return contact_details

if __name__ == "__main__":
    try:
        gorakhpur_contact_details = parse_dainik_jagran_contact_us()
        if gorakhpur_contact_details:
            print("Dainik Jagran Gorakhpur Contact Details:")
            for details in gorakhpur_contact_details:
                print(details)
        else:
            print("No contact details found for Gorakhpur in Dainik Jagran 'Contact Us' page.")
    except Exception as e:
        print("An error occurred: {}".format(e))
