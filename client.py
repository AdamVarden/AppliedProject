"""
    Script for the GUI chat app.
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    # Handles receiving of messages
    while True:
        try:
            msg = client_socket.recv(BUFFIZ).decode("utf8")
            msg_list.insert(tkinter.END,MSG)
        except OSError:
            break

def send(event=None):
    # Handles sending messages
    msg = my_msg.get()
    my_msg.set("") # Clears the input field
    client_socket.close()
    if msg == "{quit}":
        client_socket.close()
        top.quit()
        
def on_closing(event=None):
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Text...")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame,height=20, width=50, yscrollcommand=scrollbar.set)

        