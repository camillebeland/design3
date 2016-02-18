from robot import robot_web_controller
from configuration import configuration
from robot.simulation_robot import SimulationWheels

from robot.wheels_usb_controller import WheelsUsbController
import serial
import serial.tools.list_ports as lp
from robot.wheels_usb_commands import WheelsUsbCommands

from robot.robot import Robot
from robot.map import Map

if __name__ == '__main__':
    config = configuration.getconfig()

    host = config.get('robot', 'host')
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
        arduino_pid = config.getint('robot', 'arduino-pid')
        arduino_vid = config.getint('robot', 'arduino-vid')
        ports = lp.comports()
        print("{0} , {1}".format(arduino_pid, arduino_vid))	
        arduinoport = list(filter(lambda port: port.pid == arduino_pid and port.vid == arduino_vid, ports))
        assert(len(list(arduinoport)) != 0)
        print(arduinoport[0].device)
        serialport = serial.Serial(port=arduinoport[0].device, baudrate=115200)
        wheels = WheelsUsbController(serialport,WheelsUsbCommands())

    robot = Robot(wheels, worldmap)
    robot_web_controller.inject(robot)
    robot_web_controller.run(host, port)
