from flask import Flask
from flask.ext.socketio import SocketIO
from robot.mock_robot import MockRobot
from configuration import configuration
from flask_cors import *
from flask import request

app = Flask(__name__)

socket_io = SocketIO(app)
CORS(app)
robot = MockRobot()


def start_robot():
    robot.start()


def start_server(port):
    socket_io.run(app, port=port)


@app.route('/robot/move', methods=['POST'])
def robot_move():
    velocity_x = request.json['x']
    velocity_y = request.json['y']
    robot.move(velocity_x, velocity_y)
    return "OK"


@socket_io.on('fetchPosition')
def some_function():
    socket_io.emit('position',  {'robotPosition': robot.pos})

if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('robot', 'port'))
    start_robot()
    start_server(port)
