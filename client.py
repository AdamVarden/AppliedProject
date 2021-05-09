"""
    Script for the GUI chat app.
    G00359605 - Adam Varden

"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog 
import os
# Variables for connecting to server
HOST = ""
PORT = 33000
ADDR = (HOST, PORT)
BUFSIZ = 1024
userName = ""
# File sharing variables
filePath = ""
fileName = ""
fileShareMode = False

client_socket = socket(AF_INET, SOCK_STREAM)

# Receiving messages from server 
def receive():
    # Handles receiving of messages
    global fileShareMode
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            # Entering creation of a file
            if msg == "{fileshare}":
                print("The alert: " + msg)
                fileShareMode = True
                theFileName = client_socket.recv(BUFSIZ)
                theFile = client_socket.recv(BUFSIZ)
                # Writing the file                
                with open(theFileName, "wb") as f:
                    f.write(theFile)
                # Turning file share off
                fileShareMode = False
            # Adding messages to the message list widget
            else:
                msg_list.insert(tkinter.END,msg)
            
        except OSError:
            break

# Sending messages
def send(event=None):    
    global fileShareMode, filePath, fileName
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

        fileName = os.path.basename(filePath)
        print(fileName+" Has been sent")
        client_socket.send(bytes(fileName, "utf8"))
        # Reading the file as bytes and sending them to the server
        with open(filePath, 'rb') as f:
            client_socket.sendfile(f, 0)
            print(f)
        print("File sent")

    else:
        # Sending a regular message
        client_socket.send(bytes(msg, "utf8"))

# When the user closes the GUI
def on_closing(event=None):
    my_msg.set("{quit}")
    send()
# Method for connecting to the database linked to the connect button on the connect tab
def connect():
    global HOST, PORT, userName, ADDR
    
    HOST = str(hostEntry.get())
    PORT = int(portEntry.get())
    userName = nameEntry.get()
    ADDR = (HOST, PORT)
    print(HOST,PORT, ADDR)
    
    client_socket.connect(ADDR) 
    client_socket.send(bytes(userName, "utf8"))
    # Recieving messages thread
    receive_thread = Thread(target=receive)
    receive_thread.start()

# For opening file explorer and getting a file name
def browseFiles(): 
    global filePath
    # Finding a file
    filePath = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files",  "*.txt*"), ("all files", "*.*"))) 
       
    # Change label contents 
    theFileName.configure(text="File Opened: "+filePath) 
    print(filePath)

# Notifying the server we are gonna be sending a file
def sendFile():
    my_msg.set("{fileshare}")
    send()
    send()
        
# Setting up the GUI
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


# File Share Tab widgets
theFileName = Label(fileShareTab,  text = "No File Selected", width = 100, height = 4,  fg = "blue") 
fileExpButton = Button(fileShareTab,  text = "Browse Files", command = browseFiles) 
sendFileButton = Button(fileShareTab,  text = "Send File", command = sendFile) 

theFileName.pack()
fileExpButton.pack()
sendFileButton.pack()

tkinter.mainloop()  # Starts GUI execution.
        