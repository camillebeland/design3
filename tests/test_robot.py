from nose.tools import *
from robot.robot import Robot

DELTA_X = 10.0
DELTA_Y = 20.0

AN_ANGLE = 30.3

FINAL_DESTINATION = [1, 2]

class MockWheels():
    def move(self, delta_x, delta_y):
        if(delta_x == DELTA_X and delta_y == DELTA_Y):
            self.moveCalledWithGoodArguments = True

    def rotate(self, angle):
        if(angle == AN_ANGLE):
            self.rotateCalled = True

class MockMap():
    def get_robot_position(self):
        self.getRobotPositionCalled = True
        return FINAL_DESTINATION

class MockPathFinder():
    pass

wheels = MockWheels()
worldmap = MockMap()
pathfinder = MockPathFinder()

robot = Robot(wheels, worldmap, pathfinder)

def test_when_robot_move_then_wheels_move():
    robot.move(DELTA_X, DELTA_Y)
    assert_true(wheels.moveCalledWithGoodArguments)

def test_when_robot_move_to_then_get_robot_position_is_called():
    robot.move_to(FINAL_DESTINATION)
    assert_true(worldmap.getRobotPositionCalled)

def test_when_robot_rotate_then_wheels_rotate():
    robot.rotate(AN_ANGLE)
    assert_true(wheels.rotateCalled)
