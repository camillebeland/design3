from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)
socket_io = SocketIO(app)

def inject(a_robot):
    global robot
    robot = a_robot

def run(port):
    socket_io.run(app, port=port)


@socket_io.on('move')
def robot_setvelocity(data):
    delta_x = int(data['delta_x'])
    delta_y = int(data['delta_y'])
    robot.move(delta_x, delta_y)


@socket_io.on('fetchPosition')
def robot_fetchposition():
    socket_io.emit('position',  {'robotPosition': robot.getpos()})


