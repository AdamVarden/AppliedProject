"""
Server Code
"""

from socket import AF_INET, socket, SOCK_STREAM 
from threading import Thread
import tkinter
import pymongo
from datetime import date
from tkinter import *
from tkinter import ttk

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
choice = ""

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
    
    records = mycol.find({},{"Name": 1, "Address": 1, "Date": 1}).sort("Date",1)
    print_name = ''
    print_address = ''
    print_date = ''
    for record in records:
        print_name += str(record["Name"]) + "\n"
        print_address += str(record["Address"]) + "\n"
        print_date += str(record["Date"]) + "\n"
        
    name_label = Label(viewDatabaseTab, text=print_name)
    name_label.grid(row=3,column=1,columnspan=2)
    
    address_label = Label(viewDatabaseTab, text=print_address)
    address_label.grid(row=3,column=2,columnspan=2)
    
    date_label = Label(viewDatabaseTab, text=print_date)
    date_label.grid(row=3,column=3,columnspan=2) 



def search():
    searchField = searchEntry.get()
    choice = clicked.get()
    print_name = ''
    print_address = ''
    print_date = ''
    
    
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

def UI():
    global searchEntry, clicked, name_label, address_label,date_label
    root.title("Server")
    
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
    
    


if __name__ == "__main__":
    SERVER.listen(5) # Listens for a max of 5 connections
    print("Waiting for the connection")
    
    root = Tk()
    root.geometry("370x400")
    
    tabControl = ttk.Notebook(root)
    viewDatabaseTab = ttk.Frame(tabControl)
    
    searchTab = ttk.Frame(tabControl)
    tabControl.add(viewDatabaseTab, text='Database')
    tabControl.add(searchTab, text='Search')
    
    tabControl.pack(expand=1, fill="both")
    
    
    UI()
    
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    
    
    

 
