# =================================================================================================
# Contributing Authors:	    <Emily Behrendsen, Margaret Bacon>
# Email Addresses:          <eabe247@uky.edu, meba293@uky.edu>
# Date:                     <11/15/2023>
# Purpose:                  <Server of the project, allows clients to communicate and etablish connection>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games
 

import socket
from threading import Thread

 
quit = False
client1gameState = ""
client2gameState = ""



# Author:       Emily Behrendsen, Maggie Bacon
# Purpose:      Establish a server clients can connect to
# Pre:           <What preconditions does this method expect to be true? Ex. This method expects the program to be in X state before being called>
#                called from main, The IP port is set correctly
# Post:          <What postconditions are true after this method is called? Ex. This method changed global variable X to Y>
#                Creates and opens a server socket
def createServer() -> socket.socket:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    serverSocket.bind(("localhost", 22258))
    
    return serverSocket




# TODO serverSocket:socket.socket, 
# Author:       Emily Behrendsen, Maggie Bacon
# Purpose:      To assingn left and right paddles, screen height and width,  and get servers to start together
# Pre:           <What preconditions does this method expect to be true? Ex. This method expects the program to be in X state before being called>
#               Server has started, A client has joined the server, they have sent a can I play request and there are less then three clients
# Post:          <What postconditions are true after this method is called? Ex. This method changed global variable X to Y>
#                The two players are have thier paddles, the size of the screen and have started playing the game. 
def connection(serverSocket:socket.socket, clientSocket:socket.socket, clientList:list[socket.socket]):
    msg = ""
    screenWidth = 640
    screenHeight = 480

    # Paddle assingment 
    if len(clientList) % 2 == 1:
        playerPaddle = "left"
    else:
        playerPaddle = "right"

    # Send Screen Height
    clientSocket.send(str(screenHeight).encode())
    
    # Once known that Height is recived, send Width
    check = clientSocket.recv(1024).decode()
    if check == "height_ack":
        clientSocket.send(str(screenWidth).encode())

    # Once known that Width is recived, send player paddle
    check = clientSocket.recv(1024).decode()
    if check == "width_ack":
        clientSocket.send(playerPaddle.encode())

    # The game starts once right paddle has been assigned
    if playerPaddle == "right":
        clientList[0].send(str("go").encode())




# TODO clientSocket:socket.socket,
# Author:       Emily Behrendsen, Maggie Bacon
# Purpose:      To handle Game State synchronization between clients
# Pre:           <What preconditions does this method expect to be true? Ex. This method expects the program to be in X state before being called>
#               Expects the clients have started the game 
# Post:          <What postconditions are true after this method is called? Ex. This method changed global variable X to Y>
#               The game has been played in sync, and there is a winner
def handleClient(clientSocket:socket.socket, clientList:list[socket.socket]):
    global client1gameState
    global client2gameState

    while True:
        # Recive each of the clients game states & split into aray
        client1gameState = clientList[0].recv(1024).decode().split(",")
        client2gameState = clientList[1].recv(1024).decode().split(",")

        # Position 8 holds the sync varaible
        state1 = int(client1gameState[8])
        state2 = int(client2gameState[8])

        if state1 > state2:
            # we use player 2's paddle position
            client1gameState[4] = client2gameState[2]
            client1gameState[5] = client2gameState[3]

            clientList[0].send(','.join(client1gameState).encode())
            clientList[1].send(','.join(client1gameState).encode())
        else:
            # we use player 1's paddle postion 
            client2gameState[4] = client1gameState[2]
            client2gameState[5] = client1gameState[3]

            clientList[0].send(','.join(client2gameState).encode())
            clientList[1].send(','.join(client2gameState).encode())



# Author:       Emily Behrendsen, Maggie Bacon
# Purpose:       <What should this method do>
# Pre:           <What preconditions does this method expect to be true? Ex. This method expects the program to be in X state before being called>
#               The server script was ran
# Post:          <What postconditions are true after this method is called? Ex. This method changed global variable X to Y>
#                The socket is closed, the threads were created and the game had been played all the way though
def main():
    serverSocket = createServer()
    serverSocket.listen()
    
    maxplayers = 2
    currentNumClients = 0
    clientList = []

    while not quit:
        # accpeting new connections
        clientSocket, clientAddress = serverSocket.accept()
        clientList.append(clientSocket)
        msg = clientSocket.recv(1024).decode()
        print(msg)

        # If recived reqest and still allowing players to join, deticate paddles and start game
        if (msg == "Can I play?") and (currentNumClients <= maxplayers):
            currentNumClients += 1

            connection(serverSocket, clientSocket, clientList)
            thread1 = Thread(target=handleClient, args=(clientSocket, clientList))
        
            thread1.start()

        
    serverSocket.close()




if __name__ == "__main__" :
    main()
