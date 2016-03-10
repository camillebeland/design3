import cv2
import os

class MockCameraService(object):
    def __init__(self):
        root_directory = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(root_directory, "base_station", "mock_image.jpg")
        image = cv2.imread(image_path)
        self.image = image


    def get_frame(self, format='bgr'):
        img  = self.image
        if(format == 'bgr'):
            return img
        elif(format == 'jpeg'):
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg



