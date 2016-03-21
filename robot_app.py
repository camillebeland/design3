import serial
import serial.tools.list_ports as lp

from configuration import configuration
from pathfinding.cell import Cell
from pathfinding.mesh import Mesh
from pathfinding.pathfinding import PathFinder
from robot.map import Map
from robot import robot_web_controller
from robot.worldmap_service import WorldmapService
from robot.manchester_antenna_usb_controller import ManchesterAntennaUsbController
from robot.robot import Robot
from robot.robot_service import RobotService
from robot.simulation.error_simulation import NoisyWheels
from robot.simulation.manchester_antenna_simulation import ManchesterAntennaSimulation
from robot.simulation.simulation_map import SimulationMap
from robot.usb_commands import UsbCommands
from robot.wheels_usb_controller import WheelsUsbController
from robot.vision_daemon import VisionDaemon
from robot.arduino_magnet import ArduinoMagnet
from robot.simulation.simulation_magnet import SimulationMagnet

if __name__ == '__main__':
    config = configuration.get_config()

    host = config.get('robot', 'host')
    port = config.getint('robot', 'port')
    wheelsconfig = config.get('robot', 'wheels')
    base_station_host = config.get('baseapp', 'host')
    base_station_port = config.get('baseapp', 'port')
    base_station_address = "http://" + base_station_host + ":" + base_station_port
    island_server_address = config.get('island_server', 'host')

    robot_service = RobotService(base_station_address, island_server_address)

    if wheelsconfig == "simulation":
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
        except :
            print("Warning : noise not specified, setting 0")
            noise = 0

        wheels = NoisyWheels(world_map, refresh_time = refresh_time, wheels_velocity=wheels_velocity, noise=noise)
        manchester_antenna = ManchesterAntennaSimulation()
        magnet = SimulationMagnet()

    elif wheelsconfig == "usb-arduino":
        vision_daemon = VisionDaemon(base_station_address)
        world_map = Map(1600, 1200, vision_daemon)

        arduino_pid = config.getint('robot', 'arduino-pid')
        arduino_vid = config.getint('robot', 'arduino-vid')
        arduino_baudrate = config.getint('robot', 'arduino-baudrate')
        ports = lp.comports()
        arduinoport = list(filter(lambda port: port.pid == arduino_pid and port.vid == arduino_vid, ports))
        assert(len(list(arduinoport)) != 0)
        serialport = serial.Serial(port=arduinoport[0].device, baudrate=arduino_baudrate, timeout=0.01)
        wheels = WheelsUsbController(serialport, UsbCommands())
        manchester_antenna = ManchesterAntennaUsbController(serialport)
        magnet = ArduinoMagnet(serialport, UsbCommands())

    islands = WorldmapService(base_station_host, base_station_port)
    polygons = islands.get_polygons()
    treasures = islands.get_treasures()

    cell = Cell(1600, 1200, 800, 600)
    mesh = Mesh(cell.partition_cells(polygons, 100))

    pathfinder = PathFinder(mesh)
    robot = Robot(wheels, world_map, pathfinder, robot_service, manchester_antenna, magnet)

    robot_web_controller.inject(robot, mesh, robot_service)
    robot_web_controller.run(host, port)
