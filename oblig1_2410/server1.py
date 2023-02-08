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

toSpillere = False
online = []

def broadcast(message):         #broadcasts a message to all clients in the clients list 
        for client in online : 
            client.send(message.encode())

def serverGame(con):
    """
    når vi har to spillere spiller vi rockPaperScissors.
    """

    while toSpillere:
        con.send("venter på en spiller til".encode())
        time.sleep(3)
    con.send("vi er klare".encode())
    spillerSvar = con.recv(1024).decode
    

def handleClient(con):
    """
    a client handler function
    """
    global toSpillere
    while True:
        navn = con.recv(1024).decode()
        data = con.recv(1024).decode()
        if data == ".g":
            print("vi vil spille")
            if not toSpillere:
                print("må vente")
                toSpillere = True
            else:
                print("lesgo")
                toSpillere = False
            serverGame(con)
        elif (data == "exit"):
            break
        else:
            broadcast(data)
    con.close()


def main():
    """
    creates a server socket, listens for new connections,
    and spawns a new thread whenever a new connection join
    """
    serverPort = 12022
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
        #connectionSocket.
        thread.start_new_thread(handleClient, (connectionSocket,))
    serverSocket.close()

if __name__ == '__main__':
    main()