from socket import *
def main():
    server_sd = socket(AF_INET, SOCK_STREAM)
    port = 12000
    server_ip = '127.0.0.1'

    #bind
    server_sd.bind((server_ip, port))

    #activate listening on the socket
    server_sd.listen(1)
    #server waits on accept for connection
    conn_sd, addr = server_sd.accept()

    #read data from the client and print
    recieved_line = conn_sd.recv(1024).decode()
    print(recieved_line)

    #send data back
    conn_sd.send(recieved_line.encode())
    conn_sd.close()
    server_sd.close()

