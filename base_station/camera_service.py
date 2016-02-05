import cv2
import base64


class CameraService:
    def __init__(self):
        self.camera_port = 0

    def take_picture(self):
        retval, image = cv2.VideoCapture(self.camera_port).read()
        return image

    def take_picture_base64(self):
        camera_capture = self.take_picture()
        file = "image.jpg"
        cv2.imwrite(file, camera_capture)
        with open("image.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string




