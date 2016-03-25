import requests
from pathfinding.polygon import Polygon


class WorldmapService:
    def __init__(self, host, port):
        self.worldmap_objects = {}
        while not self.worldmap_objects:
            try:
                self.worldmap_objects = requests.get('http://' + host + ':' + port + '/worldmap').json()
            except requests.exceptions.RequestException:
                print('can\'t fetch islands http://'+ host + ':' + port + '/worldmap' + ' is not available')
        self.polygons = []
        self.__robot_fetch_islands__()
        self.__create_polygon_list__()

    def get_polygons(self):
        return self.polygons

    def get_treasures(self):
        return self.treasures

    def __robot_fetch_islands__(self):
        self.circles = self.worldmap_objects['circles']
        self.pentagons = self.worldmap_objects['pentagons']
        self.squares = self.worldmap_objects['squares']
        self.triangles = self.worldmap_objects['triangles']
        self.treasures = self.worldmap_objects['treasures']

    def __create_polygon_list__(self):
        self.polygons.extend([Polygon(circle['x'], circle['y'], circle['radius'] + 40) for circle in self.circles])
        self.polygons.extend([Polygon(pentagon['x'], pentagon['y'], 70) for pentagon in self.pentagons])
        self.polygons.extend([Polygon(square['x'], square['y'], 70) for square in self.squares])
        self.polygons.extend([Polygon(triangle['x'], triangle['y'], 70) for triangle in self.triangles])