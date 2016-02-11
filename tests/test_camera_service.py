from nose.tools import *
from nose import with_setup
from base_station.camera_service import VideoCamera

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
    camera = VideoCamera(mock_video, cv2)
    image = camera.get_frame()
    assert_equal("bytes", image)