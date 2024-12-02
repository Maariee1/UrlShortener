import requests
import os
import pyperclip
import customtkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser  # For opening links in the browser

# Backend: URL Shortener using TinyURL API
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
        payload = {"url": orig_url, "domain": "tinyurl.com"}

        response = requests.post(self.base_url, json=payload, headers=headers)
        data = response.json()

        try:
            if 'data' in data and 'tiny_url' in data['data']:
                short_link = data['data']['tiny_url']
                self.shortened_urls[orig_url] = short_link
            else:
                print(f"Error: {data.get('errors', 'Unknown error occurred.')}")
        except KeyError:
            print("Unexpected error occurred: Missing expected keys in the response.")

    def bulk_shorten(self, urls):
        for url in urls:
            self.shorten_link(url)

    def display_shortened_urls(self):
        if self.shortened_urls:
            with open("URLs.txt", "a") as file:
                for orig_url, short_url in self.shortened_urls.items():
                    file.write(f"{orig_url} -> {short_url}\n")

# Frontend: Tkinter GUI
window = Tk()
window.title("G-URL Shortener")
window.configure(bg="#FBF4C4")
window.geometry("1260x700")

api_key = "Vyf64pu9k3P8aciCbr6ODAZLH22zcpjUBnKSidRDSDBzOb9ZDCCouA9S6tup"
shortener = URLShortener(api_key)

def MainTab():
    for widget in window.winfo_children():
        widget.destroy()

    def generateLink():
        orig_url = entry.get().strip()
        if orig_url:
            shortener.shorten_link(orig_url)
            if orig_url in shortener.shortened_urls:
                short_link = shortener.shortened_urls[orig_url]
                entry1.delete(0, END)
                entry1.insert(0, short_link)
                # pyperclip.copy(short_link)
                # print("Shortened URL copied to clipboard!")
        else:
            entry1.delete(0, END)
            entry1.insert(0, "Please enter a valid URL!")

    def OpenLink():
        short_link = entry1.get().strip()
        if short_link:
            webbrowser.open(short_link)

    def pasteText():
        clipboard_text = pyperclip.paste()
        entry.delete(0, END)
        entry.insert(0, clipboard_text)

    label = customtkinter.CTkLabel(window, font=('Consolas', 17, 'bold'), text='Paste your link below', text_color='black')
    label.place(x=370, y=195)

    generateLinkButton = customtkinter.CTkButton(
        window, font=('Georgia', 20, 'bold'), text='Generate Link',
        corner_radius=300, fg_color='#21531C', text_color='#FBF4C4',
        hover_color='#3D6C38', width=100, height=50, command=generateLink)
    generateLinkButton.place(x=531, y=283)

    pasteButton = customtkinter.CTkButton(
        window, text='PASTE', corner_radius=100, fg_color='#21531C',
        text_color='#FBF4C4', hover_color='#3D6C38', width=45, command=pasteText)
    pasteButton.place(x=920, y=237)

    entry = customtkinter.CTkEntry(
        master=window, placeholder_text="Enter your link here",
        placeholder_text_color='#2B7025', font=('Times New Roman', 20),
        fg_color="#21531C", text_color="white", corner_radius=300,
        width=570, height=50)
    entry.place(x=630, y=250, anchor='center')

    label1 = customtkinter.CTkLabel(window, font=('Consolas', 17, 'bold'), text='Shortened Link', text_color='black')
    label1.place(x=370, y=360)

    entry1 = customtkinter.CTkEntry(
        master=window, font=('Times New Roman', 20), fg_color="#21531C",
        text_color="white", corner_radius=300, width=570, height=50)
    entry1.place(x=630, y=415, anchor='center')

    openLinkButton = customtkinter.CTkButton(
        window, font=('Georgia', 18, 'bold'), text='Open Shortened Link',
        corner_radius=300, fg_color='#21531C', text_color='#FBF4C4',
        hover_color='#3D6C38', width=100, height=48, command=OpenLink)
    openLinkButton.place(x=506, y=448)

    copyButton = customtkinter.CTkButton(
        window, text='COPY', corner_radius=100, fg_color='#21531C',
        text_color='#FBF4C4', hover_color='#3D6C38', width=50,
        command=lambda: pyperclip.copy(entry1.get()))
    copyButton.place(x=920, y=403)

MainTab()
window.mainloop()
