import cv2
from threading import Thread

class VideoCamera(object):
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.video = cv2.VideoCapture(camera_id)
        self.running = True
        self.start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, jpeg = cv2.imencode('.jpg', self.image)
        return jpeg.tobytes()

    def start(self):
        print("starting")
        self.thread = Thread(target = self.__update)
        self.running = True
        self.thread.start()

    def __update(self):
        while self.running:
            success, self.image = self.video.read()

    def stop(self):
        self.running = False
