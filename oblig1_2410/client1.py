from socket import *
import sys
serverName = '192.168.0.2'
serverPort = 12022
clientSocket = socket(AF_INET, SOCK_STREAM)

def clientGame():
    print("vi skal spille")
    svar = clientSocket.recv(1024).decode()
    while svar[0] == "v":
        print(svar)
        svar = clientSocket.recv(1024).decode()
    print(svar)

try:
    clientSocket.connect((serverName,serverPort))
except:
    print("ConnectionError")
    sys.exit()
while True:
    sentence = input('skriv ".g" for å spille spill, eller skriv en melding')
    #sjekker om brukeren vil spille spill.
    if sentence[:1] == ".g":
        clientSocket.send(".g".encode())
        clientGame()
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print ('From Server:', modifiedSentence.decode())
    if (sentence == "exit"):
        break
clientSocket.close()