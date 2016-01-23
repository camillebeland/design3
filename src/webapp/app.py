from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)


@app.route('/')
def index():
    return render_template("index.html")


@socket_io.on('message')
def some_function():
    coordonates = randint(0,200)
    socket_io.emit('event',  {'data': coordonates})

if __name__ == '__main__':
    socket_io.run(app)

