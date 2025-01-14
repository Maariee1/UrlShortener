from tkinter import *
from tkinter import ttk, Frame, Scrollbar, Text, Toplevel
from tkinter import messagebox
import webbrowser
import pyperclip
import customtkinter
import pickle
import re
from PIL import Image, ImageTk
from Functionality import URLShortener, is_valid_url  
from colorama import Fore, Style, init
from datetime import datetime
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from flask import Flask, redirect, request
# import requests
init()

# Loads the API key from the pickle file
with open("api_key.pkl", "rb") as file:
    API_KEY = pickle.load(file)

window = Tk()
window.title("G-URL Shortener")
window.configure(bg="#FBF4C4")
window.geometry("1260x700")

shortener = URLShortener(API_KEY)

def MainTab():
    for widget in window.winfo_children():
        widget.destroy()

    connection = sqlite3.connect("Analytics.db")   

    cursor = connection.cursor()

    def generateLink():
        orig_url = entry.get().strip()
        month_key = datetime.now().strftime("%Y-%m")
        daily_key = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if orig_url:
            error_message = shortener.shorten_link(orig_url)
            if error_message:
                entry1.configure(state='normal')  # Temporarily make it editable to insert text
                entry1.delete(0, END)
                entry1.insert(0, "Error: The URL provided is invalid.")
                entry1.configure(text_color="red")  # Make error text red
                entry1.configure(state='readonly')  # Make it readonly again
                print(Fore.RED + "Error: The URL provided is invalid." + Style.RESET_ALL)
                cursor.execute('''
                            INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                            VALUES (?, ?, ?)
                ''',(timestamp, "InvalidUrl", "No output"))
                cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, InvalidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET InvalidUrls = InvalidUrls + 1
                ''',(month_key, daily_key, 1))
                connection.commit()

            elif orig_url in shortener.shortened_urls:
                entry1.configure(state='normal')  # Temporarily make it editable to insert text
                entry1.delete(0, END)
                entry1.insert(0, shortener.shortened_urls[orig_url])
                entry1.configure(text_color="white")
                entry1.configure(state='readonly')  # Make it readonly again
                print(Fore.GREEN + "The URL has been shortened successfully." + Style.RESET_ALL)
                cursor.execute('''
                            INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                            VALUES (?, ?, ?)
                ''',(timestamp, orig_url, " "))
                cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, ValidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET ValidUrls = ValidUrls + 1
                ''',(month_key, daily_key, 1))
                connection.commit()
                shortened_url = entry1.get().strip()
                short_url(shortened_url, timestamp)
                
        else:
            entry1.configure(state='normal')  # Temporarily make it editable to insert text
            entry1.delete(0, END)
            entry1.insert(0, "Error: Please enter a valid URL.")
            entry1.configure(text_color="red")  # Make error text red
            entry1.configure(state='readonly')  # Make it readonly again
            print(Fore.RED + "Error: Please enter a valid URL." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, "InvalidUrl", "No output"))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, InvalidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET InvalidUrls = InvalidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()

    def short_url(shortened_url, timestamp):
        cursor.execute('''
                        UPDATE History
                        SET ShortUrl = ?
                        WHERE Timestamps = ?
                ''',(shortened_url, timestamp))
        connection.commit()

    def copyText():
        text = entry1.get()
        if text and "Error" not in text:
            pyperclip.copy(text)
            entry1.configure(text_color="white")
            print(Fore.GREEN + "The shortened URL has been copied to the clipboard." + Style.RESET_ALL)
        else:
            entry1.configure(text_color="red")  # Keep error messages red
            print(Fore.RED + "Error: There is no valid shortened URL to copy." + Style.RESET_ALL)

    def OpenLink():
        short_url = entry1.get().strip()

        # Check if the URL is valid
        if not short_url or not is_valid_url(short_url):
            entry1.delete(0, END)
            entry1.insert(0, "Error: The URL is invalid or empty.")
            entry1.configure(text_color="red")  # Display error in red in GUI
            print("Error: The URL is invalid or empty.")
            return

        try:
            # Open the short URL in the browser
            webbrowser.open(short_url)
            print(f"Opening link: {short_url}")

            # Connect to the database
            conn = sqlite3.connect('Analytics.db')
            cursor = conn.cursor()

            # Update the clicks count for the short URL
            cursor.execute('''
                INSERT INTO Analytics (ShortUrl, Clicks)
                VALUES (?, 1)
                ON CONFLICT(ShortUrl)
                DO UPDATE SET Clicks = Clicks + 1
            ''', (short_url,))
            conn.commit()

            # Fetch the updated click count
            cursor.execute("SELECT Clicks FROM Analytics WHERE ShortUrl = ?", (short_url,))
            clicks = cursor.fetchone()[0]

            # Display the updated click count in the GUI
            entry1.delete(0, END)
            entry1.insert(0, f"URL opened! Total clicks: {clicks}")
            entry1.configure(text_color="green")
            print(f"Total clicks for {short_url}: {clicks}")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            entry1.delete(0, END)
            entry1.insert(0, "Error: Unable to update clicks.")
            entry1.configure(text_color="red")

        finally:
            if 'conn' in locals():
                conn.close()


#------------------ANALYTICS OR URL------------------------------#  
    def delete_all_history():
        db_path = 'Analytics.db'
        try:
            # Confirmation dialog
            confirm = messagebox.askyesno(
                title="Confirm Delete",
                message="Are you sure you want to delete all history? This action cannot be undone."
            )
            if not confirm:
                return

            # Connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Delete all records from the History table
            cursor.execute("DELETE FROM History")
            conn.commit()

            # Clear the history_table in the UI
            for row in history_table.get_children():
                history_table.delete(row)

            messagebox.showinfo(title="Success", message="All history has been deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            messagebox.showerror(title="Error", message="An error occurred while deleting history.")
        finally:
            if 'conn' in locals():
                conn.close()

    def show_analytics():
        # Create the analytics window

        analytics_window = Toplevel(window)
        analytics_window.title("URL Analytics")
        analytics_window.geometry("1200x700")
        analytics_window.configure(bg="#FBF4C4")

        # Create the main frame
        main_frame = Frame(analytics_window, bg="#FFF3E0", relief="solid", borderwidth=2)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add label for URL History
        history_label = Label(
            main_frame,
            text="URL History and Clicks",
            font=('Georgia', 16, 'bold'),
            bg="#FFF3E0",
            fg="#3E2723"
        )
        history_label.pack(anchor="w", pady=3)

        # Create a frame for URL History table
        history_frame = Frame(main_frame, bg="#FFF3E0", relief="solid", borderwidth=2)
        history_frame.pack(fill="both", expand=True, padx=3, pady=3)

        # Add URL History table
        history_table = ttk.Treeview(
            history_frame,
            columns=("Timestamp", "Long URL", "Short URL", "Clicks"),
            show="headings"
        )
        history_table.heading("Timestamp", text="Timestamp")
        history_table.heading("Long URL", text="Long URL")
        history_table.heading("Short URL", text="Short URL")
        history_table.heading("Clicks", text="Clicks")
        history_table.column("Timestamp", width=200, anchor="center")
        history_table.column("Long URL", width=400, anchor="center")
        history_table.column("Short URL", width=400, anchor="center")
        history_table.column("Clicks", width=100, anchor="center")
        history_table.pack(fill="both", expand=True, pady=3)

        # Fetch data from the database
        db_path = 'Analytics.db'
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Fetch URL History along with click counts
            cursor.execute("""
                SELECT h.Timestamps, h.LongUrl, h.ShortUrl, a.Clicks
                FROM History h
                LEFT JOIN Analytics a ON h.ShortUrl = a.ShortUrl
                ORDER BY h.Timestamps DESC
            """)
            history_data = cursor.fetchall()
            for row in history_data:
                history_table.insert('', 'end', values=row)

        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")

        finally:
            if 'conn' in locals():
                conn.close()

        # Create a frame for Total Shortened URLs table
        total_frame = Frame(main_frame, bg="#FFF3E0", relief="solid", borderwidth=2)
        total_frame.pack(fill="both", expand=True, padx=3, pady=3)

        # Add label for Total Shortened URLs
        total_label = Label(
            total_frame,
            text="Total Shortened URLs",
            font=('Georgia', 16, 'bold'),
            bg="#FFF3E0",
            fg="#3E2723"
        )
        total_label.pack(anchor="w", pady=3)

        # Add Total Shortened URLs table
        total_table = ttk.Treeview(
            total_frame,
            columns=("Daily", "Valid URLs", "Invalid URLs"),
            show="headings"
        )
        total_table.heading("Daily", text="Daily")
        total_table.heading("Valid URLs", text="Valid URLs")
        total_table.heading("Invalid URLs", text="Invalid URLs")
        total_table.column("Daily", width=200, anchor="center")
        total_table.column("Valid URLs", width=300, anchor="center")
        total_table.column("Invalid URLs", width=300, anchor="center")
        total_table.pack(fill="both", expand=True, pady=3)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Fetch Total Shortened URLs for the Daily key
            cursor.execute("SELECT Daily, ValidUrls, InvalidUrls FROM TotalUrlShortened ORDER BY Daily DESC")
            total_data = cursor.fetchall()
            for row in total_data:
                total_table.insert('', 'end', values=row)

        except sqlite3.Error as e:
            print(f"Error fetching total shortened URLs: {e}")

        finally:
            if 'conn' in locals():
                conn.close()


        # Create a frame for buttons
        button_frame = Frame(analytics_window, bg="#FBF4C4")
        button_frame.pack(pady=10)

        # Add Close button
        close_button = customtkinter.CTkButton(
            button_frame,
            text="Close",
            font=('Georgia', 14, 'bold'),
            corner_radius=300,
            fg_color='#21531C',
            text_color='#FBF4C4',
            hover_color='#3D6C38',
            command=analytics_window.destroy
        )
        close_button.pack(side=LEFT, padx=5)

        # Add Graph button
        graph_button = customtkinter.CTkButton(
            button_frame,
            text="View Graphs",
            font=('Georgia', 14, 'bold'),
            corner_radius=300,
            fg_color='#21531C',
            text_color='#FBF4C4',
            hover_color='#3D6C38',
            command=show_graph  # Ensure `show_graph` is defined elsewhere
        )
        graph_button.pack(side=LEFT, padx=5)

        delete_all_button = customtkinter.CTkButton(
            button_frame,
            text="Delete All",
            font=('Georgia', 14, 'bold'),
            corner_radius=300,
            fg_color='#D32F2F',
            text_color='#FBF4C4',
            hover_color='#B71C1C',
            command=delete_all_history
        )
        delete_all_button.pack(side=LEFT, padx=5)

#------------------GRAPH FOR INVALID AND VALID URL PER MONTH------------------------------#      
  
    def show_graph():
        graph_window = Toplevel(window)
        graph_window.title("Valid vs. Invalid URLs")
        graph_window.geometry("1260x700")
        graph_window.configure(bg="#FBF4C4")

        title_label = customtkinter.CTkLabel(
            graph_window,
            text="Valid vs. Invalid URLs",
            font=('Georgia', 28, 'bold'),
            text_color='black'
        )
        title_label.pack(pady=20)

        graph_frame = Frame(graph_window, bg="white", relief="solid", borderwidth=2)
        graph_frame.pack(fill="both", expand=True, padx=20, pady=20)

        db_path = 'Analytics.db'

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Fetch total counts of valid and invalid URLs
            cursor.execute("""
                SELECT 
                    SUM(ValidUrls) AS TotalValid,
                    SUM(InvalidUrls) AS TotalInvalid
                FROM TotalUrlShortened
            """)
            result = cursor.fetchone()

            total_valid = result[0] if result[0] is not None else 0
            total_invalid = result[1] if result[1] is not None else 0

            # Data for the bar chart
            categories = ['Valid URLs', 'Invalid URLs']
            counts = [total_valid, total_invalid]

            # Create the bar chart
            fig = Figure(figsize=(13, 5), dpi=100)

            ax1 = fig.add_subplot(121)  # First subplot for bar chart
            ax1.bar(categories, counts, color=['green', 'red'])
            ax1.set_title("Comparison of Valid and Invalid URLs")
            ax1.set_ylabel("Counts")
            ax1.set_xlabel("URL Types")

            # Fetch daily data for the total URLs shortened per day
            cursor.execute("""
                SELECT strftime('%Y-%m-%d', Daily) AS FormattedDate, 
                    SUM(ValidUrls + InvalidUrls) AS TotalUrls
                FROM TotalUrlShortened
                GROUP BY FormattedDate
                ORDER BY FormattedDate
            """)
            daily_data = cursor.fetchall()

            # Separate the data into dates and total URL counts
            dates = [row[0] for row in daily_data]
            total_urls = [row[1] for row in daily_data]

            # Create the line graph
            ax2 = fig.add_subplot(122)  # Second subplot for line chart
            ax2.plot(dates, total_urls, label='Total URLs Shortened', color='blue', marker='o')
            ax2.set_title("Total URLs Shortened per Day")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Total URLs")
            ax2.legend()

            # Display the graphs
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=15,padx=25)

        except sqlite3.Error as e:
            print(f"Error fetching data from the database: {e}")

        finally:
            if 'conn' in locals():
                conn.close()

        # Close button
        close_button = customtkinter.CTkButton(
            graph_window,
            text="Close",
            font=('Georgia', 14, 'bold'),
            corner_radius=300,
            fg_color='#21531C',
            text_color='#FBF4C4',
            hover_color='#3D6C38',
            command=graph_window.destroy
        )
        close_button.pack(pady=10)
             
    def pasteText():
        clipboard_text = pyperclip.paste()
        entry.delete(0, END)  
        entry.insert(0, clipboard_text)

    def dropdown_selection(event):
        selected_value = dropdown.get()
        if selected_value == '2':
            BlankPage2()
        elif selected_value == '3':
             BlankPage3()

#------------------------------MAIN PAGE----------------------------------#

    image = Image.open("GURL LOGO.png")
    image = image.resize((150, 100))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=545, y=580)
    label.image = photo
    
    image = Image.open("GURL QUOTE.png")
    image = image.resize((1270, 400))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label1 = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label1.pack()
    label1.image = photo
    
    view_analytics_button = customtkinter.CTkButton(
        window,
        font=('Georgia', 12, 'bold'),
        text='View Analytics',
        fg_color='#FBF4C4',
        text_color='#21531C',
        hover='#FBF4C4',
        command=show_analytics
    )
    view_analytics_button.place(x=560, y=560)
    
    #GENERATE LINK
    label = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Paste your link below',
        text_color='black')
    label.place(x=370,y=195)

    generateLink = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = 'Generate Link',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=50, 
        command = generateLink)

    generateLink.place(x=531,y=283)

    pasteText = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=45,
        command=pasteText)
    pasteText.place(x=920,y=237)

    entry = customtkinter.CTkEntry(
        master=window,
        placeholder_text="Enter your link here", 
        placeholder_text_color='#2B7025',
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=570,                                
        height=50,                                
    )
    entry.place(x=630, y=250, anchor='center')

    #SHORTENED LINK
    label1 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Shortened Link',
        text_color='black')
    label1.place(x=370,y=360)

    entry1 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=570,                                
        height=50,
        state='readonly')
    entry1.place(x=630,y=415,anchor='center')

    OpenLink = customtkinter.CTkButton(
        window,
        font =('Georgia',18,'bold'), 
        text = 'Open Shortened Link',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=48, 
        command = OpenLink)
    OpenLink.place(x=506,y=448)

    copyText = customtkinter.CTkButton(
        window,
        text=' COPY ',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=50,
        command=copyText)
    copyText.place(x=920,y=403)

#------------------------------DROP DOWN MENU----------------------------------#
    style = ttk.Style()
    style.theme_use('default')  
    style.configure(
        "Custom.TCombobox",            
        fieldbackground="#21531C",     
        foreground="white",            
        background="#FBF4C4",          
        selectbackground="#21531C",    
        selectforeground="white",     
    )

    label_dropdown = Label(window, 
                        text='Select the number of links to shorten:',
                        font=('Times New Roman', 11,'bold'),
                        fg='black',
                        bg='#FBF4C4')
    label_dropdown.place(x=420, y=528)

    dropdown = ttk.Combobox(window, 
                            values=['--    --', '2', '3'], 
                            font=('Consolas', 10,'bold'),
                            style="Custom.TCombobox")
    dropdown.current(0)  # Set default value
    dropdown.place(x=678, y=530)
    dropdown.bind('<<ComboboxSelected>>', dropdown_selection)

    #ABOUT US BUTTON
    AboutUs = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = ' About Us ',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=50,
        command=AboutUsButton)
    AboutUs.place(x=60, y=600)

    #TERMS AND CONDITION BUTTON
    TermsCondition = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = 'Terms & Condition',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=50,
        command=TermButton)
    TermsCondition.place(x=960, y=600)

#------------------------------TERMS AND CONDITION PAGE----------------------------------#
def TermButton():  
    for widget in window.winfo_children():  # Clear existing widgets
        widget.destroy()
    
    #Quote of GURL    
    image = Image.open("GURL BIG QUOTE.png")
    image = image.resize((500, 200))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=-70, y=30)
    label.image = photo
    
    terms_condition_frame = customtkinter.CTkFrame(window, 
                                            width=1000, 
                                            height=42, 
                                            corner_radius=0, 
                                            fg_color="#21531C")
    terms_condition_frame.place(x=289, y=50)
    
    Label_for_tcf = customtkinter.CTkLabel(terms_condition_frame,
                                           text="TERMS AND CONDITIONS",
                                           text_color="#21531C",
                                           width=290, 
                                           height=60,
                                           corner_radius=50, 
                                           fg_color="#FBF4C4",
                                           font=("Bookman Old Style", 25,'bold'))
    Label_for_tcf.place(relx=0.5, rely=0.5, anchor="center")
    
    label1 = customtkinter.CTkLabel(
        window,
        font=('Consolas', 16, 'bold'), 
        text="These Terms and Conditions represent a legally binding agreement\n"
        "between you (the user) and GURL's Service Provider as you interact with\n"
        "with service. When you make use of “GURL: Turn Long Links, To Quick Links\n"
        "URL Shortener System, you consent to the following terms:",
        text_color="#21531C"
    )
    label1.place(x=450, y=130)
    
    label2 = customtkinter.CTkLabel(
        window,
        font=('Consolas', 16, 'bold'), 
        text="By using the Services, you acknowledge that you have read,\n"
        "understood, and accept all of these Terms and Conditions. Using the\n"
        "services is strictly prohibited if you do not agree to all of these Terms\n"
        "and Conditions, and you must stop using such services right away.",
        text_color="#21531C"
    )
    label2.place(x=305, y=600)
    
    label3 = customtkinter.CTkLabel(
        window,
        font=('Bookman Old Style', 20, 'bold'), 
        text="USER RESPONSIBILITY",
        text_color="#21531C"
    )
    label3.place(x=100, y=250)
    
    label4 = customtkinter.CTkLabel(
        window,
        font=('Bookman Old Style', 20, 'bold'), 
        text="INTELLECTUAL PROPERTY",
        text_color="#21531C"
    )
    label4.place(x=500, y=250)
    
    label5 = customtkinter.CTkLabel(
        window,
        font=('Bookman Old Style', 20, 'bold'), 
        text="TERMINATION OF SERVICES",
        text_color="#21531C"
    )
    label5.place(x=900, y=250)
    
    term1_frame = customtkinter.CTkFrame(window, 
                                            width=350, 
                                            height=280, 
                                            corner_radius=50, 
                                            fg_color="#21531C")
    term1_frame.place(x=45, y=300)
    
    Label_for_term1 = customtkinter.CTkLabel(term1_frame,
                                           text="Avoid abuse, harm, disrupt or\n"
                                           "anything that can cause lag our\n"
                                           "services or systems - for instance by:\n"
                                           " \n"
                                           "1. Spamming, hacking or\n"
                                           "bypassing our systems\n"
                                           " \n"
                                           "2. Uploading viruses, malware,\n"
                                           "or any malicious code",
                                           text_color="#FBF4C4",
                                           justify = 'left',
                                           font=("Bookman Old Style", 16,'bold')) 
    Label_for_term1.place(x=25, y=50)
    
    term2_frame = customtkinter.CTkFrame(window, 
                                            width=350, 
                                            height=280, 
                                            corner_radius=50, 
                                            fg_color="#21531C")
    term2_frame.place(x=465, y=300)
    
    Label_for_term2 = customtkinter.CTkLabel(term2_frame,
                                           text="You own your content, and you\n"
                                           "provide us a limited license that\n"
                                           "allows us to exploit it to achieve the\n"
                                           "purpose of making the service.\n",
                                           text_color="#FBF4C4",
                                           justify = 'center',
                                           font=("Bookman Old Style", 16,'bold')) 
    Label_for_term2.place(x=25, y=100)
    
    term3_frame = customtkinter.CTkFrame(window, 
                                            width=350, 
                                            height=280, 
                                            corner_radius=50, 
                                            fg_color="#21531C")
    term3_frame.place(x=880, y=300)
    
    Label_for_term3 = customtkinter.CTkLabel(term3_frame,
                                           text="GURL reserves the right to terminate\n"
                                           "your access to our services for\n"
                                           "violations of these terms.\n",
                                           text_color="#FBF4C4",
                                           justify = 'center',
                                           font=("Bookman Old Style", 16,'bold')) 
    Label_for_term3.place(x=25, y=110)
    
    Back_button = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = 'Back',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=120,
        height=50,
        command=MainTab)
    Back_button.place(x=100, y=620)
    
    GoTo_AboutUs = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = 'About Us',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=50,
        command=AboutUsButton)
    GoTo_AboutUs.place(x=1025, y=620)
    
#------------------------------ABOUT US PAGE----------------------------------#
def AboutUsButton():  
    for widget in window.winfo_children():  
        widget.destroy()
       
    image = Image.open("GURL BIG QUOTE.png")
    image = image.resize((500, 200))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=360, y=70)
    label.image = photo
    
    image = Image.open("GURL LOGO.png")
    image = image.resize((150, 100))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=545, y=580)
    label.image = photo

    about_us_frame = customtkinter.CTkFrame(window, 
                                            width=350, 
                                            height=80, 
                                            corner_radius=50, 
                                            fg_color="#21531C")
    about_us_frame.place(x=81, y=80)
    Label_for_box = customtkinter.CTkLabel(about_us_frame,
                                           text="About the System",
                                           text_color="#21531C",
                                           width=290, 
                                           height=60,
                                           corner_radius=50, 
                                           fg_color="#FBF4C4",
                                           font=("Bookman Old Style", 25,'bold'))  
    Label_for_box.place(relx=0.5, rely=0.5, anchor="center")

    about_us_frame1 = customtkinter.CTkFrame(window, 
                                            width=350, 
                                            height=80, 
                                            corner_radius=50, 
                                            fg_color="#21531C")
    about_us_frame1.place(x=834, y=80)
    Label_for_box1 = customtkinter.CTkLabel(about_us_frame1,
                                           text="About the Team",
                                           text_color="#21531C",
                                           width=290, 
                                           height=60,
                                           corner_radius=50, 
                                           fg_color="#FBF4C4",
                                           font=("Bookman Old Style", 25,'bold'))  # Optional, to customize font and size
    Label_for_box1.place(relx=0.5, rely=0.5, anchor="center")
    #Left Big Box
    about_us_frame3 = customtkinter.CTkFrame(window, 
                                            width=420, 
                                            height=400, 
                                            corner_radius=50, 
                                            fg_color="#21531C")
    about_us_frame3.place(x=45, y=190)
    #label achuchu left big box
    Label_for_box3 = customtkinter.CTkLabel(about_us_frame3,
                                           text="GURL SHORTENER",
                                           text_color="#FBF4C4",
                                           width=290, 
                                           height=60,
                                           corner_radius=50, 
                                           font=("Bookman Old Style", 25,'bold'))  # Optional, to customize font and size
    Label_for_box3.place(x=50, y=1)
    
    Label_for_box3 = customtkinter.CTkLabel(about_us_frame3,
                                           text="GURL is a powerful yet simple URL shortening tool\n"
                                             "designed to transform long, complicated links into\n"
                                             "concise, shareable ones. It offers a seamless\n"
                                             "solution for quick and efficient navigation, making\n"
                                             "it easier than ever to share links across platforms.\n"
                                             "With GURL, turn long links into quick clicks and\n"
                                             "enhance your online experience with effortless\n"
                                             "accessibility.",
                                           text_color="#FBF4C4",
                                           width=350, 
                                           height=60,
                                           corner_radius=50, 
                                           justify='left',
                                           font=("Bookman Old Style", 14,'bold'))  # Optional, to customize font and size
    Label_for_box3.place(x=0, y=55)
    Label_for_box3 = customtkinter.CTkLabel(about_us_frame3,
                                           text="This system includes additional features such as the \n"
                                             "“About Us” Page, which introduces the team behind \n"
                                             "the project, and the “Terms and Conditions” Page, \n"
                                             "indicating the policies for using the URL shortening \n"
                                             "service. These additional features provide transparency \n"
                                             "and build trust with users. Moreover, a user can enter \n"
                                             "up to 3 URLs, and the system will generate 3 shortened \n"
                                             "links that redirect to each website in their browser.",
                                           text_color="#FBF4C4",
                                           width=350, 
                                           height=60,
                                           corner_radius=50, 
                                           justify='left',
                                           font=("Bookman Old Style", 13,'bold'))  # Optional, to customize font and size
    Label_for_box3.place(x=0, y=220)
    
    #Right Big Box
    about_us_frame4 = customtkinter.CTkFrame(window, 
                                            width=420, 
                                            height=400, 
                                            corner_radius=50, 
                                            fg_color="#21531C")
    about_us_frame4.place(x=800, y=190)
    Label_for_box4 = customtkinter.CTkLabel(about_us_frame4,
                                           text="GROUP - 8",
                                           text_color="#FBF4C4",
                                           width=290, 
                                           height=60,
                                           corner_radius=50, 
                                           font=("Bookman Old Style", 25,'bold'))  # Optional, to customize font and size
    Label_for_box4.place(x=55, y=1)
    Label_for_box4 = customtkinter.CTkLabel(about_us_frame4,
                                           text="We are a team of second-year Information Technology\n"
                                             "students from the Polytechnic University of the\n"
                                             "Philippines, united by our shared passion for \n" 
                                             "technology and innovation. As part of our academic\n"
                                             "journey, we developed GURL - a Generated Uniform\n"
                                             "Resource Locator aimed at providing a simple and\n"
                                             "user-friendly way to shorten and manage URLs.\n"
                                             "    \n"
                                             "We are dedicated to creating a system that enhances\n"
                                             "the browsing experience by making URLs more\n"
                                             "manageable, and accessible. Our system allows users\n"
                                             "to shorten long web addresses, making them easier to\n"
                                             "share on social media, in emails, or for personal use.\n"
                                             "Through this system, we aim to improve efficiency and\n"
                                             "user convenience in managing online resources.\n",
                                           text_color="#FBF4C4",
                                           width=350, 
                                           height=60,
                                           corner_radius=50, 
                                           justify='left',
                                           font=("Bookman Old Style", 13,'bold'))  # Optional, to customize font and size
    Label_for_box4.place(x=0, y=55)
    Label_for_box4 = customtkinter.CTkLabel(about_us_frame4,
                                           text="Meet the team:\n" 
                                             "    Vince Adrian Besa             Bench Brian Bualat\n"
                                             "    Michael Rua Maestre        Ciara Marie Condino\n" 
                                             "    Karl Caya                          Rica  Salespara\n" 
                                             "    Jan Alexa Gonato              Zcintilla Serquiña\n",
                                           text_color="#FBF4C4",
                                           width=350, 
                                           height=60,
                                           corner_radius=50, 
                                           justify='left',
                                           font=("Bookman Old Style", 11,'bold'))  # Optional, to customize font and size
    Label_for_box4.place(x=30, y=310)
    
    #Middle Big Box
    about_us_frame5 = customtkinter.CTkFrame(window, 
                                            width=300, 
                                            height=250, 
                                            corner_radius=50, 
                                            fg_color="#21531C")
    about_us_frame5.place(x=480, y=290)
    Label_for_box5 = customtkinter.CTkLabel(about_us_frame5,
                                            text="If you have any question or concerns,\n"
                                            "you can contact us at:\n"
                                            "\n"
                                            "EMAIL ADDRESS:\n"
                                            "contact.us.gurl@gmail.com\n"
                                            "\n"
                                            "CONTACT NUMBER:\n"
                                            "Phone number: +63 905 521 4699\n",
                                            text_color="#FBF4C4",
                                            width=250, 
                                            height=10,
                                            corner_radius=50, 
                                            justify='left',
                                        font=("Bookman Old Style", 14,'bold'))  # Optional, to customize font and size
    Label_for_box5.place(x=15, y=70)

    Label_for_box6 = customtkinter.CTkLabel(about_us_frame5,
                                            text="CONTACT US:",
                                            text_color="#FBF4C4",
                                            width=150, 
                                            height=10,
                                            corner_radius=50, 
                                            justify='left',
                                        font=("Bookman Old Style", 27,'bold'))  # Optional, to customize font and size
    Label_for_box6.place(x=55, y=20)
    
    Back_button = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = 'Back',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=120,
        height=50,
        command=MainTab)
    Back_button.place(x=185, y=620)
    
    GoTo_Terms = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = 'Terms & Condition',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=50,
        command=TermButton)
    GoTo_Terms.place(x=890, y=620)

connection = sqlite3.connect("Analytics.db")   

cursor = connection.cursor()

def BlankPage2():  
    for widget in window.winfo_children():
        widget.destroy()
        
    #Syntax to add image using Pil or pillow
    image = Image.open("GURL LOGO.png")
    image = image.resize((150, 120))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=535, y=595)
    label.image = photo
    
    # Gurl and quote
    image = Image.open("GURL QUOTE.png")
    image = image.resize((1290, 450))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label1 = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label1.pack()
    label1.image = photo    

    def generateLink():
        orig_urll = entry1.get().strip()
        orig_url = entry2.get().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        month_key = datetime.now().strftime("%Y-%m")
        daily_key = datetime.now().strftime("%Y-%m-%d")

        error_message1 = shortener.shorten_link(orig_urll)
        if error_message1:
            entry_shortened1.configure(state="normal")  # Temporarily enable editing
            entry_shortened1.delete(0, END)
            entry_shortened1.insert(0, "Error: The URL provided is invalid.")
            entry_shortened1.configure(text_color="red")
            entry_shortened1.configure(state="disabled")  # Make read-only
            print(Fore.RED + "Error: The first URL provided is invalid." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, "InvalidUrl", "No output"))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, InvalidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET InvalidUrls = InvalidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()
            
        elif orig_urll in shortener.shortened_urls:
            entry_shortened1.configure(state="normal")  # Temporarily enable editing
            entry_shortened1.delete(0, END)
            entry_shortened1.insert(0, shortener.shortened_urls[orig_urll])
            entry_shortened1.configure(text_color="white")
            entry_shortened1.configure(state="disabled")  # Make read-only
            print(Fore.GREEN + "The first URL has been shortened successfully." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, orig_urll, " "))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, ValidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET ValidUrls = ValidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()
            shortened_url = entry_shortened1.get().strip()
            short_url(shortened_url, timestamp)

        error_message = shortener.shorten_link(orig_url)
        if error_message:
            entry_shortened2.configure(state="normal")  # Temporarily enable editing
            entry_shortened2.delete(0, END)
            entry_shortened2.insert(0, "Error: The URL provided is invalid.")
            entry_shortened2.configure(text_color="red")
            entry_shortened2.configure(state="disabled")  # Make read-only
            print(Fore.RED + "Error: The second URL provided is invalid." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, "InvalidUrl", "No output"))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, InvalidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET InvalidUrls = InvalidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()
            
        elif orig_url in shortener.shortened_urls:
            entry_shortened2.configure(state="normal")  # Temporarily enable editing
            entry_shortened2.delete(0, END)
            entry_shortened2.insert(0, shortener.shortened_urls[orig_url])
            entry_shortened2.configure(text_color="white")
            entry_shortened2.configure(state="disabled")  # Make read-only
            print(Fore.GREEN + "The second URL has been shortened successfully." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, orig_url, " "))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, ValidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET ValidUrls = ValidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()
            shortened_url = entry_shortened2.get().strip()
            short_url2(shortened_url, timestamp)

    def short_url(shortened_url, timestamp):
        cursor.execute('''
                        UPDATE History
                        SET ShortUrl = ?
                        WHERE Timestamps = ?
                ''',(shortened_url, timestamp))
        connection.commit()

    def short_url2(shortened_url, timestamp):
        cursor.execute('''
                        UPDATE History
                        SET ShortUrl = ?
                        WHERE ROWID = (
                        SELECT ROWID
                        FROM History
                        WHERE Timestamps = ? AND ShortUrl IS NOT NULL
                        ORDER BY ROWID ASC
                        LIMIT 1 OFFSET 1
        )
                ''',(shortened_url, timestamp))
        connection.commit()

    def pasteText1(entry1):
        clipboard_text = pyperclip.paste()
        entry1.delete(0, END)
        entry1.insert(0, clipboard_text)

    def pasteText2(entry2):
        clipboard_text = pyperclip.paste()
        entry2.delete(0, END)
        entry2.insert(0, clipboard_text)   

    def copyText1():
        text = entry_shortened1.get()
        if text and "Error" not in text:
            pyperclip.copy(text)
            entry_shortened1.configure(text_color="white")
            print(Fore.GREEN + "The shortened URL has been copied to the clipboard." + Style.RESET_ALL)
        else:
            entry_shortened1.configure(text_color="red")  # Keep error messages red
            print(Fore.RED + "Error: There is no valid shortened URL to copy." + Style.RESET_ALL)

    def copyText2():
        text1 = entry_shortened2.get()
        if text1 and "Error" not in text1:
            pyperclip.copy(text1)
            entry_shortened2.configure(text_color="white")
            print(Fore.GREEN + "The shortened URL has been copied to the clipboard." + Style.RESET_ALL)
        else:
            entry_shortened2.configure(text_color="red")  # Keep error messages red
            print(Fore.RED + "Error: There is no valid shortened URL to copy." + Style.RESET_ALL)
            
    def is_valid_url(url):
        # Regex pattern for validating a URL
        pattern = re.compile(
            r'^(https?://)?'  # http:// or https:// (optional)
            r'(www\.)?'       # www. (optional)
            r'[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}'  # Domain
            r'(:[0-9]+)?'     # Port (optional)
            r'(/.*)?$'        # Path (optional)
        )
        return pattern.match(url) is not None

    # OpenLink1 with URL validation
    def OpenLink():
        short_urll = entry_shortened1.get().strip()  # First link
        short_url = entry_shortened2.get().strip()   # Second link

        # Validate and open the first link
        if not short_urll or not is_valid_url(short_urll):
            entry_shortened1.delete(0, END)
            entry_shortened1.insert(0, "Error: The URL is invalid or empty.")
            entry_shortened1.configure(text_color="red")  # Make the error message red in the GUI
            print(Fore.RED + "Error: The first URL is invalid or empty." + Style.RESET_ALL)
        else:
            webbrowser.open(short_urll)
            print(Fore.GREEN + f"Opening link: {short_urll}" + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO Analytics (ShortUrl, Clicks)
                        VALUES (?, ?)
                        ON CONFLICT(ShortUrl)
                        DO UPDATE SET Clicks = Clicks + 1
            ''',(short_urll, 1))
            connection.commit()

        # Validate and open the second link
        if not short_url or not is_valid_url(short_url):
            entry_shortened2.delete(0, END)
            entry_shortened2.insert(0, "Error: The URL is invalid or empty.")
            entry_shortened2.configure(text_color="red")  # Make the error message red in the GUI
            print(Fore.RED + "Error: The second URL is invalid or empty." + Style.RESET_ALL)
        else:
            webbrowser.open(short_url)
            print(Fore.GREEN + f"Opening link: {short_url}" + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO Analytics (ShortUrl, Clicks)
                        VALUES (?, ?)
                        ON CONFLICT(ShortUrl)
                        DO UPDATE SET Clicks = Clicks + 1
            ''',(short_url, 1))
            connection.commit()

    # FIRST SET OF BOXES
    label1 = customtkinter.CTkLabel(window,
        font=('Consolas', 17, 'bold'),
        text='Paste your link below',
        text_color='black')
    label1.place(x=50, y=215)

    entry1 = customtkinter.CTkEntry(
        master=window,
        placeholder_text="Enter your link here",
        placeholder_text_color='#2B7025',
        font=('Times New Roman', 20),
        fg_color="#21531C",
        text_color="white",
        corner_radius=300,
        width=500,
        height=50
    )
    entry1.place(x=290, y=270, anchor='center')

    paste_btn1 = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',
        text_color='#FBF4C4',
        hover_color='#3D6C38',
        width=45,
        command=lambda: pasteText1(entry1))
    paste_btn1.place(x=550, y=255)

    label_shortened1 = customtkinter.CTkLabel(window,
        font=('Consolas', 17, 'bold'),
        text='Shortened Link',
        text_color='black')
    label_shortened1.place(x=650, y=215)

    entry_shortened1 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),
        fg_color="#21531C",
        text_color="white",
        corner_radius=300,
        width=500,
        height=50)
    entry_shortened1.place(x=890, y=270, anchor='center')

    copy_btn1 = customtkinter.CTkButton(
        window,
        text='COPY',
        corner_radius=100,
        fg_color='#21531C',
        text_color='#FBF4C4',
        hover_color='#3D6C38',
        width=50,
        command=copyText1)
    copy_btn1.place(x=1150, y=255)

    # SECOND SET OF BOXES
    label2 = customtkinter.CTkLabel(window,
        font=('Consolas', 17, 'bold'),
        text='Paste your link below',
        text_color='black')
    label2.place(x=50, y=300)

    entry2 = customtkinter.CTkEntry(
        master=window,
        placeholder_text="Enter your link here",
        placeholder_text_color='#2B7025',
        font=('Times New Roman', 20),
        fg_color="#21531C",
        text_color="white",
        corner_radius=300,
        width=500,
        height=50
    )
    entry2.place(x=290, y=355, anchor='center')

    paste_btn2 = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',
        text_color='#FBF4C4',
        hover_color='#3D6C38',
        width=45,
        command=lambda: pasteText2(entry2))
    paste_btn2.place(x=550, y=340)

    label_shortened2 = customtkinter.CTkLabel(window,
        font=('Consolas', 17, 'bold'),
        text='Shortened Link',
        text_color='black')
    label_shortened2.place(x=650, y=300)

    entry_shortened2 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),
        fg_color="#21531C",
        text_color="white",
        corner_radius=300,
        width=500,
        height=50)
    entry_shortened2.place(x=890, y=355, anchor='center')

    copy_btn2 = customtkinter.CTkButton(
        window,
        text='COPY',
        corner_radius=100,
        fg_color='#21531C',
        text_color='#FBF4C4',
        hover_color='#3D6C38',
        width=50,
        command=copyText2)
    copy_btn2.place(x=1150, y=340)

    # BOTTOM BUTTONS
    generate_btn = customtkinter.CTkButton(
        window,
        font=('Georgia', 20, 'bold'),
        text='Generate Link',
        corner_radius=300,
        fg_color='#21531C',
        text_color='#FBF4C4',
        hover_color='#3D6C38',
        width=150,
        height=50,
        command=generateLink)
    generate_btn.place(x=200, y=500)

    open_link_btn = customtkinter.CTkButton(
        window,
        font=('Georgia', 18, 'bold'),
        text='Open Shortened Link',
        corner_radius=300,
        fg_color='#21531C',
        text_color='#FBF4C4',
        hover_color='#3D6C38',
        width=200,
        height=50,
        command=OpenLink)
    open_link_btn.place(x=780, y=500)

    back_btn = customtkinter.CTkButton(
        window,
        font=('Georgia', 20, 'bold'),
        text='Back',
        corner_radius=300,
        fg_color='#21531C',
        text_color='#FBF4C4',
        hover_color='#3D6C38',
        width=100,
        height=50,
        command=MainTab)
    back_btn.place(x=560, y=570)

connection = sqlite3.connect("Analytics.db")   

cursor = connection.cursor()  
    
def BlankPage3():  
    for widget in window.winfo_children():
        widget.destroy()
    
    #Gurl and quote
    image = Image.open("GURL QUOTE.png")
    image = image.resize((1290, 450))
    photo = ImageTk.PhotoImage(image) 

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label1 = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label1.pack()
    label1.image = photo  

    def generateLink3():      
        orig_url1 = entryP31.get().strip()
        orig_url2 = entryP32.get().strip()
        orig_url3 = entryP33.get().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        month_key = datetime.now().strftime("%Y-%m")
        daily_key = datetime.now().strftime("%Y-%m-%d")

        error_message1 = shortener.shorten_link(orig_url1)
        if error_message1:
            entryC31.configure(state="normal")  # Enable editing
            entryC31.delete(0, END)
            entryC31.insert(0, "Error: The URL provided is invalid.")
            entryC31.configure(text_color="red")  # Make error text red
            entryC31.configure(state="disabled")  # Disable editing
            print(Fore.RED + "Error: The first URL provided is invalid." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, "InvalidUrl", "No output"))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, InvalidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET InvalidUrls = InvalidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()

        elif orig_url1 in shortener.shortened_urls:
            entryC31.configure(state="normal")  # Enable editing
            entryC31.delete(0, END)
            entryC31.insert(0, shortener.shortened_urls[orig_url1])
            entryC31.configure(text_color="white")  
            entryC31.configure(state="disabled")  # Disable editing
            print(Fore.GREEN + "The first URL has been shortened successfully." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, orig_url1, " "))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, ValidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET ValidUrls = ValidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()
            shortened_url1 = entryC31.get().strip()
            short_url1(shortened_url1, timestamp)

        error_message2 = shortener.shorten_link(orig_url2)
        if error_message2:
            entryC32.configure(state="normal")
            entryC32.delete(0, END)
            entryC32.insert(0, "Error: The URL provided is invalid.")
            entryC32.configure(text_color="red")  # Make error text red
            entryC32.configure(state="disabled")
            print(Fore.RED + "Error: The second URL provided is invalid." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, "InvalidUrl", "No output"))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, InvalidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET InvalidUrls = InvalidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()

        elif orig_url2 in shortener.shortened_urls:
            entryC32.configure(state="normal")
            entryC32.delete(0, END)
            entryC32.insert(0, shortener.shortened_urls[orig_url2])
            entryC32.configure(text_color="white")
            entryC32.configure(state="disabled")
            print(Fore.GREEN + "The second URL has been shortened successfully." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, orig_url2, " "))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, ValidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET ValidUrls = ValidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()
            shortened_url2 = entryC32.get().strip()
            short_url2(shortened_url2, timestamp)

        error_message3 = shortener.shorten_link(orig_url3)
        if error_message3:
            entryC33.configure(state="normal")
            entryC33.delete(0, END)
            entryC33.insert(0, "Error: The URL provided is invalid.")
            entryC33.configure(text_color="red")  # Make error text red
            entryC33.configure(state="disabled")
            print(Fore.RED + "Error: The third URL provided is invalid." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, "InvalidUrl", "No output"))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, InvalidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET InvalidUrls = InvalidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()

        elif orig_url3 in shortener.shortened_urls:
            entryC33.configure(state="normal")
            entryC33.delete(0, END)
            entryC33.insert(0, shortener.shortened_urls[orig_url3])
            entryC33.configure(text_color="white")
            entryC33.configure(state="disabled")  
            print(Fore.GREEN + "The third URL has been shortened successfully." + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO History (Timestamps, LongUrl, ShortUrl)
                        VALUES (?, ?, ?)
            ''',(timestamp, orig_url3, " "))
            cursor.execute('''
                            INSERT INTO TotalUrlShortened (Monthly, Daily, ValidUrls)
                            VALUES (?, ?, ?)
                            ON CONFLICT(Daily)
                            DO UPDATE SET ValidUrls = ValidUrls + 1
                ''',(month_key, daily_key, 1))
            connection.commit()
            shortened_url3 = entryC33.get().strip()
            short_url3(shortened_url3, timestamp)


    def short_url1(shortened_url1, timestamp):
        cursor.execute('''
                        UPDATE History
                        SET ShortUrl = ?
                        WHERE Timestamps = ?
                ''',(shortened_url1, timestamp))
        connection.commit()

    def short_url2(shortened_url2, timestamp):
        cursor.execute('''
                        UPDATE History
                        SET ShortUrl = ?
                        WHERE ROWID = (
                        SELECT ROWID
                        FROM History
                        WHERE Timestamps = ? AND ShortUrl IS NOT NULL
                        ORDER BY ROWID ASC
                        LIMIT 1 OFFSET 1
        )
                ''',(shortened_url2, timestamp))
        connection.commit()

    def short_url3(shortened_url3, timestamp):
        cursor.execute('''
                        UPDATE History
                        SET ShortUrl = ?
                        WHERE ROWID = (
                        SELECT ROWID
                        FROM History
                        WHERE Timestamps = ? AND ShortUrl IS NOT NULL
                        ORDER BY ROWID ASC
                        LIMIT 1 OFFSET 2
        )
                ''',(shortened_url3, timestamp))
        connection.commit()

    def pasteText31():
        clipboard_text1 = pyperclip.paste() 
        entryP31.delete(0, END)
        entryP31.insert(0, clipboard_text1)
        
    def pasteText32():
        clipboard_text2 = pyperclip.paste()
        entryP32.delete(0, END)
        entryP32.insert(0, clipboard_text2)  
        
    def pasteText33():
        clipboard_text3 = pyperclip.paste()
        entryP33.delete(0, END)  
        entryP33.insert(0, clipboard_text3)

    def copyText31():
        text1 = entryC31.get()
        if text1 and "Error" not in text1:
            pyperclip.copy(text1)
            entryC31.configure(text_color="white")
            print(Fore.GREEN + "The shortened URL has been copied to the clipboard." + Style.RESET_ALL)
        else:
            entryC31.configure(text_color="red")  # Keep error messages red
            print(Fore.RED + "Error: There is no valid shortened URL to copy." + Style.RESET_ALL)
         
    def copyText32():
        text2 = entryC32.get()
        if text2 and "Error" not in text2:
            pyperclip.copy(text2)
            entryC32.configure(text_color="white")
            print(Fore.GREEN + "The shortened URL has been copied to the clipboard." + Style.RESET_ALL)
        else:
            entryC32.configure(text_color="red")  # Keep error messages red
            print(Fore.RED + "Error: There is no valid shortened URL to copy." + Style.RESET_ALL)       

    def copyText33():
        text3 = entryC33.get()
        if text3 and "Error" not in text3:
            pyperclip.copy(text3)
            entryC33.configure(text_color="white")
            print(Fore.GREEN + "The shortened URL has been copied to the clipboard." + Style.RESET_ALL)
        else:
            entryC33.configure(text_color="red")  # Keep error messages red
            print(Fore.RED + "Error: There is no valid shortened URL to copy." + Style.RESET_ALL)       
        
    def OpenLink3():
        short_url1 = entryC31.get().strip()  # First link
        short_url2 = entryC32.get().strip()  # Second link
        short_url3 = entryC33.get().strip()  # Third link

        # Validate and open the first link
        if not short_url1 or not is_valid_url(short_url1):
            entryC31.delete(0, END)
            entryC31.insert(0, "Error: The URL is invalid or empty.")
            entryC31.configure(text_color="red")  # Make the error message red in the GUI
            print(Fore.RED + "Error: The first URL is invalid or empty." + Style.RESET_ALL)
        else:
            webbrowser.open(short_url1)
            print(Fore.GREEN + f"Opening link: {short_url1}" + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO Analytics (ShortUrl, Clicks)
                        VALUES (?, ?)
                        ON CONFLICT(ShortUrl)
                        DO UPDATE SET Clicks = Clicks + 1
            ''',(short_url1, 1))
            connection.commit()

        # Validate and open the second link
        if not short_url2 or not is_valid_url(short_url2):
            entryC32.delete(0, END)
            entryC32.insert(0, "Error: The URL is invalid or empty.")
            entryC32.configure(text_color="red")  # Make the error message red in the GUI
            print(Fore.RED + "Error: The second URL is invalid or empty." + Style.RESET_ALL)
        else:
            webbrowser.open(short_url2)
            print(Fore.GREEN + f"Opening link: {short_url2}" + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO Analytics (ShortUrl, Clicks)
                        VALUES (?, ?)
                        ON CONFLICT(ShortUrl)
                        DO UPDATE SET Clicks = Clicks + 1
            ''',(short_url2, 1))
            connection.commit()

        # Validate and open the third link
        if not short_url3 or not is_valid_url(short_url3):
            entryC33.delete(0, END)
            entryC33.insert(0, "Error: The URL is invalid or empty.")
            entryC33.configure(text_color="red")  # Make the error message red in the GUI
            print(Fore.RED + "Error: The third URL is invalid or empty." + Style.RESET_ALL)
        else:
            webbrowser.open(short_url3)
            print(Fore.GREEN + f"Opening link: {short_url3}" + Style.RESET_ALL)
            cursor.execute('''
                        INSERT INTO Analytics (ShortUrl, Clicks)
                        VALUES (?, ?)
                        ON CONFLICT(ShortUrl)
                        DO UPDATE SET Clicks = Clicks + 1
            ''',(short_url3, 1))
            connection.commit()
    
    #FIRST PASTE LINK SET
    labelP31 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Paste your link below',
        text_color='black')
    labelP31.place(x=50,y=200)
    
    entryP31 = customtkinter.CTkEntry(
        master=window,
        placeholder_text="Enter your link here", 
        placeholder_text_color='#2B7025',
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50                                 
    )
    entryP31.place(x=290, y=255, anchor='center')
    
    pasteText_btn31 = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=45,
        command= pasteText31)
    pasteText_btn31.place(x=550,y=240)
    
    #SECOND PASTE LINK SET
    label32 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Paste your link below',
        text_color='black')
    label32.place(x=50,y=300)
    
    entryP32 = customtkinter.CTkEntry(
        master=window,
        placeholder_text="Enter your link here", 
        placeholder_text_color='#2B7025',
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50                                 
    )
    entryP32.place(x=290, y=355, anchor='center')
    
    pasteText_btn32 = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=45,
        command= pasteText32)
    pasteText_btn32.place(x=550,y=340)
    
    #THIRD PASTE LINK SET
    label33 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Paste your link below',
        text_color='black')
    label33.place(x=50,y=400)
    
    entryP33 = customtkinter.CTkEntry(
        master=window,
        placeholder_text="Enter your link here", 
        placeholder_text_color='#2B7025',
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50                                 
    )
    entryP33.place(x=290, y=455, anchor='center')
    
    pasteText_btn33 = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=45,
        command= pasteText33)
    pasteText_btn33.place(x=550,y=440)

    generateLink_btn = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = 'Generate Link',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=50, 
        command = generateLink3)
    generateLink_btn.place(x=200,y=550)

    #SHORTENED LINK
    
    #FIRST COPY LINK SET
    labelC31 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Shortened Link',
        text_color='black')
    labelC31.place(x=650,y=200)

    entryC31 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50)
    entryC31.place(x=890,y=255,anchor='center')
    
    copyText_btn31 = customtkinter.CTkButton(
        window,
        text=' COPY ',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=50,
        command= copyText31)
    copyText_btn31.place(x=1150,y=240)
    
    #SECOND COPY LINK SET
    labelC32 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Shortened Link',
        text_color='black')
    labelC32.place(x=650,y=300)

    entryC32 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50)
    entryC32.place(x=890,y=355,anchor='center')
    
    copyText_btn32 = customtkinter.CTkButton(
        window,
        text=' COPY ',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=50,
        command= copyText32)
    copyText_btn32.place(x=1150,y=340)
    
    #THIRD COPY LINK SET
    labelC33 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Shortened Link',
        text_color='black')
    labelC33.place(x=650,y=400)

    entryC33 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50)
    entryC33.place(x=890,y=455,anchor='center')
    
    copyText_btn33 = customtkinter.CTkButton(
        window,
        text=' COPY ',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=50,
        command= copyText33)
    copyText_btn33.place(x=1150,y=440)

    OpenLink_btn = customtkinter.CTkButton(
        window,
        font =('Georgia',18,'bold'), 
        text = 'Open Shortened Link',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=48, 
        command = OpenLink3)
    OpenLink_btn.place(x=780,y=550)

    Back_button = customtkinter.CTkButton(
        window,
        font=('Georgia', 20, 'bold'), 
        text='Back',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=50,
        command=MainTab)
    Back_button.place(x=560, y=620)

MainTab()
    
window.mainloop()
