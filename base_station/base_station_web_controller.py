from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import time
import base_station.logger as logger
from base_station.logger import Logger
from base_station.vision_service import VisionService
from base_station.vision import ShapeDetector

app = Flask(__name__)
CORS(app)


def inject_mock_map(mock_app):
    global app
    app = mock_app


def inject(a_camera, a_refresh_time, the_worldmap):
    global camera, refresh_time, worldmap, logger, vision_service
    camera = a_camera
    refresh_time = a_refresh_time
    worldmap = the_worldmap
    logger = Logger()
    vision_service = VisionService(a_camera, ShapeDetector())


def generate_frame(camera, refresh_time):
    while True:
        time.sleep(refresh_time)
        bytes_frame = camera.get_frame('jpeg').tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytes_frame + b'\r\n\r\n')


def run(host, port):
    logger.info("Starting the base station app at "+str(port))
    app.run(host=host, port=port, threaded=True)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(camera, refresh_time), mimetype='multipart/x-mixed-replace; boundary=frame')

def cell_to_json(cell):
    return {'x': cell.x, 'y':cell.y, 'width':cell.width, 'height':cell.height}


@app.route('/worldmap')
def fetch_worldmap():
    return jsonify({'circles' : worldmap['circles'], 'triangles': worldmap['triangles'],
                    'squares': worldmap['squares'], 'pentagons': worldmap['pentagons']})

@app.route('/robot_position')
def fetch_position():
    robot_position = vision_service.find_robot_position()
    return jsonify(robot_position)

@app.route('/logger/info', methods=['POST'])
def log_info():
    logger.info(request.json['message'])
    return "OK"