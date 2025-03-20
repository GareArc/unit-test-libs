def floyd_warshall(graph: list[list[float]]) -> list[list[float]]:
    """
    Computes the shortest distances between every pair of vertices in a
    weighted graph (possibly containing edges with negative weights but no
    negative cycles) using the Floyd-Warshall algorithm.
    'graph' is given as a 2D matrix; graph[u][v] = weight from u to v.
    Returns a distance matrix (2D list).
    """
    # Make a copy so we don't mutate the original
    dist = [row[:] for row in graph]
    n = len(dist)
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

