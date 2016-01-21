from nose.tools import *
from src.robot.robot import * 

def test_pos():
    robot = Robot()
    assert_equal([0,0], robot.pos)


