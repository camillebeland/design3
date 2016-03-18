from robot import robot_web_controller
from configuration import configuration
from robot.error_simulation import NoisyWheels

from robot.wheels_usb_controller import WheelsUsbController
import serial
import serial.tools.list_ports as lp
from robot.wheels_usb_commands import WheelsUsbCommands

from robot.robot import Robot
from robot.map import Map
from pathfinding.pathfinding import PathFinder, Cell, Mesh
from robot.islands_service import IslandsService
from robot.robot_service import RobotService

from pathfinding.pathfinding import Polygon

if __name__ == '__main__':
    config = configuration.get_config()

    host = config.get('robot', 'host')
    port = config.getint('robot', 'port')
    wheelsconfig = config.get('robot', 'wheels')
    base_station_host = config.get('baseapp', 'host')
    base_station_port = config.get('baseapp', 'port')
    base_station_address = "http://" + base_station_host + ":" + base_station_port

    worldmap = Map(900, 544)
    if(wheelsconfig == "simulation"):
        try:
            refreshtime = config.getint('robot', 'wheels-refresh-time')
        except :
            print("Warning : wheels-refresh-time not specified, setting 10")
            refreshtime = 10

        try:
            wheelsvelocity= config.getint('robot', 'wheels-velocity')
        except :
            print("Warning : wheels-velocity not specified, setting 5")
            wheelsvelocity = 5

        try:
            noise = config.getint('robot', 'simulation-noise')
        except :
            print("Warning : noise not specified, setting 0")
            noise = 0


        wheels = NoisyWheels(worldmap, refresh_time = refreshtime, wheels_velocity=wheelsvelocity, noise=noise)

    elif(wheelsconfig == "usb-arduino"):
        arduino_pid = config.getint('robot', 'arduino-pid')
        arduino_vid = config.getint('robot', 'arduino-vid')
        arduino_baudrate = config.getint('robot', 'arduino-baudrate')
        ports = lp.comports()
        arduinoport = list(filter(lambda port: port.pid == arduino_pid and port.vid == arduino_vid, ports))
        assert(len(list(arduinoport)) != 0)
        serialport = serial.Serial(port=arduinoport[0].device,baudrate=arduino_baudrate)
        wheels = WheelsUsbController(serialport,WheelsUsbCommands())

    islands = IslandsService(base_station_host, base_station_port)
    cell = Cell(1600,1200,800,600)
    polygons = islands.get_polygons()

    mesh = Mesh(cell.partition_cells(polygons, 100))
    pathfinder = PathFinder(mesh)
    robot_service = RobotService(base_station_address)
    robot = Robot(wheels, worldmap, pathfinder, robot_service)
    robot_web_controller.inject(robot, mesh)
    robot_web_controller.run(host, port)
