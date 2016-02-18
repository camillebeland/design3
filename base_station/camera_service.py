from threading import Thread

class CameraService(object):
    def __init__(self, camera, opencv, buffer):
        self.opencv = opencv
        self.camera = camera
        self.running = True
        self.buffer = buffer
        self.__start()

    def __del__(self):
        self.stop()
        self.camera.release()

    def get_frame(self):
        img = self.buffer.read()
        ret, jpeg = self.opencv.imencode('.jpg', img)
        return jpeg

    def __start(self):
        print("starting")
        self.thread = Thread(target = self.__update)
        self.running = True
        self.thread.setDaemon(True)
        self.thread.start()

    def __update(self):
        while self.running:
            success, image = self.camera.read()
            self.buffer.write(image)

    def stop(self):
        self.running = False
