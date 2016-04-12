from unittest.mock import *
from nose.tools import *
from robot.vision_daemon import VisionDaemon


class TestVisionDaemon:

    def teardown_function(self):
        self.vision_daemon.stop_fetching_robot_position_from_vision()

    @patch('robot.vision_daemon.requests')
    @patch('robot.vision_daemon.threading')
    def test_init_vision_daemon_should_start_fetch_position(self, mock_requests_framework, mock_thread):
        # Given
        base_station_address = "https://localhost:5000"

        # When
        self.vision_daemon = VisionDaemon(base_station_address, Mock(), is_mock=True)

        # Then
        assert_true(self.vision_daemon.running)
        self.teardown_function()


