from unittest.mock import *
from base_station.vision_service import VisionService

class TestRobotService:

    def __init__(self):
        self.camera_mock = Mock()
        self.shape_detector_mock = Mock()
        self.treasure_detector_mock = Mock()
        self.vision_service = VisionService(self.camera_mock, self.shape_detector_mock, self.treasure_detector_mock)

    def test_vision_service_with_circles_when_build_map_should_return_map_with_circles(self):
        # Given
        NO_POLYGONS = 0
        NB_CIRCLES = 4
        self.shape_detector_mock.find_circle_color.return_value = [{'radius': 20.892581939697266, 'x': 97.5, 'y': 391.5}]
        self.shape_detector_mock.find_polygon_color.return_value = []
        self.treasure_detector_mock.find_treasures.return_value = []

        # When
        map = self.vision_service.build_map()

        # Then
        assert len(map['circles']) == NB_CIRCLES
        assert len(map['pentagons']) == NO_POLYGONS
        assert len(map['triangles']) == NO_POLYGONS
        assert len(map['squares']) == NO_POLYGONS

    def test_vision_service_with_polygons_when_build_map_should_return_map_with_polygons(self):
        # Given
        NO_CIRCLE = 0
        NB_OF_POLYGONS = 4
        self.shape_detector_mock.find_circle_color.return_value = []
        self.treasure_detector_mock.find_treasures.return_value = []
        self.shape_detector_mock.find_polygon_color.return_value = [{'x': 97.5, 'y': 391.5}]

        # When
        map = self.vision_service.build_map()

        # Then
        assert len(map['circles']) == NO_CIRCLE
        assert len(map['pentagons']) == NB_OF_POLYGONS
        assert len(map['triangles']) == NB_OF_POLYGONS
        assert len(map['squares']) == NB_OF_POLYGONS

    def test_vision_service_with_robot_when_find_robot_position_should_return_robot_position(self):
        #Given
        ROBOT_POSITION_CENTER = (97.5, 391.5)
        self.shape_detector_mock.find_circle_color.return_value = [{'x': 97.5, 'y': 391.5, 'radius': 21.2222}]
        self.shape_detector_mock.find_polygon_color.return_value = [{'x': 97.5, 'y': 391.5}]
        self.treasure_detector_mock.find_treasures.return_value = []

        #When
        robot_position = self.vision_service.find_robot_position()

        #Then
        assert robot_position['center'] == ROBOT_POSITION_CENTER

    def test_vision_service_with_no_robot_when_find_robot_position_should_return_nothing(self):
        #Given
        self.shape_detector_mock.find_circle_color.return_value = []
        self.shape_detector_mock.find_polygon_color.return_value = []
        self.treasure_detector_mock.find_treasures.return_value = []

        #When
        robot_position = self.vision_service.find_robot_position()

        #Then
        assert not robot_position

    def test_vision_service_with_treasure_when_find_treasure_should_return_treasure_position(self):
        #Given
        NB_TREASURE = 1
        TREASURE_POSITION_X = 97.5
        TREASURE_POSITION_Y = 391.5
        self.shape_detector_mock.find_circle_color.return_value = []
        self.shape_detector_mock.find_polygon_color.return_value = []
        self.treasure_detector_mock.find_treasures.return_value = [{'x': 97.5, 'y': 391.5}]

        #When
        map = self.vision_service.build_map()

        #Then
        assert len(map['treasures']) == NB_TREASURE
        assert map['treasures'][0]['x'] == TREASURE_POSITION_X
        assert map['treasures'][0]['y'] == TREASURE_POSITION_Y



