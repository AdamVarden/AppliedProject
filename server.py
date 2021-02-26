"""
Server Code
"""

from socket import AF_INET, socket, SOCK_STREAM 
from threading import Thread
import tkinter
import pymongo
from datetime import date
from tkinter import *

#Constraints for Server
clients = {}
addresses = {}
fileShareMode = False
HOST = 'localhost'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# Database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["logDatabase"]
mycol = mydb["log"]
today = str(date.today())

def accept_connections():
    #Handles incoming clients
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected. " % client_address)
        client.send(bytes("Welcome to the Room ", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        
        
def handle_client(client):
    # Handles the client that came in
    name = client.recv(BUFSIZ).decode("utf8")
    
    msg = "%s has joined the room!" % name
    client.send(bytes(msg, "utf8"))
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    addToDatabase = {"Name":name, "Address": addresses[client], "Date": today}
    insert = mycol.insert_one(addToDatabase)
    
    while True:
        global fileShareMode
        
        msg = client.recv(BUFSIZ)
        
        if msg != bytes("{quit}", "utf8"):
            
            if msg == bytes("{fileshare}", "utf8"):
                
                print("fileshare alert")
                fileShareAlert = msg
                broadcast(fileShareAlert)
                fileShareMode = True
                
                print("Broast case function called file about to be shared")
                fileSize = client.recv(BUFSIZ)
                print("The filesize:" + str(fileSize))
                file = client.recv(BUFSIZ)
                print("The file: "+ str(file))
                broadcast(file)

            else:
                print("Broadcast a message")
                broadcast(msg, name+": ")
        # When the client leaves
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name,"utf8"))
            break


def broadcast(msg, prefix=""):
    global fileShareMode
    # Prefix is used for the name identification
    for sock in clients:
        if fileShareMode == True:
            sock.send(bytes(msg))
            print("Sent File info ")
            fileShareMode = False
        else:
            sock.send(bytes(prefix,"utf8")+msg)



def refresh():
    #dummyData = ["127.0.0.1","33000"]
    #addToDatabase = {"Name":"Adam", "Address": dummyData, "Date": today}
    #insert = mycol.insert_one(addToDatabase)
    records = mycol.find({},{"Name": 1, "Address": 1, "Date": 1})
    print_name = ''
    print_address = ''
    print_date = ''
    for record in records:
        print_name += str(record["Name"]) + "\n"
        print_address += str(record["Address"]) + "\n"
        print_date += str(record["Date"]) + "\n"
        
    name_label = Label(root, text=print_name)
    name_label.grid(row=3,column=1,columnspan=2)
    
    address_label = Label(root, text=print_address)
    address_label.grid(row=3,column=2,columnspan=2)
    
    date_label = Label(root, text=print_date)
    date_label.grid(row=3,column=3,columnspan=2)     
    
def UI():
    root.title("Server Database")
    refresh()
    retrieveRecords_button = Button(root,  text = "Refresh", command = refresh) 
    retrieveRecords_button.grid(row=1, column=2, columnspan=2, pady=10,padx=10,ipadx=137)
    
    nameTitle_label = Label(root, text="Name")
    nameTitle_label.grid(row=2,column=1,columnspan=2)
    
    addressTitle_label = Label(root, text="Address")
    addressTitle_label.grid(row=2,column=2,columnspan=2)
    
    dateTitle_label = Label(root, text="Visited")
    dateTitle_label.grid(row=2,column=3,columnspan=2)   
    
    
    
    
    tkinter.mainloop() 
    
    
    
    
    
if __name__ == "__main__":
    SERVER.listen(5) # Listens for a max of 5 connections
    print("Waiting for the connection")
    root = Tk()
    root.geometry("370x400")
    UI()
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
 
