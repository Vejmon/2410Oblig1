from socket import *
import sys
serverName = '84.213.246.185'
serverPort = 12022
clientSocket = socket(AF_INET, SOCK_STREAM)

#skal sjekke om en spiller har gyldig input, de for 5 forsøk.
def gyldig(inn):
    attempt = 0
    deGyldige = [".r",".p",".s",".f"]
    while inn not in deGyldige:
        attempt += 1
        if attempt > 4:
            return False
        inn = input("prøv igjen: ")
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

    motspillerNavn = clientSocket.recv(1024).decode()
    print("")
    print("din motspiller er: " + motspillerNavn)
    print(".r(rock), .p(paper) .s(scissor) eller .f(forfeit)'")
    valg = input('ditt valg: ')

    if gyldig(valg):
        clientSocket.send(valg.encode())
    else:
        print("fo' real?")
        clientSocket.send(".f".encode())


    resultat = clientSocket.recv(1024).decode()
    while resultat[0] == "g":
        print(resultat)
        valg = input('ditt valg: ')
        if gyldig(valg):
            clientSocket.send(valg.encode())
        resultat = clientSocket.recv(1024).decode()
    print(resultat)

try:
    clientSocket.connect((serverName,serverPort))
except:
    print("ConnectionError")
    sys.exit()

#sender vårt eget navn, og får beskjed om hvem som er online
navn = input("hva heter du?: ")
clientSocket.send(navn.encode())
print(clientSocket.recv(1024).decode())

print("skriv '.g' for å spille, '.e' for å forlate oss")
while True:

    sentence = input('melding til folket: ')
    clientSocket.send(sentence.encode())

    #sjekker om brukeren vil spille spill.
    if sentence == ".g":
        clientGame()

    if (sentence == ".e"):
        clientSocket.close()
        break