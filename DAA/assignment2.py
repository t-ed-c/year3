import heapq
import time

# Task 1: Dijkstra using Adjacency List (without heap)
def dijkstra_adj_list(n, graph, source):
    dist = [float('inf')] * n
    dist[source] = 0
    visited = [False] * n

    for _ in range(n):
        # Find unvisited node with the smallest distance
        u = -1
        min_dist = float('inf')
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                u = i
                min_dist = dist[i]

        if u == -1:
            break  # No reachable unvisited nodes left

        visited[u] = True
        for v, weight in graph[u]:
            if not visited[v] and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight

    return dist

# Task 2: Dijkstra using Min-Heap (Priority Queue)
def dijkstra_min_heap(n, graph, source):
    dist = [float('inf')] * n
    dist[source] = 0
    pq = [(0, source)]  # Min-heap: (distance, node)

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > dist[u]:
            continue  # Outdated entry

        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))

    return dist

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

# Experiment runner
def run_experiment():
    n, graph, source = take_input()

    print("\n--- Running Dijkstra with Adjacency List ---")
    start1 = time.time()
    dist_list = dijkstra_adj_list(n, graph, source)
    end1 = time.time()
    print("Shortest distances:", dist_list)
    print(f"Execution Time: {end1 - start1:.6f} seconds")

    print("\n--- Running Dijkstra with Min-Heap ---")
    start2 = time.time()
    dist_heap = dijkstra_min_heap(n, graph, source)
    end2 = time.time()
    print("Shortest distances:", dist_heap)
    print(f"Execution Time: {end2 - start2:.6f} seconds")

# Run the program
run_experiment()
