from flask import Flask, Response
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)


def inject(a_camera, a_refresh_time):
    global camera, refresh_time
    camera = a_camera
    refresh_time = a_refresh_time


def gen(camera, refresh_time):
    while True:
        time.sleep(refresh_time)
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(camera, refresh_time), mimetype='multipart/x-mixed-replace; boundary=frame')


def run(port):
    app.run(port=port)