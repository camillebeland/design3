import socket
import json

def inject(the_worldmap):
    global worldmap
    worldmap = the_worldmap

    socket_client = socket.socket()         # Create a socket object
    host = socket.gethostname()             # Get local machine name
    port = 2000                             # Reserve a port for your service.
    socket_client.bind((host, port))        # Bind to the port

    socket_client.listen(5)                 # Now wait for client connection.
    while True:
       client, address = socket_client.accept()     # Establish connection with client.
       print('Got connection from', address)
       worldmap_string = json.dumps(worldmap).encode('utf-8')
       client.send(worldmap_string)
       client.close()