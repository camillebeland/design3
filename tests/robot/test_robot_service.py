from unittest.mock import *
from nose.tools import assert_equals
from robot.robot_service import RobotService


class TestRobotService:

    @patch('robot.robot_service.requests')
    def test_ask_target_island_should_return_island_from_island_server(self, mock_requests_framework):
        # Given
        island_server_address = "https://192.168.0.2/"
        robot_service = RobotService(island_server_address)
        code_letter = "A"
        payload = {'code': code_letter}
        mock_response = Mock()
        expected_response_text_fr = '{"couleur":"bleu"}'
        expected_response_text_en = {'color', 'blue'}
        mock_response.text = expected_response_text_fr
        mock_requests_framework.get.return_value = mock_response

        # When
        response = robot_service.ask_target_island(code_letter)

        # Then
        mock_requests_framework.get.assert_called_once_with("https://192.168.0.2/", verify=False, params=payload)
        assert_equals(expected_response_text_en, response)



