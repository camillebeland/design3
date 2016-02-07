from robot import robot_web_controller
from configuration import configuration
from robot.mock_robot import MockWheels
from robot.robot import Robot


if __name__ == '__main__':
    config = configuration.getconfig()

    port = config.getint('robot', 'port')
    wheelsconfig = config.get('robot', 'wheels')
    if(wheelsconfig == "mock"):
        try:
            refreshtime = config.getint('robot', 'wheels-refresh-time')
        except :
            print("Warning : wheels-refresh-time not specified, setting 10")
            refreshtime = 10

        wheels = MockWheels(refreshtime)
    robot = Robot(wheels)
    robot.start()
    robot_web_controller.inject(robot)
    robot_web_controller.run(port)
