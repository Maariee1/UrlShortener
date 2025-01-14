import requests 
import os 
import webbrowser  
import re 
from concurrent.futures import ThreadPoolExecutor 

os.system('cls')

def is_valid_url(url):
    
    pattern = re.compile(
        r'^(https?://)?'  
        r'(www\.)?'       
        r'[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}'  
        r'(:[0-9]+)?'     
        r'(/.*)?$'       
    )
    return pattern.match(url) is not None

class URLShortener:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.tinyurl.com/create"
        self.shortened_urls = {}  
        self.invalid_urls = []    

    def shorten_link(self, orig_url):
        if not is_valid_url(orig_url):
            self.invalid_urls.append(orig_url)
            return f"Invalid URL: {orig_url}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "url": orig_url,
            "domain": "tinyurl.com" 
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            data = response.json()

            if 'data' in data and 'tiny_url' in data['data']:
                short_link = data['data']['tiny_url']
                self.shortened_urls[orig_url] = short_link
                return None  
            else:
                error_message = data.get('errors', 'Unknown error occurred.')
                return f"Error for {orig_url}: {error_message}"
        except Exception as e:
            return f"Failed to process {orig_url}: {e}"

    def shorten_links_simultaneously(self, urls):
        # Shorten multiple URLs simultaneously using ThreadPoolExecutor.
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.shorten_link, urls)
        
        for result in results:
            if result:
                print(result)  

        self.display_shortened_urls()

    def display_shortened_urls(self):
        if self.shortened_urls:
            os.makedirs("URL Shortener", exist_ok=True)  
            with open("URL Shortener/URLs.txt", "a") as file:  
                for orig_url, short_url in self.shortened_urls.items():
                    line = f"{orig_url} ==>> {short_url}\n"
                    file.write(line)
            print("\nAll shortened URLs saved to 'URL Shortener/URLs.txt'.")
        else:
            print("\nNo valid URLs were shortened.")

        if self.invalid_urls:
            print("\nInvalid URLs:")
            for url in self.invalid_urls:
                print(f"- {url}")

    def open_all_links(self):
        # Open all shortened links in the default web browser.
        if self.shortened_urls:
            print("\nOpening all shortened links in your default web browser...")
            for short_url in self.shortened_urls.values():
                webbrowser.open(short_url)
        else:
            print("\nNo shortened URLs to open.")

    @staticmethod
    def get_limited_urls():
        # Ask user how many URLs to input with a limit of 3.
        while True:
            try:
                url_count = int(input("Select the number of links to shorten: "))
                if 1 <= url_count <= 3:
                    break
                else:
                    print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        urls = []
        for i in range(url_count):
            url = input(f"Enter URL {i + 1}: ").strip()
            urls.append(url)
        return urls

# Main Execution
if __name__ == "__main__":
    API_KEY = "Vyf64pu9k3P8aciCbr6ODAZLH22zcpjUBnKSidRDSDBzOb9ZDCCouA9S6tup"
    shortener = URLShortener(API_KEY)

    # Input limited URLs
    urls = shortener.get_limited_urls()

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
