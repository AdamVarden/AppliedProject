"""
Server Code
"""

from socket import AF_INET, socket, SOCK_STREAM 
from threading import Thread
import pymongo
from datetime import date

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
    
    while True:
        global fileShareMode
        
        msg = client.recv(BUFSIZ)
        
        if msg != bytes("{quit}", "utf8"):
            
            if msg == bytes("{fileshare}", "utf8"):
                
                print("fileshare alert")
                fileShareAlert = msg

                fileShareMode = True
                print("Broast case function called file about to be shared")
                broadcast(fileShareAlert)
                fileSize = client.recv(BUFSIZ)
                print(fileSize)
                file = client.recv(BUFSIZ)
                broadcast(file)
                fileShareMode = False

            else:
                print("Broadcast a message")
                broadcast(msg, name+": ")
        # When the client leaves
        else:
            client.send(bytes("{quit}", "utf8"))
            #addToDatabase = {"Name":name, "Address": addresses[client], "Date": today}
            #insert = mycol.insert_one(addToDatabase)
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
        else:
            sock.send(bytes(prefix,"utf8")+msg)


if __name__ == "__main__":
    SERVER.listen(5) # Listens for a max of 5 connections
    print("Waiting for the connection")
    #for x in mycol.find():
        #print(x)
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()