import requests
import os
import pyperclip  # Import pyperclip for clipboard functionality

# This code uses the tinyurl API due to some problems using cutt.ly API

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
            "url": orig_url,
            "domain": "tinyurl.com"
        }
        
        response = requests.post(self.base_url, json=payload, headers=headers)
        data = response.json()
        
        print('')

        try:
            if 'data' in data and 'tiny_url' in data['data']:
                short_link = data['data']['tiny_url']
                self.shortened_urls[orig_url] = short_link  # Store in hashmap
                print(f"\nShort Link: {short_link}\n")
                self.offer_copy_to_clipboard(short_link)  # Offer to copy to clipboard
            else:
                print(f"\nError: {data.get('errors', 'Unknown error occurred.')}\n")
        except KeyError:
            print('\nUnexpected Error Occurred: Missing expected keys in the response.\n')

    def bulk_shorten(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        num_of_urls = int(input("Select the number of links to shorten: "))

        for i in range(num_of_urls):
            print(f"\nURL {i + 1}:")
            link = input("Paste your link here: ")
            self.shorten_link(link)

        self.display_shortened_urls()

    def display_shortened_urls(self):  # .txt file to store the original and shortened URLs
        if self.shortened_urls:
            with open("URL Shortener/URLs.txt", "a") as file:  # "a" stands for append, if "w" the newer inputs just overwrite the previous inputs by the user 
                for orig_url, short_url in self.shortened_urls.items():
                    line = f"{orig_url} ==>> {short_url}\n"
                    file.write(line)
        else:
            print("\nNo URLs have been shortened yet.")

    def offer_copy_to_clipboard(self, short_url):
        """Offer the user an option to copy the shortened URL to the clipboard."""
        copy_choice = input("Do you want to copy the short link to the clipboard? (y/n): ").strip().lower()
        if copy_choice == 'y':
            self.copy_to_clipboard(short_url)
            print("The short link has been copied to the clipboard.")
        else:
            print("Copying skipped.")

    def copy_to_clipboard(self, short_url):
        """Copy the shortened URL to the clipboard."""
        pyperclip.copy(short_url)

# Main Execution
if __name__ == "__main__":
    API_KEY = "Vyf64pu9k3P8aciCbr6ODAZLH22zcpjUBnKSidRDSDBzOb9ZDCCouA9S6tup"
    shortener = URLShortener(API_KEY)
    shortener.bulk_shorten()
