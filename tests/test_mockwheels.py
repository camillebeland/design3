from nose.tools import *
from nose import with_setup
from mock_robot import MockWheels
from time import sleep


wheels = MockWheels()

def setup():
    print("Setting things up")
    wheels.__init__()

def teardown():
    pass

@with_setup(setup, teardown)
def test_pos():
    assert_equal([0,0], wheels.pos)


@with_setup(setup, teardown)
def test_speed():
    wheels.start()
    sleep(0.1)
    wheels.set_velocity(2,1)
    sleep(0.5)

    x_actual = wheels.pos[0]
    y_actual = wheels.pos[1]
    x_expected = 1.0
    y_expected = 0.5

    assert_equal_with_error(x_expected, x_actual, 0.05)
    assert_equal_with_error(y_expected, y_actual, 0.05)

def assert_equal_with_error(expected, actual, error_percentage):
    if( expected == 0 ):
        actual_error = abs(actual)
    else:
        actual_error = abs(1 - actual/expected)

    assert_true( actual_error < error_percentage, msg="Error {1}% larger than {0}%".format(round(error_percentage*100, 2), round(actual_error*100,2)))

