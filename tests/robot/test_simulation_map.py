from nose import with_setup
from nose.tools import *
from utils.position import Position
from unittest.mock import *

from robot.simulation.simulation_map import SimulationMap

WIDTH = 300.0
HEIGHT = 100.0
A_POSITION = Position(20.0, 50.0)
A_POSITION_OUTSIDE_BOUNDARIES = Position(500.0, 200.0)
AN_ANGLE = 142
A_MOVE_OUTSIDE = Position(A_POSITION.x + WIDTH, 0.0)
PRECISION = 1e-6

world_map = SimulationMap(WIDTH, HEIGHT, Mock(), Mock())


def setup():
    world_map.__init__(WIDTH, HEIGHT, Mock(), Mock())


@with_setup(setup)
def test_when_init_map_then_width_is_set():
    assert_equal(WIDTH, world_map._width)


@with_setup(setup)
def test_when_init_map_then_height_is_set():
    assert_equal(HEIGHT, world_map._height)


@with_setup(setup)
def test_when_set_robot_position_then_position_is_set():
    a_position_x = 3
    a_position_y = 4
    a_position = Position(a_position_x, a_position_y)
    world_map.set_robot_position(a_position_x, a_position_y)
    assert_equal(a_position, world_map.get_robot_position())


@with_setup(setup)
def test_when_rotate_robot_of_angle_then_robot_has_rotated_an_angle():
    world_map.rotate_robot(AN_ANGLE)
    assert_equal(AN_ANGLE, world_map.get_robot_angle())


@with_setup(setup)
def test_given_a_rotated_robot_of_a_small_angle_when_move_a_distance_then_robot_has_moved_with_angle_considered():
    world_map.rotate_robot(30)
    world_map.move_robot(0, 10)

    assert_equal_with_error(A_POSITION.x + 5, world_map.get_robot_position().x, PRECISION)
    assert_equal_with_error(A_POSITION.y + 8.66025, world_map.get_robot_position().y, PRECISION)


@with_setup(setup)
def test_given_a_rotated_robot_of_a_large_angle_when_move_a_distance_then_robot_has_moved_with_angle_considered():
    world_map.rotate_robot(200)
    world_map.move_robot(0, 10)

    assert_equal_with_error(A_POSITION.x - 3.42020143, world_map.get_robot_position().x, PRECISION)
    assert_equal_with_error(A_POSITION.y - 9.39692620, world_map.get_robot_position().y, PRECISION)


@with_setup(setup)
def test_when_rotate_robot_for_an_angle_larger_than_circle_then_wrap_to_360():
    world_map.rotate_robot(500)
    assert_equal(140, world_map.get_robot_angle())


def assert_equal_with_error(expected, actual, error):
    actual_error = expected - actual

    assert_true( actual_error < error, msg="Error {1} larger than {0}".format(error, actual_error))


