import binascii
import cv2
from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration
from images.images_provider import Images_Provider
import base64
with open("image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

app = Flask(__name__)
socket_io = SocketIO(app)
image_provider = Images_Provider()


def start_server(port):
    socket_io.run(app, port=port)


@socket_io.on('fetchImage')
def some_function():
    socket_io.emit('sentImage',  {'image': str(encoded_string)})

if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('imageapp', 'port'))
    start_server(port)
