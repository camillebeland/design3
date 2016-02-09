from nose.tools import *
from nose import with_setup
from mock_robot import MockWheels
from time import sleep

class MockedMap:
    def __init__(self):
        self.robotdistance = [0,0]
        self.robotangle = 0

    def move_robot(self, delta_x, delta_y):
        self.robotdistance[0] += delta_x
        self.robotdistance[1] += delta_y

    def rotate_robot(self, angle):
        self.robotangle += angle

mockedworldmap = MockedMap()
wheels = MockWheels(mockedworldmap)

AN_ANGLE = 42
A_DISTANCE = [10,2]
SPEED = 200
FAST_REFRESH_TIME_IN_MS = 2
TIME_TO_GO_A_DISTANCE_IN_SECONDS = 0.1
PRECISION = 1e-6


def setup():
    mockedworldmap.__init__()
    wheels.__init__(mockedworldmap, wheels_velocity=SPEED, refresh_time=FAST_REFRESH_TIME_IN_MS)

def teardown():
    wheels.stop()

@with_setup(setup=setup, teardown=teardown)
def test_when_initiated_wheels_has_no_target():
    assert_equal([0,0], wheels.target)

@with_setup(setup=setup, teardown=teardown)
def test_when_initiated_wheels_are_not_running():
    assert_false(wheels.running)

@with_setup(setup=setup, teardown=teardown)
def test_when_initiated_wheels_has_no_directions():
    assert_equal([0,0], wheels.direction)

@with_setup(setup=setup, teardown=teardown)
def test_when_start_wheels_are_running():
    wheels.start()
    assert_true(wheels.running)

@with_setup(setup=setup, teardown=teardown)
def test_when_start_and_stop_then_wheels_are_not_running():
    wheels.start()
    wheels.stop()
    assert_false(wheels.running)

@with_setup(setup=setup, teardown=teardown)
def test_given_started_wheels_when_move_a_distance_then_robot_has_moved_a_distance():
    wheels.start()
    wheels.move(A_DISTANCE[0],A_DISTANCE[1])
    sleep(TIME_TO_GO_A_DISTANCE_IN_SECONDS)
    assert_equal_with_error(A_DISTANCE[0], mockedworldmap.robotdistance[0], PRECISION)
    assert_equal_with_error(A_DISTANCE[1], mockedworldmap.robotdistance[1], PRECISION)


@with_setup(setup=setup, teardown=teardown)
def test_given_started_wheels_when_move_zero_distance_then_robot_has_not_moved():
    wheels.start()
    wheels.move(0,0)
    sleep(TIME_TO_GO_A_DISTANCE_IN_SECONDS)
    assert_equal_with_error(0,mockedworldmap.robotdistance[0], PRECISION)

@with_setup(setup=setup, teardown=teardown)
def test_given_started_wheels_when_rotate_wheels_of_angle_then_robot_has_rotate_an_angle():
    wheels.start()
    wheels.rotate(AN_ANGLE)
    assert_equal(AN_ANGLE, mockedworldmap.robotangle)

def assert_equal_with_error(expected, actual, error):
    actual_error = expected - actual
    assert_true( actual_error < error, msg="Error {1} larger than {0}".format(error, actual_error))


