from threading import Thread
from base_station.world_map_vision.color_filter import *
from base_station.double_sided_buffer import DoubleSidedBuffer
from base_station.world_map_vision.islands_finder import IslandsFinder

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

    def get_frame(self):
        img = self.buffer.read()
        island_finder = IslandsFinder(img, BlueFilter())
        circles, triangles, squares, pentagons = island_finder.find_islands()
        island_finder.draw_contours(circles, triangles, squares, pentagons, img)
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
