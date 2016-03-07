import urllib, json
from pathfinding.pathfinding import Cell, Mesh, polygon

class IslandsService:
    def __init__(self):
        islands_string = urllib.request.urlopen('http://localhost:5000/worldmap').read()
        self.islands = json.loads(islands_string.decode('utf-8'))
        self.polygons = []
        self.__robot_fetch_islands__()
        self.__create_polygon_list__()

    def get_polygons(self):
        return self.polygons

    def __robot_fetch_islands__(self):
        self.circles = self.islands['circles']
        self.pentagons = self.islands['pentagons']
        self.squares = self.islands['squares']
        self.triangles = self.islands['triangles']

    def __create_polygon_list__(self):
        self.polygons.extend([polygon(circle['x'], circle['y'], circle['radius'] + 20) for circle in self.circles])
        self.polygons.extend([polygon(pentagon['x'], pentagon['y'], 50) for pentagon in self.pentagons])
        self.polygons.extend([polygon(square['x'], square['y'], 50) for square in self.squares])
        self.polygons.extend([polygon(triangle['x'], triangle['y'], 50) for triangle in self.triangles])