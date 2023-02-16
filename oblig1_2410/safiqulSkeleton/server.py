"""
Server side: it simultaneously handles multiple clients
and broadcast when a client new client joins or a client
sends a message.
"""
import socket
from socket import *
import _thread as thread
import time
import sys


# this is to keep all the newly joined connections!
all_client_connections = []


def now():
	"""
	returns the time of day
	"""
	return time.ctime(time.time())


def handleClient(connection, addr):
	"""
	a client handler function 
	"""
	#motd to new user, with online users.
	msg = "Welcome!\nOnline users: "
	for client in all_client_connections:
		msg += format(client.getpeername()) + ", "
	connection.send(msg.encode())

	#add the new user to list of connected users
	all_client_connections.append(connection)		# Appends the new connection to the list off all clients
	#newJoin = f"{addr} has just joined"		# Message to inform others that a new client has joined
	broadcast(connection, "--has joined--", addr)		# Broadcast the join-message

	while True:
		message = connection.recv(2048).decode()		# Recieve the message from client
		print(now() + " " + str(addr) + "#  ", message)

		# Close connection if client sends exit or there isn't a message
		if message.strip() == "exit" or len(message) == 1 or not message:
			break
		else:
			# broadcast this message to the others
			broadcast(connection, message, addr)
	broadcast(connection, "--has left--", addr)
	connection.close()
	all_client_connections.remove(connection)


def broadcast(connection, message, addr):
	print("Broadcasting")
	utMessage = "\n" + now() + f" {addr}: \n" + message
	for client in all_client_connections:		# Broadcast the message to everyone except the client who sent it
		if client != connection:
			client.send(utMessage.encode())


def main():
	"""
	creates a server socket, listens for new connections,
	and spawns a new thread whenever a new connection join
	"""
	serverPort = 12000
	serverSocket = socket(AF_INET, SOCK_STREAM)
	try:
		serverSocket.bind(('', serverPort))		# Binding
	except:
		print("Bind failed. Error : ")
		sys.exit()
	serverSocket.listen(10)		# Listen for connections
	print('The server is ready to receive')
	while True:
		connectionSocket, addr = serverSocket.accept()   # accept a connection

		print('Server connected by ', addr) 
		print('at ', now())
		thread.start_new_thread(handleClient, (connectionSocket,addr))		# Start a new thread for the connection
	serverSocket.close()


if __name__ == '__main__':
	main()
