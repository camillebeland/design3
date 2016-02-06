from flask import Flask, jsonify
from flask.ext.cors import CORS
from flask.ext.socketio import SocketIO
from configuration import configuration
from base_station.camera_service import CameraService


app = Flask(__name__)
CORS(app)
camera_service = CameraService()

@app.route('/', methods=['GET'])
def some_function():
    encoded_string = camera_service.take_picture_base64()
    image = {
        'image': str(encoded_string)
    }
    return jsonify(image), 201



if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('baseapp', 'port'))
    app.run(port=port)
