from robot import robot_web_controller
from configuration import configuration
from robot.simulation_robot import SimulationWheels

from robot.wheels_usb_controller import WheelsUsbController
import serial
import serial.tools.list_ports as lp
from robot.wheels_usb_commands import WheelsUsbCommands

from robot.robot import Robot
from robot.map import Map
from pathfinding.pathfinding import Mesh, Cell, polygon, PathFinder

if __name__ == '__main__':
    config = configuration.getconfig()

    port = config.getint('robot', 'port')
    wheelsconfig = config.get('robot', 'wheels')

    worldmap = Map(400,400)
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

        wheels = SimulationWheels(worldmap, refresh_time = refreshtime, wheels_velocity=wheelsvelocity)

    elif(wheelsconfig == "usb-arduino"):
        arduino_pid = config.get('robot', 'arduino-pid')
        arduino_vid = config.get('robot', 'arduino-pid')
        ports = lp.comports()
        arduinoport = filter(lambda port: port.pid == arduino_pid and port.vid == arduino_vid, ports)
        assert(len(arduinoport) == 0)
        serialport = serial.Serial(port=arduinoport[0].device)
        wheels = WheelsUsbController(serialport,WheelsUsbCommands)

    #mesh hardcode
    cell = Cell(700,400,350,200)
    mesh = Mesh(cell.partitionCells([polygon(200,200,10), polygon(400,200,5),polygon(50, 300, 5)],10))
    pathfinder = PathFinder(mesh)
    robot = Robot(wheels, worldmap,pathfinder)
    robot_web_controller.inject(robot, mesh)
    robot_web_controller.run(port)
