import cv2
import os


class MockCameraService(object):

    def __init__(self, image_path="vision_utils/island_frame.jpg"):
        image = cv2.imread(image_path)
        self.image = image

    def get_frame(self, format='bgr'):
        img = self.image
        if format == 'bgr':
            return img
        elif format == 'jpeg':
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg



