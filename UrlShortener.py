from tkinter import *
from tkinter import ttk
import webbrowser
import pyperclip
import customtkinter
from webbrowser import open as open_browser
import re
from PIL import Image, ImageTk
from Functionality import URLShortener

window = Tk()
window.title("G-URL Shortener")
window.configure(bg="#FBF4C4")
window.geometry("1260x700")

API_KEY = "Vyf64pu9k3P8aciCbr6ODAZLH22zcpjUBnKSidRDSDBzOb9ZDCCouA9S6tup"
shortener = URLShortener(API_KEY)

def MainTab():
    for widget in window.winfo_children():
        widget.destroy()
        
    def generateLink():
        orig_url = entry.get().strip()
        if orig_url:
            error_message = shortener.shorten_link(orig_url)
            # Display the shortened URL in the shortened link entry
            if error_message:
                entry1.delete(0, END)
                entry1.insert(0, "Error: Invalid URL.")
            elif orig_url in shortener.shortened_urls:
                entry1.delete(0, END)
                entry1.insert(0, shortener.shortened_urls[orig_url])
        else:
            entry1.delete(0, END)
            entry1.insert("Please enter a valid URL.")
        
    def copyText():
        text = entry1.get()
        if text:
            pyperclip.copy(text)
            print("Shortened link copied to clipboard.")
        else:
            print("No shortened link to copy.")
        
    def OpenLink():
        short_url = entry1.get()
        if short_url.strip():
            webbrowser.open(short_url)
            print(f"Opening link: {short_url}")
        else:
            print("No shortened link to open.")
        
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
            
    #Syntax to add image using Pil or pillow
    image = Image.open("GURL LOGO.png")
    image = image.resize((150, 100))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=545, y=580)
    label.image = photo
    
    #Gurl and quote
    image = Image.open("GURL QUOTE.png")
    image = image.resize((1270, 400))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label1 = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label1.pack()
    label1.image = photo
    
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
        height=50                                 
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
        height=50)
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

    # DROPDOWN MENU
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
    
#NEXT PAGE FOR TERMS AND CONDITION
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
    
#NEXT PAGE FOR ABOUT US
def AboutUsButton():  
    for widget in window.winfo_children():  # Clear existing widgets
        widget.destroy()
    
    #Quote of GURL    
    image = Image.open("GURL BIG QUOTE.png")
    image = image.resize((500, 200))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=360, y=70)
    label.image = photo
    
    #LOGO of GURL    
    image = Image.open("GURL LOGO.png")
    image = image.resize((150, 100))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=545, y=580)
    label.image = photo
    
    # First Upper Left Box in About Us
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
                                           font=("Bookman Old Style", 25,'bold'))  # Optional, to customize font and size
    Label_for_box.place(relx=0.5, rely=0.5, anchor="center")
           
    # #Second Upper Right Box in About Us
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
                                             "    Michael Maestre               Ciara Marie Condino\n" 
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

def BlankPage2():  
    for widget in window.winfo_children():
        widget.destroy()
        
    # #Syntax to add image using Pil or pillow
    # image = Image.open("GURL LOGO.png")
    # image = image.resize((150, 120))
    # photo = ImageTk.PhotoImage(image)

    # style = ttk.Style()
    # style.configure("Custom.TLabel", background='#FBF4C4')
    # label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    # label.place(x=535, y=595)
    # label.image = photo
    
    #Gurl and quote
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
        if orig_urll:
            error_message1 = shortener.shorten_link(orig_urll)
        if orig_url:
            error_message = shortener.shorten_link(orig_url)
            # Display the shortened URL in the shortened link entry
        if error_message1:
                entry1.delete(0, END)
                entry_shortened1.delete(0, END)
                entry_shortened1.insert(0, f"Error: Invalid URL.")
        if error_message:
                entry2.delete(0, END)
                entry_shortened2.delete(0, END)
                entry_shortened2.insert(0, f"Error: Invalid URL.")               
        if orig_urll in shortener.shortened_urls:
                entry_shortened1.delete(0, END)
                entry_shortened1.insert(0, shortener.shortened_urls[orig_urll])
        if orig_url in shortener.shortened_urls:
                entry_shortened2.delete(0, END)
                entry_shortened2.insert(0, shortener.shortened_urls[orig_url])

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
        if text:
            pyperclip.copy(text)
            print("Shortened link copied to clipboard.")
        else:
            print("No shortened link to copy.")

    def copyText2():
        text1 = entry_shortened2.get()
        if text1:
            pyperclip.copy(text1)
            print("Shortened link copied to clipboard.")
        else:
            print("No shortened link to copy.")
            
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
        short_urll = entry_shortened1.get().strip()  

        if not short_urll or not is_valid_url(short_urll):
            print("First link is invalid or empty.")
        else:
            open_browser(short_urll)
            print(f"Opening link: {short_urll}")
            
        short_url = entry_shortened2.get().strip()  

        # Validate the URL
        if not short_url or not is_valid_url(short_url):
            print("Second link is invalid or empty.")
        else:
            open_browser(short_url)
            print(f"Opening link: {short_url}")

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
        username = entryP31.get(), entryP32.get(), entryP33.get()
        print('Musta' + username) #INSERT FUNCTIONALITY AND INVALID INPUTS
        
    def pasteText31():
        clipboard_text = pyperclip.paste()
        entryP31.delete(0, END)  
        entryP31.insert(0, clipboard_text)
        
    def pasteText32():
        clipboard_text = pyperclip.paste()
        entryP32.delete(0, END)  
        entryP32.insert(0, clipboard_text)
        
    def pasteText33():
        clipboard_text = pyperclip.paste()
        entryP33.delete(0, END)  
        entryP33.insert(0, clipboard_text)
    
    def copyText31():
        text = entryC31.get()
        pyperclip.copy(text)
         
    def copyText32():
        text = entryC32.get()
        pyperclip.copy(text) 
    
    def copyText33():
        text = entryC33.get()
        pyperclip.copy(text) 
        
    def OpenLink3():
        print('hello') #INSERT FUNCTIONALITY
        
    
    #GENERATE LINK
    
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
