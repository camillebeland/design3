from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from configuration import configuration

app = Flask(__name__, static_folder='webapp/static', template_folder='webapp/templates')
socket_io = SocketIO(app)


@app.route('/')
def index():
    return render_template("index.html")


def start_server(port):
    socket_io.run(app, port=port)


if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('webapp', 'port'))
    socket_io.run(app, port=port)
    start_server(port)

