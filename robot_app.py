from robot import robot_web_controller 
from configuration import configuration
from robot.mock_robot import MockRobot

if __name__ == '__main__':
    config = configuration.getconfig()
    robot = MockRobot()
    robot.start()
    port = int(config.get('robot', 'port'))
    robot_web_controller.inject(robot)
    robot_web_controller.run(port)
