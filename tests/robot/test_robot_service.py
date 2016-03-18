from unittest.mock import *
from nose.tools import assert_equals
from robot.robot_service import RobotService


class TestRobotService:

    @patch('robot.robot_service.requests')
    def test_log_info_should_send_http_call(self, mock_requests_framework):
        # Given
        a_message = "Something is happening during the normal course of the system"
        base_station_address = "address of the base station"
        robot_service = RobotService(base_station_address, Mock())

        # When
        robot_service.log_info(a_message)

        # Then
        mock_requests_framework.post.assert_called_once_with(base_station_address+"/logger/info", json={'message': a_message})

    @patch('robot.robot_service.requests')
    def test_ask_target_island_should_return_island_from_island_server(self, mock_requests_framework):
        # Given
        island_server_address = "https://192.168.0.2/"
        robot_service = RobotService(Mock(), island_server_address)
        code_letter = "A"
        payload = {'code': code_letter}
        mock_response = Mock()
        expected_response_text = "blue triangle"
        mock_response.text = expected_response_text
        mock_requests_framework.get.return_value = mock_response

        # When
        response = robot_service.ask_target_island(code_letter)

        # Then
        mock_requests_framework.get.assert_called_once_with("https://192.168.0.2/", verify=False, params=payload)
        assert_equals(expected_response_text, response)

    @patch('robot.robot_service.requests')
    def test_get_robot_position_should_fetch_position(self, mock_requests_framework):
        # Given
        base_station_address = "https://localhost:5000"
        robot_service = RobotService(base_station_address, Mock())
        robot_service.start_fetching_robot_position_from_vision()

        # When
        response = robot_service.get_robot_position()
        robot_service.stop_fetching_robot_position_from_vision()

        # Then
        mock_requests_framework.get.assert_called_with("https://localhost:5000/robot_position")



