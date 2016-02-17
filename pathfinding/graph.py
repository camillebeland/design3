import networkx as nx

class PathFinder:
    def __init__(self, mesh):
        self.graph = nx.Graph()
        for node in mesh:
            self.graph.add_node(node)
            for other_node in mesh:
                if(node.is_adjacent_to(other_node)):
                    self.graph.add_edge(node, other_node)

    def find_path(self, from_point, to_point):
        from_cell = None
        to_cell = None
        for cell in self.graph.nodes():
            if(cell.contains_point(from_point)):
                from_cell = cell
            elif(cell.contains_point(to_point)):
                to_cell = cell

        cell_path = nx.astar_path(self.graph, from_cell, to_cell)
        path = list(map(lambda cell : (cell.x, cell.y), cell_path))
        path.pop(0)
        path.pop()
        path.insert(0,from_point)
        path.append(to_point)
        return path
