"""
    Script for the GUI chat app.
"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog 
import os

HOST = ""
PORT = 33000
ADDR = (HOST, PORT)
BUFSIZ = 1024
userName = ""
filename = ""
fileShareMode = False

client_socket = socket(AF_INET, SOCK_STREAM)

def receive():
    # Handles receiving of messages
    global fileShareMode
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg == "{fileshare}":
                print("The alert: " + msg)
                fileShareMode = True
                
                theFile = client_socket.recv(BUFSIZ)
                #print("The file content " + str(theFile))
                
                with open('receiver', "wb") as f:
                    f.write(theFile)

                        
                fileShareMode = False
            else:
                msg_list.insert(tkinter.END,msg)
            
        except OSError:
            break

def send(event=None):    
    global fileShareMode, filename
    # Handles sending messages
    msg = my_msg.get()
    my_msg.set("") # Clears the input field
    
    if msg == "{quit}":
        client_socket.close()
        root.quit()
        
    # Sending a key word to the server 
    elif msg == "{fileshare}":
        
        print("{fileshare} alert sent ")
        client_socket.send(bytes(msg, "utf8"))
        
        with open(filename, 'rb') as f:
            client_socket.sendfile(f, 0)
            print(f)
        print("File sent")

    else:
        client_socket.send(bytes(msg, "utf8"))


def on_closing(event=None):
    my_msg.set("{quit}")
    send()

def connect():
    global HOST, PORT, userName, ADDR
    
    # ttk.Notebook.select(root, tab2)
    HOST = str(hostEntry.get())
    PORT = int(portEntry.get())
    userName = nameEntry.get()
    ADDR = (HOST, PORT)
    print(HOST,PORT, ADDR)
    
    client_socket.connect(ADDR) 
    client_socket.send(bytes(userName, "utf8"))
    receive_thread = Thread(target=receive)
    receive_thread.start()

# For opening file explorer and getting a file name
def browseFiles(): 
    global filename
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files",  "*.txt*"), ("all files", "*.*"))) 
       
    # Change label contents 
    theFileName.configure(text="File Opened: "+filename) 
    print(filename)

# Notifying the server we are gonna be sending a file
def sendFile():
    my_msg.set("{fileshare}")
    send()
    send()
        
    
root = tkinter.Tk()
root.title("Chat")

# Tabs
tabControl = ttk.Notebook(root)
connnectionTab = ttk.Frame(tabControl)
chatTab = ttk.Frame(tabControl)
fileShareTab = ttk.Frame(tabControl)

tabControl.add(connnectionTab, text='Connect')
tabControl.add(chatTab, text='Chat')
tabControl.add(fileShareTab, text='File Share')

tabControl.pack(expand=1, fill="both")

host = Label(connnectionTab, text="Host")
port = Label(connnectionTab, text="Port")
userName = Label(connnectionTab, text="Name")

hostEntry = Entry(connnectionTab)
portEntry = Entry(connnectionTab)
nameEntry = Entry(connnectionTab)

submit_button=Button(connnectionTab,text = 'Connect', command = connect)

host.pack()
hostEntry.pack()
port.pack()
portEntry.pack()
userName.pack()
nameEntry.pack()
submit_button.pack()


# Opens the Chat
messages_frame = tkinter.Frame(chatTab)
my_msg = tkinter.StringVar()
my_msg.set("Text...")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame,height=20, width=50, yscrollcommand=scrollbar.set)


scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(chatTab, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(chatTab, text="Send", command=send)
send_button.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)


# File Share
theFileName = Label(fileShareTab,  text = "No File Selected", width = 100, height = 4,  fg = "blue") 
fileExpButton = Button(fileShareTab,  text = "Browse Files", command = browseFiles) 
sendFileButton = Button(fileShareTab,  text = "Send File", command = sendFile) 

theFileName.pack()
fileExpButton.pack()
sendFileButton.pack()

tkinter.mainloop()  # Starts GUI execution.
        