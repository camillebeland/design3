from pathfinding.cell import Cell
from pathfinding.mesh import Mesh


class MeshBuilder:
    def __init__(self, table_corners, polygons):
        self.polygons = polygons
        self.__create_cell__(table_corners)

    def get_mesh(self):
        return Mesh(self.cell.partition_cells(self.polygons, 100))

    def __create_cell__(self, table_corners):
        max_x = max(table_corners, key=lambda item: item[0])[0]
        max_y = max(table_corners, key=lambda item: item[1])[1]
        min_x = min(table_corners, key=lambda item: item[0])[0]
        min_y = min(table_corners, key=lambda item: item[1])[1]
        width = max_x - min_x
        height = max_y - min_y
        self.cell = Cell(width, height, width/2 + (1600 - max_x), height/2 + (1200 - max_y))