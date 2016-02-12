from nose.tools import *
from base_station.camera_service import CameraService
from base_station.double_sided_buffer import DoubleSidedBuffer


class MockCameraCapture:
    def read(self):
        return (True, "image")


class MockOpenCV:
    def imencode(self, string, image):
        if (string == '.jpg' and image == 'image'):
            return (True, "bytes")


mock_camera = MockCameraCapture()
cv2 = MockOpenCV()


class TestCameraService:
    def setup(self):
        self.camera = CameraService(mock_camera, cv2, DoubleSidedBuffer())

    def test_given_a_camera_when_get_frame_then_returns_image_in_bytes(self):
        image = self.camera.get_frame()
        assert_equal("bytes", image)
