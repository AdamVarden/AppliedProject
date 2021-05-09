"""
Server Code
G00359605 - Adam Varden
"""

from socket import AF_INET, socket, SOCK_STREAM 
from threading import Thread
import tkinter
import pymongo
from datetime import date
from tkinter import *
from tkinter import ttk

#Variables Server
clients = {}
addresses = {}
fileShareMode = False
HOST = 'localhost'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# Database Variables
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["logDatabase"]
mycol = mydb["log"]
today = str(date.today())
choice = ""

def accept_connections():
    #Handles incoming clients using a Loop to listen
    while True:
        # Storing the client and clients address to two different lists
        client, client_address = SERVER.accept()
        # Print to the command prompt that a new connection was made
        print("%s:%s has connected. " % client_address)
        client.send(bytes("Welcome to the Room ", "utf8"))
        addresses[client] = client_address
        # Creating new Thread for new Client
        Thread(target=handle_client, args=(client,)).start()
        
        
def handle_client(client):
    # Handles the client that came in
    name = client.recv(BUFSIZ).decode("utf8")
    
    # Sending out a notification to other clients in the chat room 
    msg = "%s has joined the room!" % name
    client.send(bytes(msg, "utf8"))
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    # Adding the client the entered to the database
    addToDatabase = {"Name":name, "Address": addresses[client], "Date": today}
    insert = mycol.insert_one(addToDatabase)
    # A loop for receving messages from the client
    while True:
        global fileShareMode
        # Receive Message
        msg = client.recv(BUFSIZ)
        # Making sure the quit protocol is not received
        if msg != bytes("{quit}", "utf8"):
            # File share protocol
            if msg == bytes("{fileshare}", "utf8"):
                print("fileshare alert")
                # Sending the alert out to the clients
                fileShareAlert = msg
                broadcast(fileShareAlert)
                fileShareMode = True

            # Message broadcast
            else:
                print("Broadcast a chat message")
                broadcast(msg, name+": ")
            # When file share mode is true
            if fileShareMode == True:
                print("Broadcast case function called file about to be shared")
                # Storing the file name and file bytes and broadcasting them
                fileName = client.recv(BUFSIZ)
                file = client.recv(BUFSIZ)
                broadcast(fileName)
                broadcast(file)
                print("The file Name: "+ str(fileName))
                print("The file: "+ str(file))
                
        # When the client leaves
        else:
            client.send(bytes("{quit}", "utf8"))
            # Closing socket
            client.close()
            # Removing the client from the list
            del clients[client]
            # Notifying that someone has left
            broadcast(bytes("%s has left the chat." % name,"utf8"))
            break

# Broadcasting the message over the sockets
# Prefix is used for the name identification
def broadcast(msg, prefix=""):
    global fileShareMode
    # Looping over the client addresses stored in the clients address
    for sock in clients:
        # Used for sending files
        if fileShareMode == True:
            sock.send(bytes(msg))
            print("Sent File info ")
            fileShareMode = False
        # Used for sending messages
        else:
            sock.send(bytes(prefix,"utf8")+msg)


# Refresh method for the Refresh button
def refresh():
    # Using pymongo to retrieve all data from the database and sorting them by date
    records = mycol.find({},{"Name": 1, "Address": 1, "Date": 1}).sort("Date",1)
    # Used for printing names
    print_name = ''
    print_address = ''
    print_date = ''
    # Looping over records data
    for record in records:
        print_name += str(record["Name"]) + "\n"
        print_address += str(record["Address"]) + "\n"
        print_date += str(record["Date"]) + "\n"
    
    # Altering the labels in the UI
    name_label = Label(viewDatabaseTab, text=print_name)
    name_label.grid(row=3,column=1,columnspan=2)
    
    address_label = Label(viewDatabaseTab, text=print_address)
    address_label.grid(row=3,column=2,columnspan=2)
    
    date_label = Label(viewDatabaseTab, text=print_date)
    date_label.grid(row=3,column=3,columnspan=2) 


# Searching the mongo database
def search():
    searchField = searchEntry.get()
    choice = clicked.get()
    print_name = ''
    print_address = ''
    print_date = ''
    
    # Changing the date varaible to match query syntax for mongo
    if choice == "Date (YY-MM-DD)":
        choice = "Date"

    myquery = { str(choice): str(searchField) }

    records = mycol.find(myquery)
    recordCount = records.count()

    # If records is not blank
    if recordCount > 0:
        for record in records:
            print_name += str(record["Name"]) + "\n"
            print_address += str(record["Address"]) + "\n"
            print_date += str(record["Date"]) + "\n"
        name_label.configure(text=print_name)
        address_label.configure(text=print_address)
        date_label.configure(text=print_date)
        

    
    # else the records are blank
    else:
        name_label.configure(text="")
        address_label.configure(text="No Result")
        date_label.configure(text="")

# User interface
def UI():
    global searchEntry, clicked, name_label, address_label,date_label,viewDatabaseTab
    
    # Setting up tkinter
    root = Tk()
    root.geometry("370x400")
    
    # Creating the tabs
    tabControl = ttk.Notebook(root)
    viewDatabaseTab = ttk.Frame(tabControl)
    
    searchTab = ttk.Frame(tabControl)
    tabControl.add(viewDatabaseTab, text='Database')
    tabControl.add(searchTab, text='Search')
    
    tabControl.pack(expand=1, fill="both")
    root.title("Server")
    
    # Retrieving the database contents and adding them to the labels
    refresh()
    retrieveRecords_button = Button(viewDatabaseTab,  text = "Refresh", command = refresh) 
    retrieveRecords_button.grid(row=1, column=2, columnspan=2, pady=10,padx=10,ipadx=137)
    
    nameTitle_label = Label(viewDatabaseTab, text="Name")
    nameTitle_label.grid(row=2,column=1,columnspan=2)
    
    addressTitle_label = Label(viewDatabaseTab, text="Address")
    addressTitle_label.grid(row=2,column=2,columnspan=2)
    
    dateTitle_label = Label(viewDatabaseTab, text="Visited")
    dateTitle_label.grid(row=2,column=3,columnspan=2)   

    # Search tab
    clicked = StringVar()
    clicked.set("Name")
    searchTitle_label = Label(searchTab, text="Search: ")
    searchTitle_label.grid(row=1,column=1,columnspan=2)   
    
    searchEntry = Entry(searchTab)
    searchEntry.grid(row=1,column=4,columnspan=2)  
     
    dropDown = OptionMenu(searchTab, clicked, "Name", "Date (YY-MM-DD)")
    dropDown.grid(row=1,column=6,columnspan=2)
    
    submit_button=Button(searchTab,text = 'Search', command = search)
    submit_button.grid(row=1,column=8,columnspan=1)
    name_label = Label(searchTab, text="")
    name_label.grid(row=4,column=3,columnspan=2)

    address_label = Label(searchTab, text="")
    address_label.grid(row=4,column=5,columnspan=2)

    date_label = Label(searchTab, text="")
    date_label.grid(row=4,column=7,columnspan=2) 

    tkinter.mainloop() 
    
    

# First method ran during execution
if __name__ == "__main__":
    SERVER.listen(5) # Listens for a max of 5 connections
    print("Waiting for the connection")

    # Creating the seperate threads
    GUI_THREAD = Thread(target=UI)
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    GUI_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()