import heapq


class GraphNode:
    def __init__(self, data):
        self.data = data
        self.edges = []

    def __repr__(self):
        return str(self.data)


class GraphEdge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight


class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        # Path compression
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 == root2:
            return False  # cycle detected

        # Union by rank
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

        return True


class Graph:
    def __init__(self):
        self.nodes = []

    def addNode(self, data):
        node = GraphNode(data)
        self.nodes.append(node)
        return node

    def addEdge(self, n1, n2, weight):
        edge = GraphEdge(n1, n2, weight)
        n1.edges.append(edge)
        n2.edges.append(edge)

    def getAllEdges(self):
        edges = set()
        for node in self.nodes:
            for edge in node.edges:
                edges.add(edge)
        return list(edges)

    # -------- KRUSKAL MST -------- #
    def mst(self):
        mst_graph = Graph()

        # Copy nodes
        node_map = {}
        for node in self.nodes:
            node_map[node] = mst_graph.addNode(node.data)

        # Get and sort edges
        edges = self.getAllEdges()
        edges.sort(key=lambda e: e.weight)

        uf = UnionFind(self.nodes)

        for edge in edges:
            if uf.union(edge.node1, edge.node2):
                mst_graph.addEdge(
                    node_map[edge.node1],
                    node_map[edge.node2],
                    edge.weight
                )

        return mst_graph


# -------- TEST -------- #
if __name__ == "__main__":
    g = Graph()

    A = g.addNode("A")
    B = g.addNode("B")
    C = g.addNode("C")
    D = g.addNode("D")
    E = g.addNode("E")

    g.addEdge(A, B, 1)
    g.addEdge(A, C, 3)
    g.addEdge(B, C, 2)
    g.addEdge(B, D, 4)
    g.addEdge(C, D, 5)
    g.addEdge(C, E, 6)
    g.addEdge(D, E, 7)

    mst = g.mst()

    print("MST Edges:")
    for node in mst.nodes:
        for edge in node.edges:
            if edge.node1 == node:
                print(f"{edge.node1} -- {edge.node2} (weight {edge.weight})")