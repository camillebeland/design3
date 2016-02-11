from configuration import configuration
from base_station.camera_service import CameraService
from base_station.mock_camera_service import MockVideoCamera
from base_station import base_station_web_controller
from base_station.double_sided_buffer import DoubleSidedBuffer
import cv2

if __name__ == '__main__':

    def camera_builder(camera_config, camera_id):
        if camera_config == "webcam":
            open_cv_camera = cv2.VideoCapture(camera_id)
            buffer = DoubleSidedBuffer()
            camera = CameraService(open_cv_camera, cv2, buffer)
        if camera_config == "mock":
            camera = MockVideoCamera()
        return camera

    config = configuration.getconfig()
    port = config.getint('baseapp', 'port')
    camera_config = config.get('baseapp', 'camera')
    camera_id = config.getint('baseapp', 'camera_id')
    refresh_time = config.getint('baseapp', 'refresh_time')

    camera = camera_builder(camera_config, camera_id)

    base_station_web_controller.inject(camera, refresh_time)
    base_station_web_controller.run(port)

