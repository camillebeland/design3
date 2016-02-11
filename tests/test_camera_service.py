from nose.tools import *
from base_station.camera_service import CameraService
from base_station.double_sided_buffer import DoubleSidedBuffer


class MockVideo:
    def read(self):
        return (True, "image")


class MockCV:
    def imencode(self, string, image):
        if(string == '.jpg' and image == 'image'):
            return (True ,"bytes")


mock_video = MockVideo()
cv2 = MockCV()


def test_when_video_camera_started_then_it_reads_opencv_camera():
    camera = CameraService(mock_video, cv2, DoubleSidedBuffer())
    image = camera.get_frame()
    assert_equal("bytes", image)

