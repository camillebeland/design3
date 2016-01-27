from nose.tools import *
from nose import with_setup
from robot.robot import *
from time import sleep


robot = Mock_Robot()

def setup():
    print("Setting things up")
    robot.__init__()

def teardown():
    pass

@with_setup(setup, teardown)
def test_pos():
    assert_equal([0,0], robot.pos)


@with_setup(setup, teardown)
def test_speed():
    robot.start()
    sleep(0.1)
    robot.set_vel(2,1)
    sleep(0.5)

    x_actual = robot.pos[0]
    y_actual = robot.pos[1]
    x_expected = 1.0
    y_expected = 0.5

    assert_equal_with_error(x_expected, x_actual, 0.05)
    assert_equal_with_error(y_expected, y_actual, 0.05)

@with_setup(setup, teardown)
def test_move():
    robot.move(3.14159, 2.3)

    x_vel_actual = robot.vel[0]
    y_vel_actual = robot.vel[1]
    x_vel_expected = -2.3
    y_vel_expected = 0.0

    assert_equal_with_error(x_vel_expected, x_vel_actual, 0.001)
    assert_equal_with_error(y_vel_expected, y_vel_actual, 0.001)

def assert_equal_with_error(expected, actual, error_percentage):
    if( expected == 0 ):
        actual_error = abs(actual)
    else:
        actual_error = abs(1 - actual/expected)

    assert_true( actual_error < error_percentage, msg="Error {1}% larger than {0}%".format(round(error_percentage*100, 2), round(actual_error*100,2)))

