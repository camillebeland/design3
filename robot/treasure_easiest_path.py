from utils.position import Position

from sys import maxint

class TreasureEasiestPath:
    def __init__(self, pathfinder=None, worldmap=None):
        self.__pathfinder = pathfinder
        self.__worldmap = worldmap
        self.__infinity = maxint

    def find_easiest_treasure_from(self, position, target_island_position):
        treasures = self.__worldmap.get_treasures()
        treasures_positions = list(map(lambda treasure: Position(treasure['x'], treasure['y']), treasures))
        paths = list(map(lambda treasure_position: {'length': self.__find_path_length(position, treasure_position, target_island_position), 'treasure': pos}, treasures_positions))
        return min(paths, key=lambda x: x['length'])['treasure']


    def __find_path_length(self, robot_position, treasure_position, target_island_position):
        try:
            path_length_to_treasure = len(self.__pathfinder.find_path(robot_position, treasure_position))
            path_length_to_island = len(self.__pathfinder.find_path(treasure_position, target_island_position))
            path_length = path_length_to_island + path_length_to_treasure
        except:
            path_length = maxint
        return path_length

    def reset_attributes(self, pathfinder, worldmap):
        self.__pathfinder = pathfinder
        self.__worldmap = worldmap
