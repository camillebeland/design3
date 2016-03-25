from threading import Thread
from base_station.double_sided_buffer import DoubleSidedBuffer


class CameraService(object):
    def __init__(self, camera, opencv):
        self.opencv = opencv
        self.camera = camera
        self.running = True
        self.buffer = DoubleSidedBuffer()
        self.__start()

    def __del__(self):
        self.stop()
        self.camera.release()

    def get_frame(self, format='bgr'):
        while self.buffer.read() is None:
            pass
        img = self.buffer.read()
        if format == 'bgr':
            return img
        elif format == 'jpeg':
            ret, jpeg = self.opencv.imencode('.jpg', img)
            return jpeg

    def __start(self):
        self.thread = Thread(target=self.__update)
        self.running = True
        self.thread.setDaemon(True)
        self.thread.start()

    def __update(self):
        while self.running:
            success, image = self.camera.read()
            self.buffer.write(image)

    def stop(self):
        self.running = False
