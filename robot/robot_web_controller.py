from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)
socket_io = SocketIO(app)


def inject(a_robot):
    global robot
    robot = a_robot


def run(port):
    socket_io.run(app, port=port)


@app.route('/robot/move', methods=['POST'])
#@socket_io.on('setVelocity')
def robot_setvelocity():
    x_velocity = request.json['x']
    y_velocity = request.json['y']
    robot.set_velocity(x_velocity, y_velocity)
    return "OK"


@socket_io.on('fetchPosition')
def robot_fetchposition():
    socket_io.emit('position',  {'robotPosition': robot.getpos()})
