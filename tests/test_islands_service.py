from unittest.mock import *
from robot.worldmap_service import WorldmapService
from unittest.mock import *


class TestIslandsService:
    
    @patch('robot.worldmap_service.requests')
    def test_get_polygons_info_should_send_http_call(self, mock_requests_framework):
        # Given
        host = "localhost"
        port = '5000'
        worldmap_service = WorldmapService(host, port)

        # When
        worldmap_service.get_polygons()

        # Then
        mock_requests_framework.get.assert_called_once_with('http://' + host + ':' + port + '/worldmap')

    @patch('robot.worldmap_service.requests')
    def test_get_polygons_with_polygons_should_return_polygons(self, mock_requests_framework):
        mock_requests_framework.get.return_value.json.return_value = \
            {"circles": [{"color": "yellow", "radius": 20.892581939697266, "shape": "circle", "x": 97.5, "y": 391.5}],
             "pentagons": [],
             "triangles": [],
             "squares": [],
             "treasures": [],
             "chargingStation": []}

        # Given
        host = "localhost"
        port = '5000'
        worldmap_service = WorldmapService(host, port)

        # When
        polygons = worldmap_service.get_polygons()

        # Then
        assert polygons[0].x == 97.5
        assert polygons[0].y == 391.5

    @patch('robot.worldmap_service.requests')
    def test_get_treasures_with_treasures_should_return_treasures(self, mock_requests_framework):
        mock_requests_framework.get.return_value.json.return_value = \
            {"circles": [],
             "pentagons": [],
             "triangles": [],
             "squares": [],
             "treasures": [{"x": 400, "y": 700}],
             "chargingStation": []
             }

        # Given
        host = "localhost"
        port = '5000'
        worldmap_service = WorldmapService(host, port)

        # When
        treasures = worldmap_service.get_treasures()

        # Then
        assert treasures[0]['x'] == 400
        assert treasures[0]['y'] == 700
