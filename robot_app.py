import serial
import serial.tools.list_ports as lp
from configuration import configuration
from pathfinding.mesh_builder import MeshBuilder
from pathfinding.pathfinding import PathFinder
from robot import robot_web_controller
from robot.table_calibration_service import TableCalibrationService
from robot.assemblers.robot_info_assembler import RobotInfoAssembler
from robot.manchester_antenna_usb_controller import ManchesterAntennaUsbController
from robot.battery import Battery
from robot.gripper import Gripper
from robot.map import Map
from robot.robot import Robot
from robot.robot_service import RobotService
from robot.simulation.error_simulation import NoisyWheels
from robot.simulation.manchester_antenna_simulation import ManchesterAntennaSimulation
from robot.simulation.battery_simulation import BatterySimulation
from robot.simulation.gripper_simulation import GripperSimulation
from robot.simulation.simulation_map import SimulationMap
from robot.wheels_usb_commands import WheelsUsbCommands
from robot.wheels_usb_controller import WheelsUsbController
from robot.wheels_correction_layer import WheelsCorrectionLayer
from robot.worldmap_service import WorldmapService
from robot.action_machine import ActionMachine
from robot.actions.move_to_charge_station import MoveToChargeStationAction
from robot.vision_daemon import VisionDaemon
from robot.movement import Movement
from robot.robot_logger_decorator import RobotLoggerDecorator

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

    robot_service = RobotService(base_station_address, island_server_address)
    table_calibration_service = TableCalibrationService(base_station_host, base_station_port)
    pixel_per_meter_ratio = table_calibration_service.get_pixel_per_meter_ratio()

    if wheels_config == "simulation":
        world_map = SimulationMap(1600, 1200)
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
        gripper = GripperSimulation()

    elif wheels_config == "usb-arduino":
        assembler = RobotInfoAssembler()
        vision_daemon = VisionDaemon(base_station_address, assembler)
        world_map = Map(vision_daemon)

        arduino_pid = config.getint('robot', 'arduino-pid')
        arduino_vid = config.getint('robot', 'arduino-vid')
        arduino_baudrate = config.getint('robot', 'arduino-baudrate')
        ports = lp.comports()
        arduino_port = list(filter(lambda port: port.pid == arduino_pid and port.vid == arduino_vid, ports))
        assert(len(list(arduino_port)) != 0)
        serial_port = serial.Serial(port=arduino_port[0].device, baudrate=arduino_baudrate, timeout=0.01)
        wheels = WheelsUsbController(serial_port, WheelsUsbCommands())
        corrected_wheels = WheelsCorrectionLayer(wheels, pixel_per_meter_ratio)
        manchester_antenna = ManchesterAntennaUsbController(serial_port)
        battery = Battery(serial_port)
        gripper = Gripper(serial_port)

    table_corners = table_calibration_service.get_table_corners()

    islands = WorldmapService(base_station_host, base_station_port)
    polygons = islands.get_polygons()
    treasures = islands.get_treasures()

    mesh_builder = MeshBuilder(table_corners, polygons)
    mesh = mesh_builder.get_mesh()
    pathfinder = PathFinder(mesh)
    movement = Movement(pathfinder, world_map, wheels, loop_time, min_distance_to_target)
    robot_service = RobotService(base_station_address, island_server_address)
    robot = Robot(corrected_wheels, world_map, pathfinder, manchester_antenna, movement, battery, gripper)

    action_machine = ActionMachine()

    move_to_charge_station = MoveToChargeStationAction(robot, robot_service, world_map, None)

    action_machine.register('move_to_charge_station', move_to_charge_station)
    action_machine.bind('start', 'move_to_charge_station')
    robot_logger = RobotLoggerDecorator(robot, robot_service)
    robot_web_controller.inject(robot_logger, mesh, robot_service, action_machine)
    robot_web_controller.run(host, port)
