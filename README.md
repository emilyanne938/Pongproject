# Pongproject

# To run Code:
# Step 1 ================================================================================
# If you wish to play on multiple computers
#   Get the IP address to use in the pongServer.py
#       To do so, run this command in your terminal
#       $ (Get-NetIPAddress -AddressFamily IPv4 | Where-Object PrefixOrigin -eq 'Manual').IPAddress
#       If two, use the second IP address that the command prompt gives you, else just use 1
#   Edit line 32 and put in number found in above step in the blank
#       serverSocket.bind(("_______", 22258))

# If you just wish to run on your own computer
#   Edit line 32 and put
#       serverSocket.bind(("localhost", 22258))

# Step 2 ================================================================================
# Start the server running
# Run the each client you want to connect with following terminal command (Our code only supports 2) 
#   $ Python3 pongClient.py

# A window should pop up
# Enter IP address found in step 1 or (localhost if running on local matchine) in Server IP field
# Enter 22258 in Server Port field
# Click join

# Do the same for second client connection

# Step 3 ================================================================================
# Begin play 