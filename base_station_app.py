from configuration import configuration
from base_station.camera_service import CameraService
from base_station.mock_camera_service import MockCameraService
from base_station import base_station_web_controller
import cv2

from base_station.vision_service import VisionService
from base_station.vision import ShapeDetector


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
    refresh_time = config.getint('baseapp', 'refresh_time')
    camera_width = config.getint('baseapp', 'camera_width')
    camera_height = config.getint('baseapp', 'camera_height')

    camera = camera_builder(camera_config, camera_id, camera_width, camera_height)
    vision = VisionService(camera, ShapeDetector())
    worldmap = vision.build_map()

    base_station_web_controller.inject(camera, refresh_time, worldmap)
    base_station_web_controller.run(host, port)
    
if __name__ == '__main__':
    run()