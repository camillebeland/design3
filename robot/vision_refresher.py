from pathfinding.mesh_builder import MeshBuilder
from pathfinding.pathfinding import PathFinder
from robot.worldmap_service import WorldmapService
from robot.table_calibration_service import TableCalibrationService
from robot.embedded_camera import EmbeddedCamera
from robot.vision.embedded_vision_service import EmbeddedVisionService
from robot.vision.embedded_treasure_detector import EmbeddedTreasureDetector
from robot.vision.embedded_recharge_station_detector import EmbeddedRechargeStationDetector
from maestroControl.camera_rotation_control import CameraRotationControl

class VisionRefresher:
    def __init__(self, robot, corrected_wheels, island_host, island_port, camera, vision_daemon):
        self.__corrected_wheels = corrected_wheels
        self.__robot = robot
        self.__island_port = island_port
        self.__island_host = island_host
        self.__camera = camera
        self.__vision_daemon = vision_daemon

    def refresh(self):
        self.__robot.stop()

        islands = WorldmapService(self.__island_host, self.__island_port)
        table_calibration = TableCalibrationService(self.__island_host, self.__island_port)
        pixel_per_meters = table_calibration.get_pixel_per_meter_ratio()
        self.__corrected_wheels.set_correction(pixel_per_meters)
        polygons = islands.get_polygons()
        table_corners = table_calibration.get_table_corners()
        mesh_builder = MeshBuilder(table_corners, polygons)
        mesh = mesh_builder.get_mesh()
        pathfinder = PathFinder(mesh)
        self.__robot.init_vision(pathfinder)

        embedded_vision_service = EmbeddedVisionService(self.__camera, EmbeddedTreasureDetector(), EmbeddedRechargeStationDetector())
        embedded_camera = EmbeddedCamera(table_calibration, embedded_vision_service, self.__vision_daemon)
        treasures = embedded_camera.get_treasures()
