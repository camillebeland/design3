from base_station.vision.island_detector import IslandDetector
from base_station.vision.robot_detector import RobotDetector
from base_station.vision.table_calibrator import TableCalibrator
from base_station.vision.treasure_detector import TreasureDetector
from base_station.vision_service import VisionService
from base_station.vision.charging_station_detector import ChargingStationDetector
from vision_utils.mock_camera_service import MockCameraService


class TestVisionService:

    def __init__(self):
        self.camera = MockCameraService(image_path="test_with_islands.jpg")
        self.shape_detector = IslandDetector()
        self.treasure_detector = TreasureDetector()
        self.table_calibrator = TableCalibrator()
        self.robot_detector = RobotDetector()
        self.charging_station_detector = ChargingStationDetector()
        self.vision_service = VisionService(self.camera, self.shape_detector, self.treasure_detector,
                                            self.table_calibrator, self.robot_detector, self.charging_station_detector)
        self.vision_service.init_worldmap_contour()


    def test_vision_service_with_no_robot_when_find_robot_position_should_return_nothing(self):
        # When
        robot_position = self.vision_service.find_robot_position()

        # Then
        assert not robot_position

    def test_vision_service_with_treasure_when_find_treasure_should_return_treasure_position(self):
        # Given
        NB_TREASURE = 1

        # When
        map = self.vision_service.build_map()

        # Then
        assert len(map['treasures']) == NB_TREASURE

    def test_vision_service_when_table_calibration_should_return_table_corner_and_ratio(self):
        #Given
        RATIO_LOW = 740
        RATIO_UP = 760

        # When
        table_calibration = self.vision_service.get_calibration_data()

        # Then
        assert len(table_calibration['table_contour']) == 4
        assert RATIO_LOW < table_calibration['pixels_per_meter'] < RATIO_UP



