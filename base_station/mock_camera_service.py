import cv2


class MockCameraService(object):
    def __init__(self):
        image = cv2.imread("base_station/mock_image.jpg")
        ret, jpeg = cv2.imencode('.jpg', image)
        self.image_bytes = jpeg


    def get_frame(self):
        return self.image_bytes

