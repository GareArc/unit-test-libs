def dfs_traversal(graph: dict[str, list[str]], start: str) -> list[str]:
    """
    Perform DFS traversal on a graph represented as an adjacency list.
    Returns the order in which nodes are visited.
    """
    visited = []
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.append(vertex)
            # Add neighbors in reverse order so the leftmost neighbor is visited first
            for neighbor in reversed(graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)
    return visited
