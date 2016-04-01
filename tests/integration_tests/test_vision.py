from base_station.vision_service import VisionService
from base_station.mock_camera_service import MockCameraService
from base_station.vision.island_detector import IslandDetector
from base_station.vision.table_calibrator import TableCalibrator
from base_station.vision.treasure_detector import TreasureDetector
from base_station.vision.robot_detector import RobotDetector
from base_station.vision.charging_station_detector import ChargingStationDetector
import os


class TestVision:
    def __init__(self):
        base_directory = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(base_directory, 'test_with_islands.jpg')
        print(image_path)

        self.camera = MockCameraService(image_path=image_path)
        self.shape_detector = IslandDetector()
        self.treasure_detector = TreasureDetector()
        self.table_calibrator = TableCalibrator()
        self.robot_detector = RobotDetector()
        self.charging_station_detector = ChargingStationDetector()
        self.vision_service = VisionService(self.camera, self.shape_detector, self.treasure_detector,
                                            self.table_calibrator, self.robot_detector, self.charging_station_detector)
        self.vision_service.init_worldmap_contour()

    def test_vision_service_when_build_map_should_return_map_islands(self):
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