# Topological sorting can be implemented using Depth-First Search (DFS).
# This works because DFS naturally explores nodes before backtracking.
# By adding each node to a stack after visiting all its neighbors,
# we ensure that all predecessors of a node are processed before the node itself.
# This guarantees a valid topological ordering in a Directed Acyclic Graph (DAG).


# -------- GRAPH IMPLEMENTATION -------- #
class GraphNode:
    def __init__(self, data):
        self.data = data
        self.neighbors = []  # directed edges

    def __repr__(self):
        return str(self.data)


class Graph:
    def __init__(self):
        self.nodes = []

    def addNode(self, data):
        node = GraphNode(data)
        self.nodes.append(node)
        return node

    def addEdge(self, n1, n2):
        # directed edge: n1 -> n2
        n1.neighbors.append(n2)

    # -------- CHECK IF DAG -------- #
    def isdag(self):
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in node.neighbors:
                if neighbor not in visited:
                    if not dfs(neighbor):
                        return False
                elif neighbor in rec_stack:
                    return False  # cycle detected

            rec_stack.remove(node)
            return True

        for node in self.nodes:
            if node not in visited:
                if not dfs(node):
                    return False

        return True

    # -------- TOPOLOGICAL SORT -------- #
    def toposort(self):
        # Step 1: check if DAG
        if not self.isdag():
            return None

        visited = set()
        stack = []

        def dfs(node):
            visited.add(node)

            for neighbor in node.neighbors:
                if neighbor not in visited:
                    dfs(neighbor)

            stack.append(node)  # add after visiting children

        for node in self.nodes:
            if node not in visited:
                dfs(node)

        stack.reverse()  # reverse to get correct order
        return stack


# -------- TEST -------- #
if __name__ == "__main__":
    g = Graph()

    A = g.addNode("A")
    B = g.addNode("B")
    C = g.addNode("C")
    D = g.addNode("D")
    E = g.addNode("E")

    # DAG example
    g.addEdge(A, B)
    g.addEdge(A, C)
    g.addEdge(B, D)
    g.addEdge(C, D)
    g.addEdge(D, E)

    print("Is DAG:", g.isdag())

    order = g.toposort()
    if order:
        print("Topological Order:", order)
    else:
        print("Graph has a cycle; no topological ordering.")