from threading import Thread


class VideoCamera(object):
    def __init__(self, camera, opencv):
        self.opencv = opencv
        self.video = camera
        self.running = True
        self.__start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, jpeg = self.opencv.imencode('.jpg', self.image)
        return jpeg

    def __start(self):
        print("starting")
        self.thread = Thread(target = self.__update)
        self.running = True
        self.thread.setDaemon(True)
        self.thread.start()

    def __update(self):
        while self.running:
            success, self.image = self.video.read()

    def stop(self):
        self.running = False
