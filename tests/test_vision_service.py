from base_station.vision_service import VisionService
from base_station.mock_camera_service import MockCameraService
from base_station.vision.island_detector import IslandDetector
from base_station.vision.table_calibrator import TableCalibrator
from base_station.vision.treasure_detector import TreasureDetector

class TestRobotService:

    def __init__(self):
        self.camera_mock = MockCameraService(image_path="test_with_islands.jpg")
        self.shape_detector_mock = IslandDetector()
        self.treasure_detector_mock = TreasureDetector()
        self.table_calibrator_mock = TableCalibrator()
        self.vision_service = VisionService(self.camera_mock, self.shape_detector_mock, self.treasure_detector_mock, self.table_calibrator_mock)
        self.vision_service.init_worldmap_contour()


    def test_vision_service_with_circles_when_build_map_should_return_map_with_circles_and_polygons(self):
        # Given
        NB_TRIANGLES = 1
        NB_CIRCLES = 1
        NB_SQUARES = 1
        NB_PENTAGONS = 1

        # When
        map = self.vision_service.build_map()

        # Then
        assert len(map['circles']) == NB_CIRCLES
        assert len(map['pentagons']) == NB_PENTAGONS
        assert len(map['triangles']) == NB_TRIANGLES
        assert len(map['squares']) == NB_SQUARES

    def test_vision_service_with_robot_when_find_robot_position_should_return_robot_position(self):
        #Given
        ROBOT_POSITION_CENTER = (803.125, 442.375)
        self.camera_mock = MockCameraService(image_path="test_with_robot.jpg")
        self.vision_service = VisionService(self.camera_mock, self.shape_detector_mock, self.treasure_detector_mock, self.table_calibrator_mock)
        self.vision_service.init_worldmap_contour()

        #When
        robot_position = self.vision_service.find_robot_position()

        #Then
        assert robot_position['center'] == ROBOT_POSITION_CENTER

    def test_vision_service_with_no_robot_when_find_robot_position_should_return_nothing(self):
        #When
        robot_position = self.vision_service.find_robot_position()

        #Then
        assert not robot_position

    def test_vision_service_with_treasure_when_find_treasure_should_return_treasure_position(self):
        #Given
        NB_TREASURE = 1
        TREASURE_POSITION_X = 1190
        TREASURE_POSITION_Y = 237

        #When
        map = self.vision_service.build_map()

        #Then
        assert len(map['treasures']) == NB_TREASURE
        assert map['treasures'][0]['x'] == TREASURE_POSITION_X
        assert map['treasures'][0]['y'] == TREASURE_POSITION_Y



