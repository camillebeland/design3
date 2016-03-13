import networkx as nx
from functools import reduce


class PathFinder:
    def __init__(self, mesh):
        self.__graph = nx.Graph()
        for cell in mesh.get_cells():
            self.__graph.add_node(cell)
            for other_cell in mesh.get_cells():
                if cell.is_adjacent_to(other_cell):
                    self.__graph.add_edge(cell, other_cell)

    def find_path(self, from_point, to_point):
        from_cell = None
        to_cell = None
        for cell in self.__graph.nodes():
            if(cell.contains_point(from_point)):
                from_cell = cell
            if(cell.contains_point(to_point)):
                to_cell = cell

        cell_path = nx.astar_path(self.__graph, from_cell, to_cell)
        path = list(map(lambda cell : (cell.x, cell.y), cell_path))
        if(len(path) ==1):
            path.pop()
            path.append(to_point)
        else:
            path.pop(0)
            path.pop()
            path.insert(0,from_point)
            path.append(to_point)
        return path


class Cell:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def area(self):
        return self.width * self.height

    def split(self):
        return [
            Cell(self.width/2.0, self.height/2.0, self.x - self.width/4.0,self.y -self.height/4.0),
            Cell(self.width/2.0, self.height/2.0, self.x - self.width/4.0,self.y +self.height/4.0),
            Cell(self.width/2.0, self.height/2.0, self.x + self.width/4.0,self.y -self.height/4.0),
            Cell(self.width/2.0, self.height/2.0, self.x + self.width/4.0,self.y +self.height/4.0),
        ]

    def contains_any(self, obstacles):
        return reduce(lambda x,y : x or y,
                      map(self.contains, obstacles),
                      False
        )

    def __str__(self):
        return "({0},{1},{2},{3})".format(self.x, self.y, self.width, self.height)

    def contains(self, obstacle):
        return obstacle.contains(self)

    def contains_point(self, point):
        x, y = point
        return (x >= (self.x - self.width/2.0) and
                x <= (self.x + self.width/2.0) and
                y >= (self.y - self.height/2.0) and
                y <= (self.y + self.height/2.0))

    def is_adjacent_to(self, other_cell):
        return (((abs(self.x - other_cell.x) - (self.width + other_cell.width)/2.0) < 1e-6 and
                abs(self.y - other_cell.y) < (self.height + other_cell.height)/2.0) or
                ((abs(self.y - other_cell.y) - (self.height + other_cell.height)/2.0) < 1e-6 and
                abs(self.x - other_cell.x) < (self.width + other_cell.width)/2.0))

    def partitionCells(self, obstacles, area_treshold):
        if(self.area() < area_treshold):
            return []
        elif(self.contains_any(obstacles)):
            childCells = self.split()
            return reduce(lambda x, y: x+y,
                          map(lambda cell: cell.partitionCells(obstacles, area_treshold), childCells))
        else:
            return [self]


class Mesh:
    def __init__(self, cells):
        self.__cells = cells

    def get_cells(self):
        return self.__cells


class polygon:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def distance(self, target):
        return (self.x - target.x)**2 + (self.y - target.y)**2

    def contains(self, cell):
        return (abs(self.x - cell.x) <= (cell.width + self.size)/2.0 and
                abs(self.y - cell.y) <= (cell.height + self.size)/2.0)


