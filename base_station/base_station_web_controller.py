from flask import Flask, Response, jsonify
from flask_cors import CORS
import time
from base_station.logger import Logger

app = Flask(__name__)
CORS(app)


def inject_mock_map(mock_app):
    global app
    app = mock_app

def inject(a_camera, a_refresh_time, the_worldmap):
    global camera, refresh_time, worldmap, logger
    camera = a_camera
    refresh_time = a_refresh_time
    worldmap = the_worldmap
    logger = Logger()


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


@app.route('/mesh')
def mesh():
    return jsonify(mesh_to_json(mesh))


def mesh_to_json(mesh):
    return {'cells': list(map(cell_to_json, mesh.get_cells()))}


def cell_to_json(cell):
    return {'x': cell.x, 'y':cell.y, 'width':cell.width, 'height':cell.height}

@app.route('/worldmap')
def worldmap():
    return jsonify({'circles' : worldmap['circles'], 'triangles': worldmap['triangles'],
                    'squares': worldmap['squares'], 'pentagons': worldmap['pentagons']})
