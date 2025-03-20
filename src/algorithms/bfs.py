from collections import deque


def bfs_traversal(graph: dict[str, list[str]], start: str) -> list[str]:
    """
    Perform BFS traversal on a graph represented as an adjacency list.
    Returns the order in which nodes are visited.
    """
    visited = []
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.append(vertex)
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
    return visited
