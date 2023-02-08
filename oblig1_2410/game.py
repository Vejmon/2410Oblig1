
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