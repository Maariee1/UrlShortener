from tkinter import *
from tkinter import ttk
import pyperclip
import customtkinter
import webbrowser #For opening link sa website
from PIL import Image, ImageTk

window = Tk()
window.title("G-URL Shortener")
window.configure(bg="#FBF4C4")
window.geometry("1260x700")

def MainTab():
    for widget in window.winfo_children():
        widget.destroy()
        
    def generateLink():
        username = entry.get()
        print('Musta' + username) #INSERT FUNCTIONALITY AND INVALID INPUTS
        
    def copyText():
        text = entry1.get()
        pyperclip.copy(text) 
        
    def OpenLink():
        print('hello') #INSERT FUNCTIONALITY
        
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
            
    # #Syntax to add image using Pil or pillow
    # image = Image.open("GURL BG (2).png")
    # image = image.resize((150, 100))
    # photo = ImageTk.PhotoImage(image)

    # style = ttk.Style()
    # style.configure("Custom.TLabel", background='#FBF4C4')
    # label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    # label.place(x=545, y=580)
    # label.image = photo
    
    # #Gurl and quote
    # image = Image.open("C:\\Users\\Ciara\\Downloads\\GURL BG (6 x 2 in) (1).png")
    # image = image.resize((1270, 400))
    # photo = ImageTk.PhotoImage(image)

    # style = ttk.Style()
    # style.configure("Custom.TLabel", background='#FBF4C4')
    # label1 = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    # label1.pack()
    # label1.image = photo
    
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
    image = Image.open("C:\\Users\\Ciara\\Downloads\\GURL BG (6 x 2 in) (2).png")
    image = image.resize((500, 200))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=360, y=70)
    label.image = photo
    
    #LOGO of GURL    
    image = Image.open("C:\\Users\\Ciara\\PYTHON\\UrlShortener\\GURL BG (2).png")
    image = image.resize((150, 100))
    photo = ImageTk.PhotoImage(image)

    style = ttk.Style()
    style.configure("Custom.TLabel", background='#FBF4C4')
    label = ttk.Label(window, image=photo, style="Custom.TLabel", relief="flat", borderwidth=0)
    label.place(x=545, y=580)
    label.image = photo
    
    # First Upper Left Box in About Us
    about_us_frame = customtkinter.CTkFrame(window, 
                                            width=300, 
                                            height=100, 
                                            corner_radius=50, 
                                            fg_color="#507C4C")
    about_us_frame.place(x=105, y=75)
    
    # #Second Upper Right Box in About Us
    about_us_frame1 = customtkinter.CTkFrame(window, 
                                            width=300, 
                                            height=100, 
                                            corner_radius=50, 
                                            fg_color="#507C4C")
    about_us_frame1.place(x=863, y=75)
    
    #Left Big Box
    about_us_frame3 = customtkinter.CTkFrame(window, 
                                            width=420, 
                                            height=400, 
                                            corner_radius=50, 
                                            fg_color="#507C4C")
    about_us_frame3.place(x=45, y=190)
    
    #Right Big Box
    about_us_frame3 = customtkinter.CTkFrame(window, 
                                            width=420, 
                                            height=400, 
                                            corner_radius=50, 
                                            fg_color="#507C4C")
    about_us_frame3.place(x=800, y=190)
    
    #Middle Big Box
    about_us_frame3 = customtkinter.CTkFrame(window, 
                                            width=300, 
                                            height=250, 
                                            corner_radius=50, 
                                            fg_color="#507C4C")
    about_us_frame3.place(x=480, y=290)
    
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
        
    def generateLink():
        print("Generate functionality to be implemented.")

    def pasteText(entry):
        clipboard_text = pyperclip.paste()
        entry.delete(0, END)
        entry.insert(0, clipboard_text)

    def copyText(entry):
        text = entry.get()
        pyperclip.copy(text)

    def OpenLink():
        print("Open functionality to be implemented.")

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
        command=lambda: pasteText(entry1))
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
        command=lambda: copyText(entry_shortened1))
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
        command=lambda: pasteText(entry2))
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
        command=lambda: copyText(entry_shortened2))
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
        
    def generateLink():
        username = entry.get()
        print('Musta' + username) #INSERT FUNCTIONALITY AND INVALID INPUTS
        
    def pasteText():
        clipboard_text = pyperclip.paste()
        entry.delete(0, END)  
        entry.insert(0, clipboard_text)
    
    def copyText():
        text = entry1.get()
        pyperclip.copy(text) 
        
    def OpenLink():
        print('hello') #INSERT FUNCTIONALITY
        
    #GENERATE LINK
    
    #FIRST PASTE LINK SET
    label = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Paste your link below',
        text_color='black')
    label.place(x=50,y=200)
    
    entry = customtkinter.CTkEntry(
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
    entry.place(x=290, y=255, anchor='center')
    
    pasteText_btn = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=45,
        command= pasteText)
    pasteText_btn.place(x=550,y=240)
    
    #SECOND PASTE LINK SET
    label = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Paste your link below',
        text_color='black')
    label.place(x=50,y=300)
    
    entry = customtkinter.CTkEntry(
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
    entry.place(x=290, y=355, anchor='center')
    
    pasteText_btn = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=45,
        command= pasteText)
    pasteText_btn.place(x=550,y=340)
    
    #THIRD PASTE LINK SET
    label = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Paste your link below',
        text_color='black')
    label.place(x=50,y=400)
    
    entry = customtkinter.CTkEntry(
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
    entry.place(x=290, y=455, anchor='center')
    
    pasteText_btn = customtkinter.CTkButton(
        window,
        text='PASTE',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=45,
        command= pasteText)
    pasteText_btn.place(x=550,y=440)

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
        command = generateLink)
    generateLink_btn.place(x=200,y=550)

    #SHORTENED LINK
    
    #FIRST COPY LINK SET
    label1 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Shortened Link',
        text_color='black')
    label1.place(x=650,y=200)

    entry1 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50)
    entry1.place(x=890,y=255,anchor='center')
    
    copyText_btn = customtkinter.CTkButton(
        window,
        text=' COPY ',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=50,
        command= copyText)
    copyText_btn.place(x=1150,y=240)
    
    #SECOND COPY LINK SET
    label1 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Shortened Link',
        text_color='black')
    label1.place(x=650,y=300)

    entry1 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50)
    entry1.place(x=890,y=355,anchor='center')
    
    copyText_btn = customtkinter.CTkButton(
        window,
        text=' COPY ',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=50,
        command= copyText)
    copyText_btn.place(x=1150,y=340)
    
    #THIRD COPY LINK SET
    label1 = customtkinter.CTkLabel(window,
        font =('Consolas',17,'bold'), 
        text = 'Shortened Link',
        text_color='black')
    label1.place(x=650,y=400)

    entry1 = customtkinter.CTkEntry(
        master=window,
        font=('Times New Roman', 20),             
        fg_color="#21531C",                       
        text_color="white",                       
        corner_radius=300,                         
        width=500,                                
        height=50)
    entry1.place(x=890,y=455,anchor='center')
    
    copyText_btn = customtkinter.CTkButton(
        window,
        text=' COPY ',
        corner_radius=100,
        fg_color='#21531C',  
        text_color='#FBF4C4',  
        hover_color='#3D6C38',
        width=50,
        command= copyText)
    copyText_btn.place(x=1150,y=440)

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
        command = OpenLink)
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