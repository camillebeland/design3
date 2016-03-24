from unittest.mock import *
from nose.tools import assert_equals
from robot.vision_daemon import VisionDaemon
import robot.robot_info_assembler
import robot.vision_daemon
from nose.tools import *
import requests
import json


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

    @patch('robot.vision_daemon.requests.get')
    def test_fetch_robot_position_from_vision_should_set_new_position(self, mock_requests_get):
        # Given
        mock_assembler = Mock()
        mock_assembler.json_to_robot_info.return_value = "a return value to make test finish"
        self.vision_daemon = VisionDaemon("a web address", mock_assembler)
        mock_response = Mock()
        mock_requests_get.return_value = mock_response
        mock_json_robot_info = "robot's info"
        mock_response.json.return_value = mock_json_robot_info

        #mock_requests_framework.exceptions.return_value.RequestException.return_value = requests.exceptions.RequestException
        #requests.exceptions.RequestException

        # When
        self.vision_daemon.__fetch_robot_position_from_vision__()

        # Then
        mock_assembler.json_to_robot_info.assert_called_once_with(mock_json_robot_info)

        self.teardown_function()