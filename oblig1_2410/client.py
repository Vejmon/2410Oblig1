
def gyldighet(listen, bokstaven):
    if bokstaven in listen:
        return True
    else:
        return False

def game():
    server_svar = clientSocket.recv(1024).decode()
    while server_svar == "vent":
        print("vi må vente på en motspiller")
        server_svar = clientSocket.recv(1024).decode()
    print("din motspiller er: " + server_svar)

    gyldig = ["r","p","s"]
    valg = input('velg r for rock, p for paper, eller s for scissor.').lower()
    while not gyldighet(gyldig, valg):
        print("prøv igjen")
        valg = input('velg r for rock, p for paper, eller s for scissor.').lower()
        gyldighet(gyldig, valg)
    clientSocket.send(valg.encode())
    print("venter på svar")
    # server svarer med enten 'gratulerer', eller 'taper'
    print(clientSocket.recv(1024).decode())

#thread
from socket import *
import sys
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((serverName,serverPort))
except:
    print("ConnectionError")
    sys.exit()
while True:
    sentence = input('Welcome! Type "broadcast" if you want to broadcast a message or type "game" if you want to play rock, paper, scissor').lower()
    if sentence == "broadcast":
        #vil broadcaste noe
        clientSocket.send(sentence.encode())
    elif sentence == "game":
        #vil spille spill
        clientSocket.send(sentence.encode())
        game()
    elif sentence == "exit":
        break
    else:
        print("Not valid input, try again")

    modifiedSentence = clientSocket.recv(1024)
    print ('From Server:', modifiedSentence.decode())





clientSocket.close()
