from utils.position import Position
PONDERATION_FACTOR = 10000.0 # 100 pixels = danger


class TreasureEasiestPath:
    def __init__(self, pathfinder=None, worldmap=None):
        self.__pathfinder = pathfinder
        self.__worldmap = worldmap
        self.__infinity = (float("inf"))

    def find_easiest_treasure_from(self, position, target_island_position):
        treasures = self.__worldmap.get_treasures()
        treasures_positions = list(map(lambda treasure: Position(treasure['x'], treasure['y']), treasures))
        paths = list(map(lambda treasure_position: {'length': self.__find_path_length(position, treasure_position, target_island_position), 'treasure': treasure_position}, treasures_positions))
        return min(paths, key=lambda x: x['length'])['treasure']

    def __find_path_length(self, robot_position, treasure_position, target_island_position):
        try:
            path_length_to_treasure = len(self.__pathfinder.find_path(robot_position, treasure_position))
            path_length_to_island = len(self.__pathfinder.find_path(treasure_position, target_island_position))
            path_length = path_length_to_island + path_length_to_treasure
        except:
            path_length = self.__infinity

        path_length += self.__calculate_islands_risk(treasure_position)
        return path_length

    def reset_attributes(self, pathfinder, worldmap):
        self.__pathfinder = pathfinder
        self.__worldmap = worldmap

    def __calculate_islands_risk(self, treasure_position):
        islands = self.__worldmap.worldmap_service.get_islands()
        islands_positions = list(map(lambda island: Position(island["x"], island["y"]), islands))
        islands_remoteness = list(map(lambda island_position: island_position.distance(treasure_position), islands_positions))
        closest_island_distance = min(islands_remoteness)
        path_ponderation = PONDERATION_FACTOR / closest_island_distance
        return path_ponderation

