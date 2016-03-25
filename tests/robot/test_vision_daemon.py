from unittest.mock import *

from robot.vision_daemon import VisionDaemon


class TestVisionDaemon:

    def teardown_function(self):
        self.vision_daemon.stop_fetching_robot_position_from_vision()

    @patch('robot.vision_daemon.requests')
    def test_init_vision_daemon_should_start_fetch_position(self, mock_requests_framework):
        # Given
        base_station_address = "https://localhost:5000"

        # When
        self.vision_daemon = VisionDaemon(base_station_address, Mock())

        # Then
        mock_requests_framework.get.assert_called_with("https://localhost:5000/vision/robot")

        self.teardown_function()