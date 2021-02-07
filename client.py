"""
    Script for the GUI chat app.
"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *
from tkinter import ttk
import os

HOST = ""
PORT = 33000
ADDR = (HOST, PORT)
BUFSIZ = 1024
userName = ""
client_socket = socket(AF_INET, SOCK_STREAM)

def receive():
    # Handles receiving of messages
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END,msg)
            
        except OSError:
            break

def send(event=None):    
    # Handles sending messages
    msg = my_msg.get()
    my_msg.set("") # Clears the input field
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        root.quit()

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

root = tkinter.Tk()
root.title("Chat")

# Tabs
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

host = Label(tab1, text="Host")
port = Label(tab1, text="Port")
userName = Label(tab1, text="Name")

hostEntry = Entry(tab1)
portEntry = Entry(tab1)
nameEntry = Entry(tab1)

submit_button=Button(tab1,text = 'Connect', command = connect)

host.pack()
hostEntry.pack()
port.pack()
portEntry.pack()
userName.pack()
nameEntry.pack()
submit_button.pack()


# Opens the Chat
messages_frame = tkinter.Frame(tab2)
my_msg = tkinter.StringVar()
my_msg.set("Text...")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame,height=20, width=50, yscrollcommand=scrollbar.set)


scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(tab2, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(tab2, text="Send", command=send)
send_button.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)





tkinter.mainloop()  # Starts GUI execution.
        