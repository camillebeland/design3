from configuration import configuration
from base_station.camera_service import VideoCamera
from base_station.mock_camera_service import MockVideoCamera
from base_station import base_station_web_controller

if __name__ == '__main__':
    config = configuration.getconfig()

    port = config.getint('baseapp', 'port')
    camera_config = config.get('baseapp', 'camera')
    if camera_config == "webcam":
        camera = VideoCamera()
    if camera_config == "mock":
        camera = MockVideoCamera()

    base_station_web_controller.inject(camera)
    base_station_web_controller.run(port)
