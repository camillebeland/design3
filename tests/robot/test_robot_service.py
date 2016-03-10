from nose.tools import *
from unittest.mock import *
from robot.robot_service import RobotService

import logging


class TestRobotService:

    @patch('robot.robot_service.requests')
    def test_log_info_should_send_http_call(self, mock_requests_framework):
        # Given
        a_message = "Something is happening during the normal course of the system"
        base_station_address = "address of the base station"
        robot_service = RobotService(base_station_address)

        # When
        robot_service.log_info(a_message)

        # Then
        mock_requests_framework.post.assert_called_once_with(base_station_address+"/logger/info", json={'message': a_message})

