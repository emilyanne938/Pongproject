# =================================================================================================
# Contributing Authors:	    <Emily Behrendsen, Margaret Bacon>
# Email Addresses:          <eabe247@uky.edu, meba293@uky.edu>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
from threading import Thread

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games
 
quit = False
client1gameState = ""
client2gameState = ""

# def status(serverSocket:socket.socket, clientSocket:socket.socket, clientList:list[socket.socket]): 
#     # clientList[0].recv(1024).decode() and clientList[1].recv(1024).decode().
#     strgamestate1 = clientList[0].recv(1024).decode()
#     strgamestate2 = clientList[1].recv(1024).decode()
#     # strgamestate1 = clientSocket.recv(1024).decode()
#     # strgamestate2 = clientSocket.recv(1024).decode()
#     # strgamestate1 = clientList[0].decode()
#     # strgamestate2 = clientList[1]

#     updatedgamestate1 = strgamestate1.split(",")
#     updatedgamestate2 = strgamestate2.split(",")

#     state1 = int(updatedgamestate1[8])
#     state2 = int(updatedgamestate2[8])

#     if state1 > state2:
#         clientSocket.send(strgamestate1.encode())
#     else:
#         clientSocket.send(strgamestate2.encode())


def createServer() -> socket.socket:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    serverSocket.bind(("localhost", 22258))
    
    return serverSocket

def connection(serverSocket:socket.socket, clientSocket:socket.socket, clientList:list[socket.socket]):
    msg = ""
    screenWidth = 640
    screenHeight = 480

    if len(clientList) % 2 == 1:
        playerPaddle = "left"
    else:
        playerPaddle = "right"

    clientSocket.send(str(screenHeight).encode())
    
    check = clientSocket.recv(1024).decode()
    if check == "height_ack":
        clientSocket.send(str(screenWidth).encode())

    check = clientSocket.recv(1024).decode()
    if check == "width_ack":
        clientSocket.send(playerPaddle.encode())

    
    if playerPaddle == "right":
        clientList[0].send(str("go").encode())

    # while True:
    #     handleClient(clientSocket, 2)
    # #clientSocket.send(str(numClients).encode())


def handleClient(clientSocket:socket.socket, clientNum, clientList:list[socket.socket]):
    global client1gameState
    global client2gameState
    while True:
        gamestate = clientSocket.recv(1024).decode()

        if clientNum == 1:
            client1gameState = gamestate.split(",")
        elif clientNum == 2:
            client2gameState = gamestate.split(",")
        else:
            print(f"ERROR: Unexpected client number {clientNum}")

        state1 = int(client1gameState[8])
        state2 = int(client2gameState[8])

        if state1 > state2:
            #clientSocket.send(','.join(client1gameState).encode())
            clientList[0].send(','.join(client1gameState).encode())
            clientList[1].send(','.join(client1gameState).encode())
        else:
            #clientSocket.send(','.join(client2gameState).encode())
            clientList[0].send(','.join(client2gameState).encode())
            clientList[1].send(','.join(client2gameState).encode())


def main():
    serverSocket = createServer()
    serverSocket.listen()
    
    maxplayers = 2
    currentNumClients = 0

    clientList = []

    while not quit:
        
        clientSocket, clientAddress = serverSocket.accept()
        clientList.append(clientSocket)
        msg = clientSocket.recv(1024).decode()
        print(msg)

        if (msg == "Can I play?") and (currentNumClients <= maxplayers):

            # make threads
            currentNumClients += 1

            # thread = Thread(target = connection, args = (serverSocket, clientSocket, clientList))
        
            # thread.start()
            connection(serverSocket, clientSocket, clientList)
            thread1 = Thread(target=handleClient, args=(clientSocket, currentNumClients, clientList))
           
            # thread.start()
            thread1.start()

        
    serverSocket.close()




if __name__ == "__main__" :
    main()

    
    # accept new clients
    # create threads