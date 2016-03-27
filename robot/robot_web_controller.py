from flask import Flask, request, jsonify
from flask.ext.socketio import SocketIO
from flask_cors import CORS
from utils.position import Position

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
    destination = Position(request.json['x'], request.json['y'])
    robot.move_to(destination)
    return "OK"


@app.route('/robot/stop', methods=['POST'])
def robot_stop():
    robot.stop()
    return "OK"


@socket_io.on('fetchRobotInfo')
def robot_fetch_info():
    socket_io.emit('robotUpdated', {'robotPosition': robot.get_position().to_dict(),
                                     'robotAngle': robot.get_angle(),
                                     'capacitorCharge': robot.get_capacitor_charge()})


@socket_io.on('fetchPath')
def robot_fetch_path():
    list = []
    for position in robot.get_path():
        list.append(position.to_dict())
    socket_io.emit('path', {'robotPath': list})


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


@app.route('/actions/<action>', methods = ['POST'])
def send_action_to_robot(action):
    try:
        action_machine.notify_event(action)
        return "OK"
    except:
        print('action : {0} did not work'.format(action))


@app.route('/actions')
def get_actions():
    return jsonify(action_machine.get_events())
