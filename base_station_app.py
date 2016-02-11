from configuration import configuration
from base_station.camera_service import VideoCamera
from base_station.mock_camera_service import MockVideoCamera
from base_station import base_station_web_controller
import cv2

if __name__ == '__main__':
    config = configuration.getconfig()

    port = config.getint('baseapp', 'port')
    camera_config = config.get('baseapp', 'camera')
    camera_id = config.getint('baseapp', 'camera_id')
    refresh_time = config.getint('baseapp', 'refresh_time')
    if camera_config == "webcam":
        open_cv_camera = cv2.VideoCapture(camera_id)
        camera = VideoCamera(open_cv_camera, cv2)
    if camera_config == "mock":
        camera = MockVideoCamera()

    base_station_web_controller.inject(camera, refresh_time)
    base_station_web_controller.run(port)
