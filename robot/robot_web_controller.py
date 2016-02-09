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
def robot_move():
    delta_x = request.json['delta_x']
    delta_y = request.json['delta_y']
    robot.move(delta_x, delta_y)
    return "OK"

@app.route('/robot/rotate', methods=['POST'])
def robot_rotate():
    raise NotImplementedError("Method unimplemented yet..");
    return "OK"

@socket_io.on('fetchPosition')
def robot_fetchposition():
    socket_io.emit('position',  {'robotPosition': robot.getpos()})
