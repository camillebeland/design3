import json
import socket               # Import socket module

def robot_fetch_islands(islands):
     circles = islands["circles"]
     pentagons = islands["pentagons"]
     squares = islands["squares"]
     triangles = islands["triangles"]
     return circles, pentagons, squares, triangles


socket_server = socket.socket()         # Create a socket object
host = socket.gethostname()             # Get local machine name
port = 2000                             # Reserve a port for your service.

socket_server.connect((host, port))
islands_string = socket_server.recv(1024)

islands = json.loads(islands_string.decode('utf-8'))
circles, pentagons, squares, triangles = robot_fetch_islands(islands)

socket_server.close()                     # Close the socket when done