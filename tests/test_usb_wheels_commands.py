from nose.tools import *
from nose import with_setup
from robot import wheels_usb_commands as cmd

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
