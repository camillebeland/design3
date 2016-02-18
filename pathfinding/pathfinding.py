import networkx as nx

class PathFinder:
    def __init__(self, graph):
        self.__graph = graph

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
