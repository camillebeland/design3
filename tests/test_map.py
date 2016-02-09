from nose.tools import *
from nose import with_setup
from map import Map

WIDTH = 300.0
HEIGHT = 100.0
A_POSITION = [20.0,50.0]
A_POSITION_OUTSIDE_BOUNDARIES = [500.0,200.0]
AN_ANGLE = 142
A_MOVE_OUTSIDE = [A_POSITION[0] + WIDTH, 0.0]
PRECISION = 1e-6

worldmap = Map(WIDTH, HEIGHT)

def setup():
    worldmap.__init__(WIDTH, HEIGHT)

@with_setup(setup)
def test_when_init_map_then_width_is_set():
    assert_equal(WIDTH, worldmap._width)

@with_setup(setup)
def test_when_init_map_then_height_is_set():
    assert_equal(HEIGHT, worldmap._height)

@with_setup(setup)
def test_when_set_robot_position_then_position_is_set():
    worldmap.set_robot_position(A_POSITION[0], A_POSITION[1])
    assert_equal(A_POSITION, worldmap.get_robot_position())

@with_setup(setup)
def test_when_set_robot_position_outside_boudaries_then_raise_error():
    assert_raises(Exception,
                  worldmap.set_robot_position,
                  A_POSITION_OUTSIDE_BOUNDARIES[0],
                  A_POSITION_OUTSIDE_BOUNDARIES[1])


@with_setup(setup)
def test_when_move_robot_outside_boundaries_then_raise_error():
    assert_raises(Exception,
                  worldmap.move_robot,
                  A_MOVE_OUTSIDE[0],
                  A_MOVE_OUTSIDE[1])

@with_setup(setup)
def test_when_rotate_robot_of_angle_then_robot_has_rotated_an_angle():
    worldmap.rotate_robot(AN_ANGLE)
    assert_equal(AN_ANGLE, worldmap.get_robot_angle())

@with_setup(setup)
def test_given_a_rotated_robot_of_a_small_angle_when_move_a_distance_then_robot_has_moved_with_angle_considered():
    worldmap.rotate_robot(30)
    worldmap.move_robot(0,10)

    assert_equal_with_error(A_POSITION[0] + 5, worldmap.get_robot_position()[0], PRECISION)
    assert_equal_with_error(A_POSITION[1] + 8.66025, worldmap.get_robot_position()[1], PRECISION)

@with_setup(setup)
def test_given_a_rotated_robot_of_a_large_angle_when_move_a_distance_then_robot_has_moved_with_angle_considered():
    worldmap.rotate_robot(200)
    worldmap.move_robot(0,10)

    assert_equal_with_error(A_POSITION[0] - 3.42020143, worldmap.get_robot_position()[0], PRECISION)
    assert_equal_with_error(A_POSITION[1] - 9.39692620, worldmap.get_robot_position()[1], PRECISION)

@with_setup(setup)
def test_when_rotate_robot_for_an_angle_larger_than_circle_then_wrap_to_360():
    worldmap.rotate_robot(500)
    assert_equal(140, worldmap.get_robot_angle())

def assert_equal_with_error(expected, actual, error):
    actual_error = expected - actual

    assert_true( actual_error < error, msg="Error {1} larger than {0}".format(error, actual_error))


