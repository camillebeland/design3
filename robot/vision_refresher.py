from pathfinding.mesh_builder import MeshBuilder
from pathfinding.pathfinding import PathFinder
from robot.worldmap_service import WorldmapService

class VisionRefresher:
    def __init__(self, robot, island_host, island_port, camera, table_corners):
        self.__table_corners = table_corners
        self.__robot = robot
        self.__island_port = island_port
        self.__island_host = island_host
        self.__camera = camera

    def refresh(self):
        self.__robot.stop()

        islands = WorldmapService(self.__island_host, self.__island_port)
        polygons = islands.get_polygons()
        mesh_builder = MeshBuilder(self.__table_corners, polygons)
        mesh = mesh_builder.get_mesh()
        pathfinder = PathFinder(mesh)
        self.__robot.init_vision(pathfinder)
