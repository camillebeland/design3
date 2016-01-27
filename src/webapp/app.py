from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from src.robot.robot import Robot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)
robot = Robot()
robot.start()

@app.route('/')
def index():
    return render_template("index.html")


@socket_io.on('fetchPosition')
def some_function():
    socket_io.emit('position',  {'robotPosition': robot.pos})

if __name__ == '__main__':
    socket_io.run(app)

