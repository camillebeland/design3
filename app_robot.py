from flask import Flask
from flask.ext.socketio import SocketIO
from robot.robot import Mock_Robot
from configuration import configuration

app = Flask(__name__)
socket_io = SocketIO(app)
robot = Mock_Robot()


def start_robot():
    robot.start()


def start_server(port):
    socket_io.run(app, port=port)


@socket_io.on('aaa')
def robot_move(velocity):
    print("moving" + x_velocity + y_velocity)
    x_velocity = velocity['x_velocity']
    y_velocity = velocity['y_velocity']
    robot.move(x_velocity, y_velocity)

@socket_io.on('fetchPosition')
def some_function():
    socket_io.emit('position',  {'robotPosition': robot.pos})

if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('robot', 'port'))
    start_robot()
    start_server(port)
