from robot.timer import Timer
from nose.tools import *


class TestTimer:
    def test_get_time_since_beginning_should_return_zero_if_timer_not_started(self):
        # Given
        timer = Timer()

        # When
        time_returned = timer.get_time_since_beginning()

        # Then
        time_elapsed = 0
        assert_equals(time_elapsed, time_returned)