"""
Server side: open a socket on a port, listen for a message 
from a client, and send an echo reply; 
echoes lines until eof when client closes socket; spawns a 
thread to handle each client connection; threads share global 
memory space with main thread.
"""
from socket import *
import _thread as thread
import time

class Client(thread.Thread):
    def __init__(self,ip,port,connection):
        thread.Thread.__init__(self)
        self.connection=connection
        self.ip=ip
        self.port=port

def now():
    """
    returns the time of day
    """
    return time.ctime(time.time())

def handleClient(connection):
    """
    a client handler function
    """
    while True:
        data = connection.recv(1024).decode() #receives input from server
        print ("received  message = ", data)    #prints the received message
        modified_message= data.lower()      #puts the message to lowercase
        # connection.send(modified_message.encode())
        if modified_message== "broadcast":
            broadcast()
        elif modified_message== "game":
            game()
        elif modified_message == "exit":
            break
    connection.close()


def main():
    """
    creates a server socket, listens for new connections,
    and spawns a new thread whenever a new connection join
    """
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    try:
        serverSocket.bind(('',serverPort))
    except:
        print("Bind failed. Error : ")
    serverSocket.listen(1)
    print ('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept()
        print('Server connected by ', addr)
        print('at ', now())
        thread.start_new_thread(handleClient, (connectionSocket,))

    serverSocket.close()

if __name__ == '__main__':
    main()

antall_spillere = 0
def game(antall_spillere): #allow two clients to play rock,paper, scissors game
    antall_spillere += 1
    #lagre klient 1 og 2, få de til å sende stein, saks eller pair og si hvem som vinner
    if antall_spillere == 1:
        client1=thread.get_ident()
        client1.send("vent må motspiller".encode())
        time.sleep(1)
    else:
        antall_spillere = 0

def broadcast(): #notify everyone when a client joins (except the client who joined)

def messageall(connection):
    msg = connection.recv(1024).decode()
    for client in self.clients :
        client.connection.send(msg)

def sendmessagetoall():
    for client in self.clients :
            client.connection.send(msg)

def sendtoclient():
    for client in self.clients :
        if client.ip == ip and client.port ==port :
            client.connection.send(msg)
