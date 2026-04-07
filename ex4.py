import time
import statistics


# -------- ADJACENCY LIST GRAPH -------- #
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

    # -------- IMPORT (.dot format) -------- #
    def importFromFile(self, file):
        self.nodes = []
        node_map = {}

        with open(file, 'r') as f:
            for line in f:
                line = line.strip()

                if '--' not in line:
                    continue

                parts = line.split('--')
                n1_data = parts[0].strip()
                right = parts[1].strip()

                n2_data = right.split('[')[0].strip()
                weight = int(right.split('weight=')[1].split(']')[0])

                if n1_data not in node_map:
                    node_map[n1_data] = self.addNode(n1_data)
                if n2_data not in node_map:
                    node_map[n2_data] = self.addNode(n2_data)

                self.addEdge(node_map[n1_data], node_map[n2_data], weight)

    # -------- DFS (Adj List) -------- #
    def dfs(self):
        visited = set()
        result = []

        def visit(node):
            visited.add(node)
            result.append(node)

            for edge in node.edges:
                neighbor = edge.node2 if edge.node1 == node else edge.node1
                if neighbor not in visited:
                    visit(neighbor)

        for node in self.nodes:
            if node not in visited:
                visit(node)

        return result


# -------- ADJACENCY MATRIX GRAPH -------- #
class Graph2:
    def __init__(self):
        self.nodes = []
        self.index_map = {}
        self.matrix = []

    def addNode(self, data):
        node = data
        self.index_map[node] = len(self.nodes)
        self.nodes.append(node)

        # Expand matrix
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0] * len(self.nodes))

    def addEdge(self, n1, n2, weight):
        i = self.index_map[n1]
        j = self.index_map[n2]
        self.matrix[i][j] = weight
        self.matrix[j][i] = weight

    # -------- IMPORT (.dot format) -------- #
    def importFromFile(self, file):
        self.nodes = []
        self.index_map = {}
        self.matrix = []

        with open(file, 'r') as f:
            for line in f:
                line = line.strip()

                if '--' not in line:
                    continue

                parts = line.split('--')
                n1 = parts[0].strip()
                right = parts[1].strip()

                n2 = right.split('[')[0].strip()
                weight = int(right.split('weight=')[1].split(']')[0])

                if n1 not in self.index_map:
                    self.addNode(n1)
                if n2 not in self.index_map:
                    self.addNode(n2)

                self.addEdge(n1, n2, weight)

    # -------- DFS (Adj Matrix) -------- #
    def dfs(self):
        visited = set()
        result = []

        def visit(node):
            visited.add(node)
            result.append(node)

            i = self.index_map[node]

            for j, weight in enumerate(self.matrix[i]):
                if weight != 0:
                    neighbor = self.nodes[j]
                    if neighbor not in visited:
                        visit(neighbor)

        for node in self.nodes:
            if node not in visited:
                visit(node)

        return result


# -------- PERFORMANCE TEST -------- #
def measure_dfs(graph, runs=10):
    times = []

    for _ in range(runs):
        start = time.perf_counter()
        graph.dfs()
        times.append(time.perf_counter() - start)

    return times


def print_stats(times, label):
    print(f"\n--- {label} ---")
    print(f"Average: {statistics.mean(times):.6f}")
    print(f"Min:     {min(times):.6f}")
    print(f"Max:     {max(times):.6f}")


# -------- MAIN -------- #
if __name__ == "__main__":
    file = "random.dot"

    g1 = Graph()
    g1.importFromFile(file)

    g2 = Graph2()
    g2.importFromFile(file)

    times1 = measure_dfs(g1)
    times2 = measure_dfs(g2)

    print_stats(times1, "DFS (Adjacency List)")
    print_stats(times2, "DFS (Adjacency Matrix)")



# The adjacency list implementation is generally faster for DFS on sparse graphs.
# This is because it only iterates through actual neighbors of each node.

# The adjacency matrix implementation checks all possible nodes (entire row),
# even if most entries are 0 (no edge). This makes it less efficient for sparse graphs.

# Since the provided random.dot graph is sparse, the adjacency list DFS is expected
# to be faster than the adjacency matrix DFS.

# In dense graphs, however, the performance difference may decrease because the
# matrix will have fewer zero entries.