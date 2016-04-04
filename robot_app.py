import serial
import serial.tools.list_ports as lp
from configuration import configuration
from pathfinding.mesh_builder import MeshBuilder
from pathfinding.pathfinding import PathFinder
from robot import robot_web_controller
from robot.assemblers.robot_info_assembler import RobotInfoAssembler
from robot.manchester_antenna_usb_controller import ManchesterAntennaUsbController
from robot.battery import Battery
from robot.map import Map
from robot.vision_perspective_correction import VisionPerspectiveCorrection
from robot.robot import Robot
from robot.robot_service import RobotService
from robot.simulation.error_simulation import NoisyWheels
from robot.simulation.manchester_antenna_simulation import ManchesterAntennaSimulation
from robot.simulation.battery_simulation import BatterySimulation
from robot.simulation.simulation_map import SimulationMap
from robot.simulation.magnet_simulation import MagnetSimulation
from robot.wheels_usb_commands import WheelsUsbCommands
from robot.wheels_usb_controller import WheelsUsbController
from robot.wheels_correction_layer import WheelsCorrectionLayer
from robot.worldmap_service import WorldmapService
from robot.action_machine import ActionMachine
from robot.actions.move_to_charge_station import MoveToChargeStationAction
from robot.actions.pick_up_treasure import PickUpTreasure
from robot.actions.drop_down_treasure import DropDownTreasure
from robot.actions.recharge import RechargeAction
from robot.actions.discover_manchester_code import DiscoverManchesterCodeAction
from robot.actions.find_island_clue import FindIslandClue
from robot.vision_daemon import VisionDaemon
from robot.movement import Movement
from robot.magnet import Magnet
from robot.simulation.magnet_simulation import MagnetSimulation
from maestroControl.prehenseur_rotation_control import PrehenseurRotationControl
from robot.vision_refresher import VisionRefresher

from utils.position import Position

if __name__ == '__main__':
    config = configuration.get_config()

    host = config.get('robot', 'host')
    port = config.getint('robot', 'port')
    wheels_config = config.get('robot', 'wheels')
    base_station_host = config.get('baseapp', 'host')
    base_station_port = config.get('baseapp', 'port')
    base_station_camera = config.get('baseapp', 'camera')
    base_station_address = "http://" + base_station_host + ":" + base_station_port
    island_server_address = config.get('island_server', 'host')
    loop_time = config.getfloat('robot', 'loop-time')
    min_distance_to_target = config.getfloat('robot', 'min-distance-to-target')

    robot_service = RobotService(island_server_address)
    world_map_service = WorldmapService(base_station_host, base_station_port)

    if wheels_config == "simulation":
        world_map = SimulationMap(1600, 1200, world_map_service)
        try:
            refresh_time = config.getint('robot', 'wheels-refresh-time')
        except:
            print("Warning : wheels-refresh-time not specified, setting 10")
            refresh_time = 10

        try:
            wheels_velocity= config.getint('robot', 'wheels-velocity')
        except:
            print("Warning : wheels-velocity not specified, setting 5")
            wheels_velocity = 5

        try:
            noise = config.getint('robot', 'simulation-noise')
        except:
            print("Warning : noise not specified, setting 0")
            noise = 0

        wheels = NoisyWheels(world_map, refresh_time = refresh_time, wheels_velocity=wheels_velocity, noise=noise)
        corrected_wheels = WheelsCorrectionLayer(wheels, 1.0)
        manchester_antenna = ManchesterAntennaSimulation()
        battery = BatterySimulation()
        magnet = MagnetSimulation()

    elif wheels_config == "usb-arduino":
        assembler = RobotInfoAssembler()
        vision_daemon = VisionDaemon(base_station_address, assembler)
        camera_position_x = config.getint('robot', 'camera-position-x')
        camera_position_y = config.getint('robot', 'camera-position-y')
        camera_height = config.getfloat('robot', 'camera-height')
        robot_height = config.getfloat('robot', 'robot-height')
        vision_perspective_corrected= VisionPerspectiveCorrection(vision_daemon, Position(camera_position_x,camera_position_y), camera_height, robot_height)
        world_map = Map(vision_perspective_corrected, world_map_service)

        arduino_pid = config.getint('robot', 'arduino-pid')
        arduino_vid = config.getint('robot', 'arduino-vid')
        arduino_baudrate = config.getint('robot', 'arduino-baudrate')
        ports = lp.comports()
        arduino_port = list(filter(lambda port: port.pid == arduino_pid and port.vid == arduino_vid, ports))
        assert(len(list(arduino_port)) != 0)
        print(arduino_port[0].device)
        serial_port = serial.Serial(port=arduino_port[0].device, baudrate=arduino_baudrate, timeout=0.1)
        print( serial_port.isOpen())
        wheels = WheelsUsbController(serial_port, WheelsUsbCommands())

        corrected_wheels = WheelsCorrectionLayer(wheels, 1.0)
        manchester_antenna = ManchesterAntennaUsbController(serial_port)
        battery = Battery(serial_port)
        polulu_port = serial.Serial(port='/dev/ttyACM1', timeout=1)
        prehenseur = PrehenseurRotationControl(polulu_port)
        magnet = Magnet(serial_port, prehenseur)

    movement = Movement(compute=None, sense=world_map, control=wheels, loop_time=loop_time, min_distance_to_target=min_distance_to_target)
    robot_service = RobotService(island_server_address)
    robot = Robot(wheels=corrected_wheels, world_map=world_map, pathfinder=None, manchester_antenna=manchester_antenna, movement=movement, battery=battery, magnet=magnet)

    vision_refresher = VisionRefresher(robot, corrected_wheels, base_station_host, base_station_port)

    action_machine = ActionMachine()
    move_to_charge_station = MoveToChargeStationAction(robot, robot_service, world_map, None)
    pick_up_treasure = PickUpTreasure(robot, robot_service, world_map, None)
    drop_down_treasure = DropDownTreasure(robot, robot_service, world_map, None)
    read_manchester_code = DiscoverManchesterCodeAction(robot, robot_service, world_map, None)
    find_island_clue = FindIslandClue(robot, robot_service, world_map, None)
    recharge = RechargeAction(robot, robot_service,world_map, None)
    find_island_clue = FindIslandClue(robot, robot_service, world_map, None)

    action_machine.register('move_to_charge_station', move_to_charge_station)
    action_machine.register('read_manchester_code', read_manchester_code)
    action_machine.bind('start', 'move_to_charge_station')
    action_machine.register('pick_up_treasure', pick_up_treasure)
    action_machine.bind('pick_up_treasure', 'pick_up_treasure')
    action_machine.register('drop_down_treasure', drop_down_treasure)
    action_machine.bind('drop_down_treasure', 'drop_down_treasure')
    action_machine.bind("read_manchester", "read_manchester_code")
    action_machine.register('find_island_clue', find_island_clue)
    action_machine.bind('find_island_clue', 'find_island_clue')
    action_machine.register("recharge", recharge)
    action_machine.bind("recharge", "recharge")

    robot_web_controller.inject(robot, vision_refresher, robot_service, action_machine)
    robot_web_controller.run(host, port)
