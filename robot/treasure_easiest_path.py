from utils.position import Position


class TreasureEasiestPath:
    def __init__(self, pathfinder=None, worldmap=None):
        self.__pathfinder = pathfinder
        self.__worldmap = worldmap

    def find_easiest_treasure_from(self, position, target_island_position):
        treasures = self.__worldmap.get_treasures()
        treasures_positions = list(map(lambda treasure : Position(treasure['x'], treasure['y']), treasures))
        paths = list(map(lambda pos : {'length' :len(self.__pathfinder.find_path(position, pos)) + len(self.__pathfinder.find_path(pos, target_island_position)), 'treasure' : pos}, treasures_positions))
        return min(paths, key=lambda x: x['length'])['treasure']
