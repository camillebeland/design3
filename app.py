from flask import Flask, render_template
from flask.ext.socketio import SocketIO

app = Flask(__name__, static_folder='webapp/static', template_folder='webapp/templates')
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    socket_io.run(app, port=8080)
