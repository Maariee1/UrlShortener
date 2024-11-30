from tkinter import *
from tkinter import ttk
import pyperclip

window = Tk()
window.title("G-URL Shortener")
window.configure(bg="#FBF4C4")
window.geometry("1260x700")

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


# icon = PhotoImage(file='C:\Users\Ciara\Documents\Photo-DSA\cutie.png')
# window.iconphoto(True,icon) #optional for icon

#GENERATE LINK
label = Label(window,
              text='Paste your link below',
              font=('Times New Roman',20,'bold'),
              fg='black',
              bg='#FBF4C4')
label.place(x=350,y=200)

generateLink = Button(window,font =('Times New Roman',15,'bold'), text = 'Generate Link', command = generateLink)
generateLink.config(bg = '#21531C')
generateLink.config(fg = '#FBF4C4')
generateLink.place(x=563,y=290)

pasteText = Button(window, text='PASTE', command = pasteText)
pasteText.place(x=920,y=245)

entry = Entry()
entry.config(font=('Times New Roman',20))
entry.config(bg = '#21531C')
entry.config(fg = 'white')
# entry.insert(0, 'Enter your link here')
entry.config(width = 40)
entry.place(x=350,y=240)

#SHORTENED LINK
label1 = Label(window,
              text='Shortened Link',
              font=('Times New Roman',20,'bold'),
              fg='black',
              bg='#FBF4C4')
label1.place(x=350,y=350)

entry1 = Entry()
entry1.config(font=('Times New Roman',20))
entry1.config(bg = '#21531C')
entry1.config(fg = 'white')
entry1.config(width = 40)
entry1.place(x=350,y=390)

OpenLink = Button(window,font=('Times New Roman',15,'bold'),text = 'Open Shortened Link', command=OpenLink)
OpenLink.config(bg = '#21531C')
OpenLink.config(fg = '#FBF4C4')
OpenLink.place(x=535,y=440)

copyText = Button(window, text='COPY', command = copyText)
copyText.place(x=920,y=392)

# Dropdown menu
label_dropdown = Label(window, 
                       text='Select the number of links to shorten:',
                       font=('Times New Roman', 15, 'bold'),
                       fg='black',
                       bg='#FBF4C4')
label_dropdown.place(x=370, y=500)

dropdown = ttk.Combobox(window, 
                        values=[1, 2, 3], 
                        font=('Times New Roman', 15))
dropdown.current(0)  # Set default value
dropdown.place(x=690, y=500)


window.mainloop()
