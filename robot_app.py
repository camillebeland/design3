from robot import robot_web_controller
from configuration import configuration
from robot.mock_robot import MockWheels
from robot.robot import Robot
from robot.map import Map

if __name__ == '__main__':
    config = configuration.getconfig()

    port = config.getint('robot', 'port')
    wheelsconfig = config.get('robot', 'wheels')

    worldmap = Map(400,400)
    if(wheelsconfig == "mock"):
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

        wheels = MockWheels(worldmap, refresh_time = refreshtime, wheels_velocity=wheelsvelocity)

    robot = Robot(wheels, worldmap)

    robot.start()
    robot_web_controller.inject(robot)
    robot_web_controller.run(port)
