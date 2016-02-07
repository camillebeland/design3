import cv2


class MockVideoCamera(object):
    def __init__(self):
        image = cv2.imread("base_station/mock_image.jpg")
        ret, jpeg = cv2.imencode('.jpg', image)
        self.image_bytes = jpeg.tobytes()


    def get_frame(self):
        return self.image_bytes

