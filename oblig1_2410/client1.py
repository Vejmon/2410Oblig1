import socket
import sys


host = socket.gethostbyname(socket.gethostname()) #Gets IP of your computer
serverPort = 12022
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#skal sjekke om en spiller har gyldig input, de for 5 forsøk.
def gyldig(inn):
    attempt = 0
    deGyldige = ["r","p","s"]
    while inn not in deGyldige:
        attempt += 1
        if attempt > 4:
            return False
        inn = input("prøv igjen")
    return True

#to spillere skal spille stenSaksPapir mot hverandre.
def clientGame():
    print("lykke til :)")

    #vi må forsikre oss om at vi er et par spillere.
    svar = clientSocket.recv(1024).decode()
    while svar[0] == "v":
        print(svar)
        svar = clientSocket.recv(1024).decode()
    print(svar)
    valg = input('skriv: r(rock), p(paper) eller s(scissor)')
    if gyldig(valg):
        clientSocket.send(valg.encode())
    else:
        print("fo' real?")
        clientSocket.send("f".encode())

try:
    clientSocket.connect((host,serverPort))
    print("Vellykket")
except:
    print("ConnectionError")
    sys.exit()

navn = input("hva heter du?: ")
clientSocket.send(navn.encode())
#Si fra til de andre på serveren at "navn har joinet"
while True:
    sentence = input('skriv ".g" for å spille, eller skriv en melding til folket: ')
    #sjekker om brukeren vil spille spill.
    if sentence[:2] == ".g":
        clientSocket.send(".g".encode())
        clientGame()
        clientSocket.send(sentence.encode())
        modifiedSentence = clientSocket.recv(1024)
        print ('From Server:', modifiedSentence.decode())
    elif (sentence == "exit"):
        break
    else:
        clientSocket.send(sentence.encode())
        modifiedSentence = clientSocket.recv(1024)
        print(modifiedSentence.decode())
clientSocket.close()

#skal sjekke om en spiller har gyldig input, de for 5 forsøk.
def gyldig(inn):
    attempt = 0
    deGyldige = ["r","p","s"]
    while inn not in deGyldige:
        attempt += 1
        if attempt > 4:
            return False
        inn = input("prøv igjen")
    return True

#to spillere skal spille stenSaksPapir mot hverandre.
def clientGame():
    print("lykke til :)")

    #vi må forsikre oss om at vi er et par spillere.
    svar = clientSocket.recv(1024).decode()
    while svar[0] == "v":
        print(svar)
        svar = clientSocket.recv(1024).decode()
    print(svar)
    valg = input('skriv: r(rock), p(paper) eller s(scissor)')
    if gyldig(valg):
        clientSocket.send(valg.encode())
    else:
        print("fo' real?")
        clientSocket.send("f".encode())


