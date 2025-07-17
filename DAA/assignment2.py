import heapq
import time

# ----------------- Task 1: Dijkstra using Adjacency List -----------------
def dijkstra_adj_list(n, graph, source):
    dist = [float('inf')] * n
    parent = [-1] * n
    visited = [False] * n
    dist[source] = 0

    for _ in range(n):
        u = -1
        min_dist = float('inf')
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                u = i
                min_dist = dist[i]

        if u == -1:
            break  # No reachable node left

        visited[u] = True
        for v, weight in graph[u]:
            if not visited[v] and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                parent[v] = u

    return dist, parent

# ----------------- Task 2: Dijkstra using Min-Heap -----------------
def dijkstra_min_heap(n, graph, source):
    dist = [float('inf')] * n
    parent = [-1] * n
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

# ----------------- Helper: Reconstruct Path -----------------
def get_path(parent, target):
    path = []
    while target != -1:
        path.append(target)
        target = parent[target]
    return path[::-1]

# ----------------- Helper: Take Input with Default Weight -----------------
def take_input():
    n = int(input("Enter number of vertices: "))
    m = int(input("Enter number of edges: "))
    graph = [[] for _ in range(n)]

    print("\nEnter the edges:")
    for _ in range(m):
        u = int(input("  From node: "))
        v = int(input("  To node: "))
        w_input = input(f"  Weight of edge ({u}, {v}) [Press Enter for default weight 1]: ").strip()
        w = int(w_input) if w_input else 1
        graph[u].append((v, w))
        # Uncomment if the graph is undirected
        # graph[v].append((u, w))

    source = int(input("\nEnter the source vertex: "))
    return n, graph, source

# ----------------- Run Both Tasks -----------------
def run_experiment():
    n, graph, source = take_input()

    # ----- Task 1: Adjacency List -----
    print("\n--- Dijkstra Using Adjacency List ---")
    start1 = time.time()
    dist1, parent1 = dijkstra_adj_list(n, graph, source)
    end1 = time.time()

    for i in range(n):
        path = get_path(parent1, i)
        print(f"Vertex {i}: Distance = {dist1[i]}, Path = {' -> '.join(map(str, path))}")
    print(f"Execution Time: {end1 - start1:.6f} seconds")

    # ----- Task 2: Min-Heap -----
    print("\n--- Dijkstra Using Min-Heap ---")
    start2 = time.time()
    dist2, parent2 = dijkstra_min_heap(n, graph, source)
    end2 = time.time()

    for i in range(n):
        path = get_path(parent2, i)
        print(f"Vertex {i}: Distance = {dist2[i]}, Path = {' -> '.join(map(str, path))}")
    print(f"Execution Time: {end2 - start2:.6f} seconds")

# ----------------- Main -----------------
run_experiment()

#Enter number of vertices: 4
#Enter number of edges: 4

#From node: 0
#To node: 1
#Weight: 1
#From node: 0
#To node: 2
#Weight: 4
#From node: 1
#To node: 2
#Weight: 2
#From node: 1
#To node: 3
#Weight: 5

#Enter the source vertex: 0

#Shortest paths from source vertex 0:
#Vertex 0: Distance = 0, Path = 0
#Vertex 1: Distance = 1, Path = 0 -> 1
#Vertex 2: Distance = 3, Path = 0 -> 1 -> 2
#Vertex 3: Distance = 6, Path = 0 -> 1 -> 3

#Execution Time: 0.000041 seconds
