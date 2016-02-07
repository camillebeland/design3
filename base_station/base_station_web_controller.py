from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def inject(a_camera):
    global camera
    camera = a_camera


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


def run(port):
    app.run(port=port)