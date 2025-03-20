import pytest
from src.algorithms.bfs import bfs_traversal


def test_basic_bfs():
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    assert bfs_traversal(graph, 'A') == ['A', 'B', 'C', 'D', 'E', 'F']


def test_single_node():
    graph = {'A': []}
    assert bfs_traversal(graph, 'A') == ['A']


def test_linear_graph():
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    assert bfs_traversal(graph, 'A') == ['A', 'B', 'C', 'D']


def test_disconnected_graph():
    graph = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C']
    }
    assert bfs_traversal(graph, 'A') == ['A', 'B']


def test_cyclic_graph():
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'C'],
        'C': ['A', 'B']
    }
    assert bfs_traversal(graph, 'A') == ['A', 'B', 'C']


def test_self_loop():
    graph = {
        'A': ['A', 'B'],
        'B': ['A']
    }
    assert bfs_traversal(graph, 'A') == ['A', 'B']


def test_multiple_paths():
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }
    assert bfs_traversal(graph, 'A') == ['A', 'B', 'C', 'D']


def test_empty_neighbors():
    graph = {
        'A': [],
        'B': [],
        'C': []
    }
    assert bfs_traversal(graph, 'A') == ['A']
