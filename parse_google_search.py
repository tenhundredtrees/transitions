import argparse
import requests
from bs4 import BeautifulSoup

def main(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting main search results (titles and descriptions)
        search_results = soup.find_all('div', class_='tF2Cxc')
        for result in search_results:
            title = result.find('h3').text if result.find('h3') else 'No title found'
            link = result.find('a')['href'] if result.find('a') else 'No link found'
            description = result.find('div', class_='IsZvec').text if result.find('div', class_='IsZvec') else 'No description found'

            print(f"Title: {title}")
            print(f"Link: {link}")
            print(f"Description: {description}\n")

    except requests.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Browse a website and extract some information.")
    parser.add_argument("--url", help="The URL of the website to browse.")

    args = parser.parse_args()

    if not args.url:
        print("Please provide a URL using the --url argument.")
        import sys
        sys.exit(1)

    main(args.url)
