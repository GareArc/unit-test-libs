import pytest
from src.algorithms.floyd_warshall import floyd_warshall

def test_basic_graph():
    graph = [
        [0, 5, float('inf'), 10],
        [float('inf'), 0, 3, float('inf')],
        [float('inf'), float('inf'), 0, 1],
        [float('inf'), float('inf'), float('inf'), 0]
    ]
    expected = [
        [0, 5, 8, 9],
        [float('inf'), 0, 3, 4],
        [float('inf'), float('inf'), 0, 1],
        [float('inf'), float('inf'), float('inf'), 0]
    ]
    assert floyd_warshall(graph) == expected

def test_single_vertex():
    graph = [[0]]
    assert floyd_warshall(graph) == [[0]]

def test_negative_weights():
    graph = [
        [0, -2, float('inf')],
        [float('inf'), 0, 3],
        [float('inf'), float('inf'), 0]
    ]
    expected = [
        [0, -2, 1],
        [float('inf'), 0, 3],
        [float('inf'), float('inf'), 0]
    ]
    assert floyd_warshall(graph) == expected

def test_complete_graph():
    graph = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]
    expected = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]
    assert floyd_warshall(graph) == expected

def test_disconnected_graph():
    graph = [
        [0, float('inf'), float('inf')],
        [float('inf'), 0, float('inf')],
        [float('inf'), float('inf'), 0]
    ]
    expected = [
        [0, float('inf'), float('inf')],
        [float('inf'), 0, float('inf')],
        [float('inf'), float('inf'), 0]
    ]
    assert floyd_warshall(graph) == expected

def test_original_not_modified():
    original = [[0, 5], [float('inf'), 0]]
    graph_copy = [row[:] for row in original]
    floyd_warshall(graph_copy)
    assert original == [[0, 5], [float('inf'), 0]]

def test_zero_weight_cycles():
    graph = [
        [0, 1, float('inf')],
        [float('inf'), 0, -1],
        [1, float('inf'), 0]
    ]
    expected = [
        [0, 1, 0],
        [0, 0, -1],
        [1, 2, 0]
    ]
    assert floyd_warshall(graph) == expected
