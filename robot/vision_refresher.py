from pathfinding.mesh_builder import MeshBuilder
from pathfinding.pathfinding import PathFinder
from robot.worldmap_service import WorldmapService
from robot.table_calibration_service import TableCalibrationService

class VisionRefresher:
    def __init__(self, robot, corrected_wheels, island_host, island_port):
        self.__corrected_wheels = corrected_wheels
        self.__robot = robot
        self.__island_port = island_port
        self.__island_host = island_host

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
        pathfinder = PathFinder(mesh, polygons)

        self.__robot.init_vision(pathfinder)
