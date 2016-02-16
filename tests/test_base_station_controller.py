from nose.tools import *
import base_station.base_station_web_controller as base_station
import numpy

class MockCameraService:
    def get_frame(self):
        return numpy.array([2,3,1,0])

mock_camera_service = MockCameraService()
REFRESH_TIME = 0


class TestBaseStationWebController:
    def test_base_station_web_controller_when_generate_frame_return_image_in_bytes(self):
        given_array = numpy.array([2,3,1,0]).tobytes()
        frame_bytes = base_station.generate_frame(mock_camera_service, REFRESH_TIME)
        assert_true(given_array in next(frame_bytes))