import time

from flask import Flask, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def inject_mock_map(mock_app):
    global app
    app = mock_app


def inject(a_camera, a_refresh_time, the_worldmap, a_vision_service):
    global camera, refresh_time, worldmap, vision_service
    camera = a_camera
    refresh_time = a_refresh_time
    worldmap = the_worldmap
    vision_service = a_vision_service


def generate_frame(camera, refresh_time):
    while True:
        time.sleep(refresh_time)
        bytes_frame = camera.get_frame('jpeg').tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytes_frame + b'\r\n\r\n')


def run_base_app(host, port):
    app.run(host=host, port=port, threaded=True)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(camera, refresh_time), mimetype='multipart/x-mixed-replace; boundary=frame')

def cell_to_json(cell):
    return {'x': cell.x, 'y':cell.y, 'width':cell.width, 'height':cell.height}


@app.route('/refresh_worldmap', methods=['POST'])
def refresh_worldmap():
    vision_service.build_map()


@app.route('/worldmap')
def fetch_worldmap():
    return jsonify({'circles' : worldmap['circles'], 'triangles': worldmap['triangles'],
                    'squares': worldmap['squares'], 'pentagons': worldmap['pentagons'],
                    'treasures':worldmap['treasures'], 'chargingStation': worldmap['charging-station']})


@app.route('/vision/robot')
def fetch_position():
    robot_position = vision_service.find_robot_position()
    return jsonify(robot_position)


@app.route('/vision/calibration_data', methods=['GET'])
def get_calibration_data():
    data = vision_service.get_calibration_data()
    return jsonify({'pixels_per_meter' : data['pixels_per_meter'], 'table_corners': data['table_contour'].tolist()})