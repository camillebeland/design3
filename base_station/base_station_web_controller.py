from flask import Flask, Response, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)


def inject(a_camera, a_refresh_time):
    global camera, refresh_time, mesh
    camera = a_camera
    refresh_time = a_refresh_time

def generate_frame(camera, refresh_time):
    while True:
        time.sleep(refresh_time)
        bytes_frame = camera.get_frame().tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytes_frame + b'\r\n\r\n')

def run(port):
    app.run(port=port)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(camera, refresh_time), mimetype='multipart/x-mixed-replace; boundary=frame')

