from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration
import base64
with open("image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

app = Flask(__name__)
socket_io = SocketIO(app)


@socket_io.on('fetchImage')
def some_function():
    socket_io.emit('sentImage',  {'image': str(encoded_string)})


def start_server(port):
    socket_io.run(app, port=port)


if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('baseapp', 'port'))
    start_server(port)
