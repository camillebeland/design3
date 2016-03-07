import requests
from pathfinding.pathfinding import polygon

class IslandsService:
    def __init__(self):
        self.islands = []
        try:
            request = requests.get('http://localhost:5000/worldmap')
            self.islands = request.json()
        except requests.exceptions.RequestException as e:
            print(e)
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
        self.polygons.extend([polygon(circle['x'], circle['y'], circle['radius'] + 40) for circle in self.circles])
        self.polygons.extend([polygon(pentagon['x'], pentagon['y'], 70) for pentagon in self.pentagons])
        self.polygons.extend([polygon(square['x'], square['y'], 70) for square in self.squares])
        self.polygons.extend([polygon(triangle['x'], triangle['y'], 70) for triangle in self.triangles])