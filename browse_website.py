import argparse
import requests
from bs4 import BeautifulSoup

def main(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: extracting the title of the page
        page_title = soup.title.string if soup.title else "No title found"
        print(f"Page title: {page_title}")

        # Example: extracting all the links from the page
        links = soup.find_all('a')
        print("Links found on the page:")
        for link in links:
            href = link.get('href')
            text = link.text
            print(f"{text} -> {href}")
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Browse a website and extract some information.")
    parser.add_argument("--url", help="The URL of the website to browse.")
    
    args = parser.parse_args()
    
    if not args.url:
        print("Please provide a URL using the --url argument.")
        sys.exit(1)
    
    main(args.url)
