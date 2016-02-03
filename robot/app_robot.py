from flask import Flask
from flask.ext.socketio import SocketIO
from robot import Mock_Robot
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)
robot = Mock_Robot()


def start_robot():
    robot.start()

def start_server(port):
    socket_io.run(app, port=port)

@socket_io.on('move')
def robot_move(data):
    x_velocity = data['x_velocity']
    y_velocity = data['y_velocity']
    robot.move(x_velocity, y_velocity)

@socket_io.on('fetchPosition')
def some_function():
    socket_io.emit('position',  {'robotPosition': robot.pos})

import sys
from getopt import getopt

def main(argv):
    options, args= getopt(argv, 'p:', ['port='])
    port = 5000
    for key, value in options:
        if(key in ('-p', '--port')):
            port = int(value)

    start_robot()
    start_server(port)

if __name__ == '__main__':
    main(sys.argv[1:])
    
    
