import base_station.base_station_web_controller as base_station
from unittest.mock import *


class TestBaseStationWebController:

    @patch('base_station.base_station_web_controller.logger')
    def test_run_should_strat_flask_server(self, mock_logger):
        # Given
        a_host = "localhost"
        a_port = "1234"
        mock_app = Mock()
        base_station.inject_mock_map(mock_app)

        # When
        base_station.run_base_app(a_host, a_port)

        # Then
        mock_app.run.assert_called_once_with(host=a_host, port=a_port, threaded=True)

    @patch('base_station.base_station_web_controller.logger')
    def test_run_should_log_starting_flask_server(self, mock_logger):
        # Given
        a_host = "localhost"
        a_port = "1234"
        mock_app = Mock()
        base_station.inject_mock_map(mock_app)

        # When
        base_station.run_base_app(a_host, a_port)

        # Then
        mock_logger.info.assert_any_call("Starting the base station app at "+str(a_port))

    @patch('base_station.base_station_web_controller.request')
    @patch('base_station.base_station_web_controller.logger')
    def test_log_info_should_call_log_info_on_logger(self, mock_logger, mock_flask_request):
        # Given
        mock_app = Mock()
        base_station.inject_mock_map(mock_app)
        a_message = "Hi, this is a message"
        data = {}
        data['message'] = a_message
        mock_flask_request.json = data

        # When
        base_station.log_info()

        # Then
        mock_logger.info.assert_called_once_with(a_message)


