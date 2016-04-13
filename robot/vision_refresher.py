from pathfinding.mesh_builder import MeshBuilder
from pathfinding.pathfinding import PathFinder
from robot.worldmap_service import WorldmapService


class VisionRefresher:
    def __init__(self, robot, island_host, island_port, camera, table_corners, treasure_easiest_path):
        self.__table_corners = table_corners
        self.__robot = robot
        self.__island_port = island_port
        self.__island_host = island_host
        self.__camera = camera
        self.__treasure_easiest_path = treasure_easiest_path

    def refresh(self, callback=None):
        worldmap = WorldmapService(self.__island_host, self.__island_port)
        polygons = worldmap.get_polygons()
        mesh_builder = MeshBuilder(self.__table_corners, polygons)
        mesh = mesh_builder.get_mesh()
        pathfinder = PathFinder(mesh, polygons)
        self.__treasure_easiest_path.reset_attributes(pathfinder, worldmap)
        self.__robot.init_vision(pathfinder)
        if callback is not None:
            callback()
