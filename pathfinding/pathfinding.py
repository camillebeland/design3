import networkx
from utils.position import Position

class PathFinder:
    def __init__(self, mesh):
        self.__mesh = mesh
        self.__graph = networkx.Graph()
        for cell in mesh.get_cells():
            self.__graph.add_node(cell)
            for other_cell in mesh.get_cells():
                if cell.is_adjacent_to(other_cell):
                    self.__graph.add_edge(cell, other_cell)

    def get_mesh(self):
        return self.__mesh

    def find_path(self, from_point, to_point):
        from_cell = None
        to_cell = None
        for cell in self.__graph.nodes():
            if cell.contains_point(from_point):
                from_cell = cell
            if cell.contains_point(to_point):
                to_cell = cell

        cell_path = networkx.astar_path(self.__graph, from_cell, to_cell)
        path = list()
        for cell in cell_path:
            path.append(Position(cell.x, cell.y))
        if len(path) == 1:
            path.pop()
            path.append(to_point)
        else:
            path.pop(0)
            path.pop()
            path.insert(0, from_point)
            path.append(to_point)
        return path
