from configuration import configuration
from base_station.camera_service import CameraService
from base_station.mock_camera_service import MockCameraService
from base_station import base_station_web_controller
from base_station import base_station_robot_controller
from threading import Thread
import cv2

from base_station.vision_service import VisionService
from base_station.vision import ShapeDetector

def base_station_web_server():
    host = config.get('baseapp', 'host')
    port = config.getint('baseapp', 'port')
    refresh_time = config.getint('baseapp', 'refresh_time')

    base_station_web_controller.inject(camera, refresh_time, worldmap)
    base_station_web_controller.run(host, port)

def base_station_robot_server():
    port = config.getint('robot_baseapp', 'port')

    base_station_robot_controller.inject(worldmap)
    base_station_robot_controller.run(port=port)

if __name__ == '__main__':
    def camera_builder(camera_config, camera_id):
        if camera_config == "webcam":
            open_cv_camera = cv2.VideoCapture(camera_id)
            open_cv_camera.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
            open_cv_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
            camera = CameraService(open_cv_camera, cv2)
        if camera_config == "mock":
            camera = MockCameraService()
        return camera

    config = configuration.getconfig()
    camera_config = config.get('baseapp', 'camera')
    camera_id = config.getint('baseapp', 'camera_id')
    camera_width = config.getint('baseapp', 'camera_width')
    camera_height = config.getint('baseapp', 'camera_height')

    camera = camera_builder(camera_config, camera_id)
    vision = VisionService(camera, ShapeDetector())
    worldmap = vision.build_map()

    Thread(target = base_station_robot_server()).start()
    Thread(target = base_station_web_server()).start()