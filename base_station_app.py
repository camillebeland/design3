from configuration import configuration
from base_station.camera_service import CameraService
from base_station.mock_camera_service import MockCameraService
from base_station import base_station_web_controller
from base_station.double_sided_buffer import DoubleSidedBuffer
from pathfinding.mesh import Mesh, Cell, polygon
import cv2

if __name__ == '__main__':

    def camera_builder(camera_config, camera_id):
        if camera_config == "webcam":
            open_cv_camera = cv2.VideoCapture(camera_id)
            open_cv_camera.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
            open_cv_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
            buffer = DoubleSidedBuffer()
            camera = CameraService(open_cv_camera, cv2, buffer)
        if camera_config == "mock":
            camera = MockCameraService()
        return camera

    config = configuration.getconfig()
    host = config.get('baseapp', 'host')
    port = config.getint('baseapp', 'port')
    camera_config = config.get('baseapp', 'camera')
    camera_id = config.getint('baseapp', 'camera_id')
    refresh_time = config.getint('baseapp', 'refresh_time')
    camera_width = config.getint('baseapp', 'camera_width')
    camera_height = config.getint('baseapp', 'camera_height')

    camera = camera_builder(camera_config, camera_id)

    #mesh hardcode
    cell = Cell(700,400,350,200)
    mesh = Mesh(cell.partitionCells([polygon(200,200,10), polygon(400,200,5),polygon(50, 300, 5)],10))
    

    base_station_web_controller.inject(camera, refresh_time, mesh)
    base_station_web_controller.run(host, port)
