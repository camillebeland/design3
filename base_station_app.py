import cv2
from base_station import base_station_web_controller
from base_station.camera_service import CameraService
from base_station.mock_camera_service import MockCameraService
from base_station.vision.island_detector import IslandDetector
from base_station.vision.treasure_detector import TreasureDetector
from base_station.vision.table_calibrator import TableCalibrator
from base_station.vision.charging_station_detector import ChargingStationDetector
from base_station.vision.robot_detector import RobotDetector
from base_station.vision_service import VisionService
from configuration import configuration
from base_station.vision.robot_vision_daemon import RobotVisionDaemon
from utils.dto.position import Position


def camera_builder(camera_config, camera_id, camera_width, camera_height):
    if camera_config == "webcam":
        open_cv_camera = cv2.VideoCapture(camera_id)
        WIDTH_PARAMETER_ID = 3
        HEIGHT_PARAMETER_ID = 4
        open_cv_camera.set(WIDTH_PARAMETER_ID, camera_width)
        open_cv_camera.set(HEIGHT_PARAMETER_ID, camera_height)
        camera = CameraService(open_cv_camera, cv2)
    if camera_config == "mock":
        camera = MockCameraService()
    return camera


def run():
    config = configuration.get_config()
    host = config.get('baseapp', 'host')
    port = config.getint('baseapp', 'port')
    camera_config = config.get('baseapp', 'camera')
    camera_id = config.getint('baseapp', 'camera_id')
    refresh_time = config.getfloat('baseapp', 'refresh_time')
    camera_width = config.getint('baseapp', 'camera_width')
    camera_height = config.getint('baseapp', 'camera_height')
    wheels_config = config.get('robot', 'wheels')

    camera = camera_builder(camera_config, camera_id, camera_width, camera_height)
    vision = VisionService(camera, IslandDetector(), TreasureDetector(), TableCalibrator(), RobotDetector(), ChargingStationDetector())
    vision.init_worldmap_contour()
    worldmap = vision.build_map()

    if wheels_config == "usb-arduino":
        camera_position_x = config.getint('robot', 'camera-position-x')
        camera_position_y = config.getint('robot', 'camera-position-y')
        camera_position = Position(camera_position_x, camera_position_y)
        camera_height = config.getfloat('robot', 'camera-height')
        robot_height = config.getfloat('robot', 'robot-height')
        robot_host = config.get('robot', 'host')
        robot_port = config.get('robot', 'port')
        robot_address = "http://" + robot_host + ":" + robot_port
        RobotVisionDaemon(robot_address, camera_position, camera_height, robot_height)

    base_station_web_controller.inject(camera, refresh_time, worldmap, vision)
    base_station_web_controller.run_base_app(host, port)

if __name__ == '__main__':
    run()
