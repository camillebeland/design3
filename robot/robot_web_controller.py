from flask import Flask
from flask.ext.socketio import SocketIO
from configuration import configuration
from flask_cors import CORS
from flask import request, jsonify

app = Flask(__name__)
CORS(app)
socket_io = SocketIO(app)


def inject(a_robot, a_mesh):
    global robot, mesh
    robot = a_robot
    mesh = a_mesh

def run(port):
    socket_io.run(app, port=port)


@app.route('/robot/move', methods=['POST'])
def robot_move():
    delta_x = request.json['delta_x']
    delta_y = request.json['delta_y']
    robot.move(delta_x, delta_y)
    return "OK"

@app.route('/robot/rotate', methods=['POST'])
def robot_rotate():
    angle = request.json['angle']
    robot.rotate(angle)
    return "OK"

@socket_io.on('fetchPosition')
def robot_fetchposition():
    socket_io.emit('position',  {'robotPosition': robot.getpos(),
                                 'robotAngle': robot.get_angle()})
@app.route('/mesh')
def mesh():
    return jsonify(mesh_to_json(mesh))

def mesh_to_json(mesh):
    return {'cells': list(map(cell_to_json, mesh.get_cells()))}

def cell_to_json(cell):
    return {'x': cell.x, 'y':cell.y, 'width':cell.width, 'height':cell.height}
