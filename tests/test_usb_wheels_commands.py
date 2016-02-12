from nose.tools import *
from nose import with_setup
from robot.wheels_usb_commands import WheelsUsbCommands

cmd = WheelsUsbCommands()

def test_stop():
    assert_equal("(s)", cmd.stop())

def test_rotate_left():
    assert_equal("(rl*)", cmd.rotate_left(42))

def test_rotate_right():
    assert_equal("(rrU)", cmd.rotate_right(85))

def test_move_slow():
    assert_equal("(m%X\x01ô)", cmd.move_slow(9560, 500))

def test_move():
    assert_equal("(M\x00\x00\x14\x04)", cmd.move(0, 5124))

@raises(Exception)
def test_when_rotate_left_of_angle_larger_than_pi_then_raise_exception():
    cmd.rotate_left(200)

@raises(Exception)
def test_when_rotate_left_of_a_negative_angle_then_raise_exception():
    cmd.rotate_left(-45)

def test_when_move_slow_of_negative_value_then_add_bit_sign():
    assert_equal('(m\x81\x56\x80\x7b)', cmd.move_slow(-342, -123))
