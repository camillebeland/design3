from nose.tools import *
from base_station.camera_service import CameraService

class TestCameraService:
    def setup(self):
        self.camera = CameraService(mock_camera, cv2)