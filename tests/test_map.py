from nose.tools import *
from nose import with_setup
from map import Map
import numpy as np

def test_map_init():
    map = Map(100, 100)
    assert_equal(100, map._width)
    assert_equal(100, map._height)
    assert_equal([50,50], map.get_robot_position())
