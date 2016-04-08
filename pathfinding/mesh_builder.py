from pathfinding.cell import Cell
from pathfinding.mesh import Mesh
from pathfinding.polygon import Polygon


class MeshBuilder:
    def __init__(self, table_corners, polygons):
        self.max_x = max(table_corners, key=lambda item: item[0])[0]
        self.max_y = max(table_corners, key=lambda item: item[1])[1]
        self.min_x = min(table_corners, key=lambda item: item[0])[0]
        self.min_y = min(table_corners, key=lambda item: item[1])[1]
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y
        self.x = self.width/2 + (1600 - self.max_x)
        self.y = self.height/2 + (1200 - self.max_y)

        self.polygons = polygons

        padding = 100

        top = Polygon(self.x, self.y + self.height / 2 + self.width / 2, self.width + padding)
        bottom = Polygon(self.x, self.y - self.height / 2 - self.width / 2, self.width + padding)
        left = Polygon(self.x - self.width / 2 - self.height / 2, self.y, self.height + padding)
        right = Polygon(self.x + self.width / 2 + self.height / 2, self.y, self.height + padding)

        self.polygons.extend([top, bottom, right, left])

        self.__create_cell__()

    def get_mesh(self):
        return Mesh(self.cell.partition_cells(self.polygons, 100))

    def __create_cell__(self):
        self.cell = Cell(self.width, self.height, self.x, self.y)
