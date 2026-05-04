
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    pq = [(0, start)]
    step = 1

    while pq:
        print(f"\n--- Step {step} ---")
        print("Priority Queue:", pq)
        print("Distances:", distances)

        current_distance, current_node = heapq.heappop(pq)
        print(f"Selected Node: {current_node} with distance {current_distance}")

        if current_distance > distances[current_node]:
            print("Skipped (better path already exists)")
            continue

        for neighbor, weight in graph[current_node]:
            new_distance = current_distance + weight
            print(f"Checking edge {current_node} -> {neighbor} with weight {weight}")

            if new_distance < distances[neighbor]:
                print(f"Updating distance of node {neighbor} from {distances[neighbor]} to {new_distance}")
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))
            else:
                print(f"No update needed for node {neighbor}")

        step += 1

    return distances


# -------- USER INPUT --------

n = int(input("Enter number of vertices: "))
e = int(input("Enter number of edges: "))

graph = {i: [] for i in range(n)}

print("Enter edges (u v w):")
for _ in range(e):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))
    graph[v].append((u, w))  # remove if directed graph

start = int(input("Enter source node: "))

# -------- RUN --------

result = dijkstra(graph, start)

print("\nFinal Shortest Distances:")
for node in result:
    print(f"{node} -> {result[node]}")
