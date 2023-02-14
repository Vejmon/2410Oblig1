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
meldinger = []

def serverGame(con, meg):
    """
    når vi har to spillere spiller vi rockPaperScissors.
    """
    global online
    global toSpillere

    while toSpillere:
        con.send("venter på en spiller til".encode())
        time.sleep(2.5)
    con.send("nå er vi klare".encode())

    #liker ikke denne løsningen...
    time.sleep(2.5)
    motspiller = meg

    #fjerner de to matchende spillerne fra køen.
    for client in online:
        if client["iKø"] == True and client != meg:
            motspiller = client
            client["iKø"] = False

    #Sender navnet til motspilleren
    con.send(motspiller["navn"].encode())

    deGyldige = [".r",".p",".s",".f"]
    while True:

        mittValg = con.recv(1024).decode()
        meg["valg"] = mittValg
        if mittValg == ".f":
            con.send("kanskje en annen gang :)".encode())
            break

        motspillerValg = motspiller["valg"]

        #venter på den andre hånden
        while motspillerValg not in deGyldige:
            motspillerValg = motspiller["valg"]

        # walkover
        if motspillerValg == ".f":
            con.send("du vant på walkover!".encode())
            break

        # stalemate
        if motspillerValg == mittValg:
            con.send("gosj, likt valg".encode())
            motspiller["valg"] = ""

        elif mittValg == ".p":
            if motspillerValg == ".r":
                con.send("de valgte stein, du vant!".encode())
                break
            elif motspillerValg == ".s":
                con.send("desverre tapte du, de valgte saks".encode())
                break

        elif mittValg == ".r":
            if motspillerValg == ".p":
                con.send("desverre tapte du, de valgte papir".encode())
                break
            elif motspillerValg == ".s":
                con.send("de valgte saks, du vant!".encode())
                break

        elif mittValg == ".s":
            if motspillerValg == ".r":
                con.send("desverre tapte du, de valgte stein".encode())
                break
            elif motspillerValg == ".p":
                con.send("de valgte papir, du vant!".encode())
                break
    motspiller["valg"] = ""
    con.send(".t".encode())

def handleClient(con):
    """
    a client handler function
    """
    global online
    global toSpillere
    global meldinger

    #ber om info fra brukeren
    #og henter variabler fra connection.
    ip, raddr = con.getpeername()
    navn = con.recv(1024).decode()
    if navn == ".f":
        con.close()

    #oppretter en client og setter den inn i de som er "online"
    enClient = {
        "navn": navn,
        "ip": ip,
        "raddr" : raddr,
        "iKø" : False,
        "valg": ""
    }
    online.append(enClient)

    #oppretter en melding om hvem andre som er online
    melding = "Online: "
    for client in online:
        if client != enClient:
            melding += client["navn"] +" fra: " + client["ip"] + ", "
    con.send(melding.encode())

    chatPos = 0
    while True:
        data = con.recv(1024).decode()
        if data == ".g":
            enClient["iKø"] = True
            if not toSpillere:
                toSpillere = True
            else:
                toSpillere = False
            serverGame(con,enClient)

        #avslutter
        elif (data == ".e"):
            online.remove(enClient)
            con.close()
            break

        #legger meldingen i listen over meldinger,hvis den ikke er tom.
        elif data != ".t":
            enMelding  = {
                "id": len(meldinger),
                "navn": enClient["navn"],
                "raddr": enClient["raddr"],
                "mld": data
            }
            meldinger.append(enMelding)
        else:
            mld = ""
            skalUt = range(chatPos,len(meldinger))
            for i in skalUt:
                chatPos += 1
                if meldinger[i]["raddr"] != enClient["raddr"]:
                    mld += meldinger[i]["navn"]+"\n"+meldinger[i]["mld"]+"\n"
            if mld != "":
                con.send(mld.encode())
            else:
                con.send(".t".encode())

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
    serverSocket.listen(9)
    print ('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept()
        print('Server connected by ', addr)
        #connectionSocket
        thread.start_new_thread(handleClient, (connectionSocket,))
    serverSocket.close()

if __name__ == '__main__':
    main()