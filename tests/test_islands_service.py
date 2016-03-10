from unittest.mock import *
from robot.islands_service import IslandsService


class TestIslandsService:
    
    @patch('robot.islands_service.requests')
    def test_get_polygons_info_should_send_http_call(self, mock_requests_framework):
        # Given
        host = "localhost"
        port = '5000'
        islands_service = IslandsService(host, port)

        # When
        islands_service.get_polygons()

        # Then
        mock_requests_framework.get.assert_called_once_with('http://'+ host + ':' + port + '/worldmap')

    @patch('robot.islands_service.requests')
    def test_get_polygons_with_polygons_should_return_polygons(self, mock_requests_framework):
        mock_requests_framework.get.return_value.json.return_value = \
            {"circles": [{"color": "yellow", "radius": 20.892581939697266, "shape": "circle", "x": 97.5, "y": 391.5}],
             "pentagons": [],
             "triangles": [],
             "squares": []}

        # Given
        host = "localhost"
        port = '5000'
        islands_service = IslandsService(host, port)

        # When
        polygons = islands_service.get_polygons()

        # Then
        assert polygons[0].x == 97.5
        assert polygons[0].y == 391.5