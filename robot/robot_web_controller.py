from flask import Flask, request, jsonify
from flask.ext.socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socket_io = SocketIO(app)


def inject(a_robot, a_mesh, a_robot_service, an_action_machine):
    global robot, mesh, robot_service, action_machine
    robot = a_robot
    mesh = a_mesh
    robot_service = a_robot_service
    action_machine = an_action_machine


def run(host, port):
    socket_io.run(app, host=host, port=port)


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


@app.route('/robot/move_to', methods=['POST'])
def robot_move_to():
    destination = []
    destination.append(request.json['x'])
    destination.append(request.json['y'])
    robot.move_to(destination)
    return "OK"


@socket_io.on('fetchPosition')
def robot_fetch_position():
    socket_io.emit('position',  {'robotPosition': robot.get_position(),
                                 'robotAngle': robot.get_angle()})


@socket_io.on('fetchPath')
def robot_fetch_path():
    socket_io.emit('path',  {'robotPath': robot.get_path()})


@app.route('/mesh')
def mesh():
    return jsonify(mesh_to_json(mesh))


@app.route('/manchester', methods=['POST'])
def ask_island_from_code():
    island = robot_service.ask_target_island(request.json["letter"])
    return island


def mesh_to_json(mesh):
    return {'cells': list(map(cell_to_json, mesh.get_cells()))}


def cell_to_json(cell):
    return {'x': cell.x, 'y':cell.y, 'width':cell.width, 'height':cell.height}

@app.route('/action/<action>', methods = ['POST'])
def send_action_to_robot(action):
    print(action)
    action_machine.notify_event(action)
    return('OK')
