from nose.tools import *
from src.robot.robot import * 
from time import sleep

def test_pos():
    robot = Robot()
    assert_equal([0,0], robot.pos)


def test_speed():
    robot = Robot()
    robot.start()
    sleep(0.1)
    robot.set_vel(2,1)
    sleep(0.5)

    x_actual = robot.pos[0]
    y_actual = robot.pos[1]
    x_expected = 1.0
    y_expected = 0.5

    assert_equal_with_error(x_expected, x_actual, 0.05)

def assert_equal_with_error(expected, actual, error_percentage):
    actual_error = abs(1 - actual/expected)
    assert_true( actual_error < error_percentage, msg="Error {1}% larger than {0}%".format(round(error_percentage*100, 2), round(actual_error*100,2)))
