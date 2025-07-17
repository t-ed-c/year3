import heapq
import time

# Modified Dijkstra using Min-Heap that tracks the path
def dijkstra_with_paths(n, graph, source):
    dist = [float('inf')] * n
    parent = [-1] * n  # Track the path
    dist[source] = 0
    pq = [(0, source)]  # (distance, node)

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, parent

# Reconstruct path from source to target using parent array
def get_path(parent, target):
    path = []
    while target != -1:
        path.append(target)
        target = parent[target]
    return path[::-1]  # reverse to get source -> target

# Input helper
def take_input():
    n = int(input("Enter number of vertices: "))
    m = int(input("Enter number of edges: "))
    graph = [[] for _ in range(n)]

    print("\nEnter the edges in format: u v weight")
    for _ in range(m):
        u = int(input("  From node: "))
        v = int(input("  To node: "))
        w = int(input(f"  Weight of edge ({u}, {v}): "))
        graph[u].append((v, w))
        # Uncomment below if the graph is undirected
        # graph[v].append((u, w))

    source = int(input("\nEnter the source vertex: "))
    return n, graph, source

# Main experiment runner
def run_experiment():
    n, graph, source = take_input()

    print("\n--- Running Dijkstra with Path Output ---")
    start = time.time()
    dist, parent = dijkstra_with_paths(n, graph, source)
    end = time.time()

    print(f"\nShortest paths from source vertex {source}:")
    for target in range(n):
        path = get_path(parent, target)
        print(f"Vertex {target}: Distance = {dist[target]}, Path = {' -> '.join(map(str, path))}")

    print(f"\nExecution Time: {end - start:.6f} seconds")

# Run the program
run_experiment()
