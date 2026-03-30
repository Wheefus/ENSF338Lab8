class GraphNode:
    def __init__(self, data):
        self.data = data
        self.edges = []

class GraphEdge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

class Graph:
    def __init__(self):
        self.nodes = []
    
    def addNode(self, data):
        new_node = GraphNode(data)
        self.nodes.append(new_node)
        return new_node

    def removeNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
        # Remove edges associated with the node
        for edge in node.edges:
            if edge.node1 == node:
                edge.node2.edges.remove(edge)
            elif edge.node2 == node:
                edge.node1.edges.remove(edge)
    
    def addEdge(self, n1, n2, weight):
        new_edge = GraphEdge(n1, n2, weight)
        n1.edges.append(new_edge)
        n2.edges.append(new_edge)
    
    def removeEdge(self, n1, n2):
        for edge in n1.edges:
            if edge.node2 == n2:
                n1.edges.remove(edge)
                n2.edges.remove(edge)
                break
    
    def importFromFile(self, file):
        self.nodes = []  # Clear existing nodes
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if '->' in line:  # Edge definition
                    parts = line.split('->')
                    n1_data = parts[0].strip()
                    n2_data = parts[1].strip().split()[0]  # Get node2 data
                    weight = int(parts[1].strip().split()[1])  # Get weight
                    n1 = self.addNode(n1_data)
                    n2 = self.addNode(n2_data)
                    self.addEdge(n1, n2, weight)

# Implements the following methods:
 
# addNode(data)
# : creates a new graph node internally storing the string
# passed as parameter. Returns a GraphNode object

    
    
 
# removeNode(node)
# : removes the node
    
 
# addEdge(n1, n2, weight)
# : creates an edge between nodes
# n1 and n2
    
 
# removeEdge(n1, n2)
# : removes the edge between nodes
# n1 and n2
    

# importFromFile(file):
 
# imports a graph description from a
# GraphViz file.
# files define a simple format for graph description. You will not
# need to implement all the features of the GraphViz format,
# only basic ones described below. 
# The method clears all existing nodes and edges, and replaces them
# with those listed in the file.
    


## Testing
if __name__ == "__main__":
    graph = Graph()
    node1 = graph.addNode("A")
    node2 = graph.addNode("B")
    graph.addEdge(node1, node2, 5)
    print(f"Node1: {node1.data}, Node2: {node2.data}, Edge Weight: {node1.edges[0].weight}")
    print(f"Node1 Edges: {len(node1.edges)}, Node2 Edges: {len(node2.edges)}")