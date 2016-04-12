import base_station.base_station_web_controller as base_station
from unittest.mock import *


class TestBaseStationWebController:

    def test_run_should_start_flask_server(self):
        # Given
        a_host = "localhost"
        a_port = "1234"
        mock_app = Mock()
        base_station.inject_mock_map(mock_app)

        # When
        base_station.run_base_app(a_host, a_port)

        # Then
        mock_app.run.assert_called_once_with(host=a_host, port=a_port, threaded=True)




