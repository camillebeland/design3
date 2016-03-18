import requests
from pathfinding.polygon import Polygon


class IslandsService:
    def __init__(self, host, port):
        try:
            self.islands = requests.get('http://'+ host + ':' + port + '/worldmap').json()
        except requests.exceptions.RequestException:
            print('can\'t fetch islands http://'+ host + ':' + port + '/worldmap' + ' is not available')
            self.islands = {'circles':[],'pentagons':[],'squares':[],'triangles':[]}
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
        self.polygons.extend([Polygon(circle['x'], circle['y'], circle['radius'] + 40) for circle in self.circles])
        self.polygons.extend([Polygon(pentagon['x'], pentagon['y'], 70) for pentagon in self.pentagons])
        self.polygons.extend([Polygon(square['x'], square['y'], 70) for square in self.squares])
        self.polygons.extend([Polygon(triangle['x'], triangle['y'], 70) for triangle in self.triangles])
