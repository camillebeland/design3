import cv2

class MockCameraService(object):
    def __init__(self):
        image = cv2.imread("base_station/photo_robot_mauve.jpg")
        self.image = image


    def get_frame(self, format='bgr'):
        img  = self.image
        if(format == 'bgr'):
            return img
        elif(format == 'jpeg'):
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg



