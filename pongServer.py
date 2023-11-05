# =================================================================================================
# Contributing Authors:	    <Emily Behrendsen, Margaret Bacon>
# Email Addresses:          <eabe247@uky.edu, meba293@uky.edu>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

# Create a socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# Bind the socket to a specific IP address and port
serverSocket.bind(("localhost", 8888))

# Put the server socket in a listening state 
serverSocket.listen(5)

clientSocket, clientAddress = serverSocket.accept()

numClients = 0

msg = ""
msg = clientSocket.recv(1024).decode()
print("Client sent: {msg}")

screenWidth = 640
screenHeight = 480

if numClients % 2 == 1:
    playerPaddle = "left"
else:
    playerPaddle = "right"

check = msg.recv(1024).decode

serverSocket.send(screenHeight)

if check == "height_ack":
    serverSocket.send(screenWidth)

if check == "width_ack":
    serverSocket.send(playerPaddle)


clientSocket.close()
serverSocket.close()