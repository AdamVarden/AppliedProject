# Python Chat Room Application
# Adam Varden - G00359605
## Description
This is the repository of my final year project which is a chat room application. Follow the set up and manuals and watch the video in case of any confusion
## Features
This application allows for users to connect to a server using socket programming to be granted entry to a chat room where they can message the other users already in there.

You are also able to send files over these sockets to the other users.
## Set up
### Mongo
Begin by downloading MongoDB Community edition from this link: ``https://www.mongodb.com/try/download/community``

Once downloaded navigate to you this file directory  ``C:\Program Files\MongoDB\Server\4.2\bin`` on your own machine

Open a command prompt in this folder

Then run the following command ``mongod``

### Python Packages
For convenience it is easier to download the anaconda prompt that is provided by anaconda. See link here [Link to anaconda](https://docs.anaconda.com/anaconda/install/)

Once installed run these following commands:

``pip install sockets``

``pip install pymongo``

Once these have been installed successfully we can move onto running the code

## Manuals
1. Download this folder using the zip feature or git clone
2. Using three anaconda prompt navigate to the directory in both
3. For the first prompt simply type ``python server.py``
4. For the second prompt simply type ``python client.py``
4. For the third prompt simply type ``python client.py``
5. Enter the server details into the connect tabs of the clients

The address of the server is:

IP: 127.0.0.1

Port: 33000

## Video
To view the screencast please click on the link below 

[Link to Screencast](https://youtu.be/7A_g4pDnv3M)


