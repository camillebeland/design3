import networkx as nx

class Graph:
    def __init__(self, mesh):
        self.graph = nx.Graph()
        for node in mesh:
            self.graph.add_node(node)
            for other_node in mesh:
                if(node.is_adjacent_to(other_node)):
                    self.graph.add_edge(node, other_node)

    def getnodes(self):
        return self.graph.nodes()

    def getedges(self):
        return self.graph.edges()
