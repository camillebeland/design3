from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration

app = Flask(__name__)
socket_io = SocketIO(app)

def inject(robot):
    robot = robot

def run(port):
    socket_io.run(app, port=port)


@socket_io.on('set-velocity')
def robot_setvelocity(data):
    x_velocity = data['x_velocity']
    y_velocity = data['y_velocity']
    robot.set_vel(x_velocity, y_velocity)


@socket_io.on('fetchPosition')
def robot_fetchposition():
    socket_io.emit('position',  {'robotPosition': robot.pos})


