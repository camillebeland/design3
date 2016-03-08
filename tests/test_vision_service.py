from unittest.mock import *
from base_station.vision_service import VisionService

class TestRobotService:

    def test_vision_service_with_circles_when_build_map_should_return_map_with_circles(self):
        # Given
        NO_POLYGONS = 0
        NB_CIRCLES = 4
        camera_mock = Mock()
        shape_detector_mock = Mock()
        vision_service = VisionService(camera_mock, shape_detector_mock)
        shape_detector_mock.find_circle_color.return_value = [{'radius': 20.892581939697266, 'x': 97.5, 'y': 391.5}]
        shape_detector_mock.find_polygon_color.return_value = []

        # When
        map = vision_service.build_map()

        # Then
        assert len(map['circles']) == NB_CIRCLES
        assert len(map['pentagons']) == NO_POLYGONS
        assert len(map['triangles']) == NO_POLYGONS
        assert len(map['squares']) == NO_POLYGONS

    def test_vision_service_with_polygons_when_build_map_should_return_map_with_polygons(self):
        # Given
        NO_CIRCLE = 0
        NB_OF_POLYGONS = 4
        camera_mock = Mock()
        shape_detector_mock = Mock()
        vision_service = VisionService(camera_mock, shape_detector_mock)
        shape_detector_mock.find_circle_color.return_value = []
        shape_detector_mock.find_polygon_color.return_value = [{'x': 97.5, 'y': 391.5}]

        # When
        map = vision_service.build_map()

        # Then
        assert len(map['circles']) == NO_CIRCLE
        assert len(map['pentagons']) == NB_OF_POLYGONS
        assert len(map['triangles']) == NB_OF_POLYGONS
        assert len(map['squares']) == NB_OF_POLYGONS

