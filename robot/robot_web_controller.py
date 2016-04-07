from flask import Flask, request, jsonify
from flask.ext.socketio import SocketIO
from flask_cors import CORS
from utils.position import Position
import logging

app = Flask(__name__)
CORS(app)
socket_io = SocketIO(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def inject(a_robot, a_vision_refresher, a_robot_service, an_action_machine):
    global robot, vision_refresher, robot_service, action_machine
    robot = a_robot
    robot_service = a_robot_service
    action_machine = an_action_machine
    vision_refresher = a_vision_refresher


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
    robot.move_to(destination, None)
    return "OK"


@app.route('/robot/stop', methods=['POST'])
def robot_stop():
    robot.stop()
    return "OK"


@socket_io.on('fetchRobotInfo')
def robot_fetch_info():
    socket_io.emit('robotUpdated', {'robotPosition': robot.get_position().to_dict(),
                                     'robotAngle': robot.get_angle()})


@socket_io.on('fetchGripperVoltage')
def robot_fetch_info():
    socket_io.emit('gripperUpdated', {'capacitorCharge': robot.get_capacitor_charge()})


@socket_io.on('fetchPath')
def robot_fetch_path():
    path = []
    path.append(robot.get_position().to_dict())
    for position in robot.get_path():
        path.append(position.to_dict())
    socket_io.emit('path', {'robotPath': path})


@app.route('/mesh')
def mesh():
    return jsonify(mesh_to_json(robot.get_mesh()))


def mesh_to_json(mesh):
    return {'cells': list(map(cell_to_json, mesh.get_cells()))}


def cell_to_json(cell):
    return {'x': cell.x, 'y': cell.y, 'width': cell.width, 'height': cell.height}


@app.route('/manchester', methods=['GET'])
def get_manchester():
    code = robot.get_manchester_code()
    if code is None:
        return jsonify({'code', ''})
    else:
        return jsonify({'code' : code.__str__()})


@app.route('/manchester/<code>', methods=['POST'])
def post_manchester_code(code):
    robot.set_manchester_code(code)
    return "Ok"


@app.route('/island', methods=['GET'])
def get_island():
    clue = robot.get_island_clue()
    return jsonify(clue)


@app.route('/island/<clue>', methods=['POST'])
def set_island(clue):
    robot.set_island_clue(clue)
    return "Ok"


@app.route('/actions/<action>', methods=['POST'])
def send_action_to_robot(action):
    try:
        action_machine.notify_event(action)
        return "OK"
    except:
        print('action : {0} did not work'.format(action))


@app.route('/actions')
def get_actions():
    return jsonify(action_machine.get_events())


@app.route('/robot/vision/refresh', methods=['POST'])
def recalculate_world_map():
    vision_refresher.refresh()
    return "OK"
