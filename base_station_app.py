from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration
from base_station.camera_service import CameraService


app = Flask(__name__)
socket_io = SocketIO(app)
camera_service = CameraService()


@socket_io.on('fetchImage')
def some_function():
    encoded_string = camera_service.take_picture_base64()
    socket_io.emit('sentImage',  {'image': str(encoded_string)})


def start_server(port):
    socket_io.run(app, port=port)


if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('baseapp', 'port'))
    start_server(port)
