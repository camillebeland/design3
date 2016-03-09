from nose.tools import *
from unittest.mock import *
from robot.movement import Movement


class TestMovement:

    def test_move_to_thread_should_log(self):
        # Given
        mock_http_service = Mock()
        movement = Movement(compute=Mock(), sense=Mock(), control=Mock(), http_service=mock_http_service)
        final_destination = "your mom"

        # When
        movement.move_to_thread(final_destination)

        # Then
        mock_http_service.log_info.assert_called_once_with("robot asked to move to "+str(final_destination))
