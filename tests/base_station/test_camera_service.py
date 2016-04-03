from unittest.mock import *
from nose.tools import *
from base_station.camera_service import CameraService


#def get_frame(self, format='bgr'):
#    img = self.buffer.read()
#    while img is None:
#        pass
#    if format == 'bgr':
#        return img
#    elif format == 'jpeg':
#        ret, jpeg = self.opencv.imencode('.jpg', img)
#        return jpeg


class TestCameraService:

    def setup(self):
         self.mock_camera = Mock()
         self.mock_open_cv = Mock()
         self.cameraService = CameraService(self.mock_camera, self.mock_open_cv)

    def test_get_frame_should_should_return_image_if_bgr_format(self):
        # Given
        self.setup()
        an_image = "anImage"
        mock_buffer = Mock()
        mock_buffer.read.return_value = an_image
        self.cameraService.set_mock_buffer(mock_buffer)

        # When
        image_returned = self.cameraService.get_frame(format="bgr")

        # Then
        assert_equals(an_image, image_returned)


    def test_stop_should_set_running_to_false(self):
        # Given
        self.setup()

        # When
        self.cameraService.stop()

        # Then
        assert_false(self.cameraService.running)
