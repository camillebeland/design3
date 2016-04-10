import networkx
from functools import reduce
from pathfinding.cell import Cell
from utils.position import Position


class PathFinder:
    def __init__(self, mesh, polygons=[]):
        self.__mesh = mesh
        self.__graph = networkx.Graph()
        for cell in mesh.get_cells():
            self.__graph.add_node(cell)
            for other_cell in mesh.get_cells():
                if cell.is_adjacent_to(other_cell):
                    self.__graph.add_edge(cell, other_cell)
        self.__obstacles = list(map(self.__polygon_to_cell, polygons))


    def __polygon_to_cell(self, polygon):
        return Cell(polygon.size, polygon.size, polygon.x, polygon.y)

    def get_mesh(self):
        return self.__mesh

    def any_obstacles_contains_point(self, point):
        any_obstacles_contains_point  = reduce(lambda x,y : x or y, map(lambda obstacle : obstacle.contains_point(point),self.__obstacles))
        return any_obstacles_contains_point

    def find_closest_node_to(self, point):
        closest_node = self.__graph.nodes()[0]
        smallest_distance = closest_node.distance(point)
        for node in self.__graph.nodes():
            new_distance = node.distance(point)
            if new_distance < smallest_distance:
                closest_node = node
                smallest_distance = new_distance
        return closest_node


    def find_path(self, from_point, to_point):
        from_cell = self.find_closest_node_to(from_point)
        to_cell = self.find_closest_node_to(to_point)

        try:
            cell_path = networkx.astar_path(self.__graph, from_cell, to_cell)
        except:
            raise Exception('No Path found!')
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
