import urllib, json
from pathfinding.pathfinding import Cell, Mesh, polygon

class Islands:
    def __init__(self):
        islands_string = urllib.request.urlopen('http://localhost:5000/worldmap').read()
        self.islands = json.loads(islands_string.decode('utf-8'))
        self.polygons = []
        self.__robot_fetch_islands__()
        self.__create_polygon_list__()

    def __robot_fetch_islands__(self):
        self.circles = self.islands['circles']
        self.pentagons = self.islands['pentagons']
        self.squares = self.islands['squares']
        self.triangles = self.islands['triangles']

    def create_mesh_with_islands(self):
        cell = Cell(960,500,300,200)
        #mesh = Mesh(cell.partitionCells([polygon(200,200,50), polygon(400,200,50), polygon(400,50,50)],10))
        mesh = Mesh(cell.partitionCells(self.polygons,10))
        return mesh

    def __create_polygon_list__(self):
        self.polygons.extend([polygon(circle['x'], circle['y'], circle['radius']) for circle in self.circles])
        self.polygons.extend([polygon(pentagon['x'], pentagon['y'], 30) for pentagon in self.pentagons])
        self.polygons.extend([polygon(square['x'], square['y'], 30) for square in self.squares])
        self.polygons.extend([polygon(triangle['x'], triangle['y'], 30) for triangle in self.triangles])