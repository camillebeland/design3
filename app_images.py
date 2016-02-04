from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration
from images.images_provider import Images_Provider

app = Flask(__name__)
socket_io = SocketIO(app)
image_provider = Images_Provider()


def start_server(port):
    socket_io.run(app, port=port)


@socket_io.on('fetch-image')
def some_function():
    socket_io.emit('image2',  {'image': image_provider.current_image})

if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('imageapp', 'port'))
    start_server(port)
