import heapq
import time
import statistics
import matplotlib.pyplot as plt


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
        new_node = GraphNode(data)
        self.nodes.append(new_node)
        return new_node

    def addEdge(self, n1, n2, weight):
        new_edge = GraphEdge(n1, n2, weight)
        n1.edges.append(new_edge)
        n2.edges.append(new_edge)

    # -------- IMPORT FOR .DOT FORMAT -------- #
    def importFromFile(self, file):
        self.nodes = []
        node_map = {}

        with open(file, 'r') as f:
            for line in f:
                line = line.strip()

                # Only process edges
                if '--' not in line:
                    continue

                # Example: 0 -- 557 [weight=45];
                parts = line.split('--')
                n1_data = parts[0].strip()

                right = parts[1].strip()

                # Extract node2
                n2_data = right.split('[')[0].strip()

                # Extract weight
                weight_part = right.split('weight=')[1]
                weight = int(weight_part.split(']')[0])

                # Create nodes if needed
                if n1_data not in node_map:
                    node_map[n1_data] = self.addNode(n1_data)
                if n2_data not in node_map:
                    node_map[n2_data] = self.addNode(n2_data)

                # Add edge
                self.addEdge(node_map[n1_data], node_map[n2_data], weight)

        print("Loaded nodes:", len(self.nodes))


    # -------- SLOW DIJKSTRA -------- #
    def slowSP(self, start):
        dist = {node: float('inf') for node in self.nodes}
        dist[start] = 0

        visited = set()
        queue = self.nodes[:]

        while queue:
            current = min(queue, key=lambda n: dist[n])
            queue.remove(current)

            visited.add(current)

            for edge in current.edges:
                neighbor = edge.node2 if edge.node1 == current else edge.node1

                if neighbor in visited:
                    continue

                new_dist = dist[current] + edge.weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist

        return dist


    # -------- FAST DIJKSTRA (FIXED) -------- #
    def fastSP(self, start):
        dist = {node: float('inf') for node in self.nodes}
        dist[start] = 0

        visited = set()
        heap = [(0, id(start), start)]  # tie-breaker added

        while heap:
            current_dist, _, current = heapq.heappop(heap)

            if current_dist > dist[current]:
                continue

            if current in visited:
                continue

            visited.add(current)

            for edge in current.edges:
                neighbor = edge.node2 if edge.node1 == current else edge.node1

                new_dist = current_dist + edge.weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, id(neighbor), neighbor))

        return dist


# -------- PERFORMANCE -------- #
def measure_performance(graph):
    slow_times = []
    fast_times = []

    if not graph.nodes:
        print("Graph is empty! Check file parsing.")
        return slow_times, fast_times

    for node in graph.nodes:
        # slow
        start = time.perf_counter()
        graph.slowSP(node)
        slow_times.append(time.perf_counter() - start)

        # fast
        start = time.perf_counter()
        graph.fastSP(node)
        fast_times.append(time.perf_counter() - start)

    return slow_times, fast_times


def print_stats(times, label):
    print(f"\n--- {label} ---")

    if not times:
        print("No data collected.")
        return

    print(f"Average: {statistics.mean(times):.6f}")
    print(f"Min:     {min(times):.6f}")
    print(f"Max:     {max(times):.6f}")


def plot_histogram(slow_times, fast_times):
    if not slow_times or not fast_times:
        print("Skipping plot (no data).")
        return

    plt.figure()

    plt.hist(slow_times, bins=20, alpha=0.5, label="SlowSP")
    plt.hist(fast_times, bins=20, alpha=0.5, label="FastSP")

    plt.xlabel("Execution Time (seconds)")
    plt.ylabel("Frequency")
    plt.title("Dijkstra Performance Comparison")
    plt.legend()

    plt.show()


# -------- MAIN -------- #
if __name__ == "__main__":
    g = Graph()

    g.importFromFile("random.dot")

    slow_times, fast_times = measure_performance(g)

    print_stats(slow_times, "SlowSP")
    print_stats(fast_times, "FastSP")

    plot_histogram(slow_times, fast_times)