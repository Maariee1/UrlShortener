from tkinter import *
from tkinter import ttk
import pyperclip
import customtkinter
import webbrowser  # Import for opening links in a browser
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
    
    label = customtkinter.CTkLabel(
        window,
        font=('Consolas', 20, 'bold'), 
        text='Terms & Conditions Page',
        text_color='black'
    )
    label.place(x=480, y=300)
    
    Back_button1 = customtkinter.CTkButton(
        window,
        font =('Georgia',20,'bold'), 
        text = 'Back',
        corner_radius=300,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=100,
        height=50,
        command=MainTab)
    Back_button1.place(x=960, y=600)
    
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
        
    #Syntax to add image using Pil or pillow
    image = Image.open("GURL LOGO.png")
    image = image.resize((150, 120))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=535, y=595)
    label.image = photo
    
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
        orig_url1 = entry1.get().strip()
        orig_url2 = entry2.get().strip()
        if orig_url1:
            error_message1 = shortener.shorten_link(orig_url1)
        if orig_url2:
            error_message = shortener.shorten_link(orig_url2)
            # Display the shortened URL in the shortened link entry
        if error_message1:
                entry1.delete(0, END)
                entry_shortened1.delete(0, END)
<<<<<<< Updated upstream
                entry_shortened1.insert(0, "Error: Invalid Url")
        if error_message:
                entry2.delete(0, END)
                entry_shortened2.delete(0, END)
                entry_shortened2.insert(0, "Error: Invalid Url")               
=======
                entry_shortened1.insert(0, "Error: Invalid URL.")
        if error_message:
                entry2.delete(0, END)
                entry_shortened2.delete(0, END)
                entry_shortened2.insert(0, "Error: Invalid URL.")             
>>>>>>> Stashed changes
        if orig_url1 in shortener.shortened_urls:
                entry_shortened1.delete(0, END)
                entry_shortened1.insert(0, shortener.shortened_urls[orig_url1])
        if orig_url2 in shortener.shortened_urls:
                entry_shortened2.delete(0, END)
                entry_shortened2.insert(0, shortener.shortened_urls[orig_url2])

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
        text = entry_shortened2.get()
        if text:
            pyperclip.copy(text)
            print("Shortened link copied to clipboard.")
        else:
            print("No shortened link to copy.")

    def OpenLink():
        short_url1 = entry_shortened1.get()
        short_url2 = entry_shortened2.get()

        if short_url1 == "Invalid Url":
            print("Link not valid to open!")
        elif short_url1.strip():
            webbrowser.open(short_url1)
            print(f"Opening link: {short_url1}")

        if short_url2 == "Invalid Url":
            print("Link not valid to open!")
        elif short_url2.strip():
            webbrowser.open(short_url2)
            print(f"Opening link: {short_url2}")

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
        command=lambda: copyText1(entry_shortened1))
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
        command=lambda: copyText2(entry_shortened2))
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