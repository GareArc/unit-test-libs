import heapq


def dijkstra(graph: dict[str, list[tuple[str, int]]], source: str) -> dict[str, int]:
    """
    Computes the shortest path distances from 'source' to all other nodes
    in a weighted graph using Dijkstra's algorithm.
    'graph' is in the form { node: [(neighbor, weight), ...], ... }
    Returns a dict of distances { node: distance }.
    """
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    visited = set()

    # Priority queue holds tuples of (distance, node)
    pq = [(0, source)]

    while pq:
        current_dist, node = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph[node]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances
