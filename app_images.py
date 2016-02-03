from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration

app = Flask(__name__)
socket_io = SocketIO(app)


def start_server(port):
    socket_io.run(app, port=port)


@socket_io.on('set-velocity')
def robot_move(data):



@socket_io.on('')
def some_function():
    socket_io.emit('position',  {'': })

if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('imagesapp', 'port'))
    start_server(port)
