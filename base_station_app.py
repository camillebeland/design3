from flask import Flask, Response
from flask_cors import CORS
from base_station.camera_service import VideoCamera
from configuration import configuration

app = Flask(__name__)
CORS(app)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('baseapp', 'port'))
    app.run(port=port)
