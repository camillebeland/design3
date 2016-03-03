from nose.tools import *
from nose import with_setup
from robot.wheels_usb_commands import WheelsUsbCommands

cmd = WheelsUsbCommands()

def test_stop():
    assert_equal("(s)".encode(), cmd.stop())

def test_rotate_left():
    assert_equal("(rl*)".encode(), cmd.rotate_left(42))

def test_rotate_right():
    assert_equal("(rrU)".encode(), cmd.rotate_right(85))

def test_move_slow():
    assert_equal('(m%X'.encode()+encodeint(0x01)+encodeint(244)+')'.encode(), cmd.move_slow(9560, 500))

def test_move():
    assert_equal('(M'.encode()+encodeint(0x00)+encodeint(0x00)+encodeint(0x14)+encodeint(0x04)+')'.encode(), cmd.move(0, 5124))

@raises(Exception)
def test_when_rotate_left_of_angle_larger_than_pi_then_raise_exception():
    cmd.rotate_left(200)

@raises(Exception)
def test_when_rotate_left_of_a_negative_angle_then_raise_exception():
    cmd.rotate_left(-45)

def test_when_move_slow_of_negative_value_then_add_bit_sign():
    assert_equal('(m'.encode()+encodeint(0x81)+encodeint(0x56)+encodeint(0x80)+encodeint(0x7b)+')'.encode(), cmd.move_slow(-342, -123))


def encodeint(integer):
    return bytes([integer])
