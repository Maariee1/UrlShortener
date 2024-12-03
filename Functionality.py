import requests
import os
import webbrowser  # Import for opening links in a browser
from concurrent.futures import ThreadPoolExecutor  # Import for concurrent processing

class URLShortener:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.tinyurl.com/create"
        self.shortened_urls = {}  # Hashmap to store original and shortened URLs

    def shorten_link(self, orig_url):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "url": orig_url.strip(),
            "domain": "tinyurl.com"
        }
        
        response = requests.post(self.base_url, json=payload, headers=headers)
        data = response.json()

        if 'data' in data and 'tiny_url' in data['data']:
            short_link = data['data']['tiny_url']
            self.shortened_urls[orig_url] = short_link  # Store in hashmap
            print(f"Original URL: {orig_url}")
            print(f"Short Link: {short_link}")
        else:
            error_message = data.get('errors', 'Unknown error occurred.')
            print(f"Error shortening URL {orig_url}: {error_message}")

    def shorten_links_simultaneously(self, urls):
        #Shorten multiple URLs simultaneously using ThreadPoolExecutor.
        with ThreadPoolExecutor() as executor:
            executor.map(self.shorten_link, urls)
        self.display_shortened_urls()

    def display_shortened_urls(self):  # .txt file to store the original and shortened URLs
        if self.shortened_urls:
            os.makedirs("URL Shortener", exist_ok=True)  # Ensure the directory exists
            with open("URL Shortener/URLs.txt", "a") as file:  # Append new links
                for orig_url, short_url in self.shortened_urls.items():
                    line = f"{orig_url} ==>> {short_url}\n"
                    file.write(line)
            print("\nAll shortened URLs saved to 'URL Shortener/URLs.txt'.")
        else:
            print("\nNo URLs have been shortened yet.")

    def open_all_links(self):
        # Open all shortened links in the default web browser.
        if self.shortened_urls:
            print("\nOpening all shortened links in your default web browser...")
            for short_url in self.shortened_urls.values():
                webbrowser.open(short_url)
        else:
            print("\nNo shortened URLs to open.")

# Main Execution
if __name__ == "__main__":
    API_KEY = "Vyf64pu9k3P8aciCbr6ODAZLH22zcpjUBnKSidRDSDBzOb9ZDCCouA9S6tup"
    shortener = URLShortener(API_KEY)

    # Input multiple URLs for simultaneous shortening
    print("Enter your URLs separated by spaces, commas, or newlines:")
    input_urls = input()
    # Split the input into individual URLs using space, comma, or newline as delimiters
    urls = [url.strip() for url in input_urls.replace(",", " ").split() if url.strip()]
    
    if urls:
        print(f"\nDetected {len(urls)} URLs. Processing...\n")
        # Shorten URLs simultaneously
        shortener.shorten_links_simultaneously(urls)

        # Ask the user if they want to open all links
        open_choice = input("\nWould you like to open all shortened links in your browser? (yes/no): ").strip().lower()
        if open_choice in ["yes", "y"]:
            shortener.open_all_links()
    else:
        print("No valid URLs detected.")
