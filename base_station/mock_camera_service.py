import cv2
import os

class MockCameraService(object):
    def __init__(self):
        base_directory = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(base_directory, "\\base_station\mock_image.jpg")
        print(image_path)
        image = cv2.imread(image_path)
        self.image = image


    def get_frame(self, format='bgr'):
        img  = self.image
        if(format == 'bgr'):
            return img
        elif(format == 'jpeg'):
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg



