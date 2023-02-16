"""
Client side: It connects to the server
and sends a message to everyone
"""

import socket
import select
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverPort = 12000
serverHost = "127.0.0.1"
client_socket.connect((serverHost, serverPort))

while True:
	""" we are going to use a select-based approach here because it will help
	us deal with two inputs (user's input (stdin) and server's messages from socket)
	"""
	inputs = [sys.stdin, client_socket]
	""" read the select documentations - You pass select three lists: the 
	first contains all sockets that you might want to try reading; the 
	second all the sockets you might want to try writing to, and the last 
	(normally left empty) those that you want to check for errors. """

	read_sockets, write_socket, error_socket = select.select(inputs, [], [])

	# we check if the message is either coming from your terminal or
	# from a server
	for socks in read_sockets:
		if socks == client_socket:
			# receive message from client and display it on the server side
			# also handle exceptions here if there is no message from the
			# client, you should exit.
			try:
				message = socks.recv(1024).decode()
			except:
				exit()

			print(message)
		else:
			# takes inputs from the user
			message = sys.stdin.readline()
			# send a message to the server
			client_socket.send(message.encode())

			#avslutter på client siden etter at "exit" er blitt sendt
			if message.strip() == "exit" or len(message) == 1:
				client_socket.close()
				sys.exit()

client_socket.close()
