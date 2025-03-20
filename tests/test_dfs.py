import pytest
from src.algorithms.dfs import dfs_traversal

def test_dfs_simple_path():
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'D', 'C']

def test_dfs_cyclic_graph():
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B']
    }
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'D', 'C']

def test_dfs_single_node():
    graph = {'A': []}
    assert dfs_traversal(graph, 'A') == ['A']

def test_dfs_disconnected_components():
    graph = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C']
    }
    assert dfs_traversal(graph, 'A') == ['A', 'B']

def test_dfs_linear_path():
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'C', 'D']

def test_dfs_complex_graph():
    graph = {
        'A': ['B', 'C', 'D'],
        'B': ['E', 'F'],
        'C': ['G'],
        'D': ['H'],
        'E': [],
        'F': [],
        'G': [],
        'H': []
    }
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'E', 'F', 'C', 'G', 'D', 'H']

def test_dfs_self_loop():
    graph = {
        'A': ['A', 'B'],
        'B': ['C'],
        'C': []
    }
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'C']

def test_dfs_empty_neighbors():
    graph = {
        'A': [],
        'B': [],
        'C': []
    }
    assert dfs_traversal(graph, 'A') == ['A']

def test_dfs_bidirectional_edges():
    graph = {
        'A': ['B'],
        'B': ['A', 'C'],
        'C': ['B']
    }
    assert dfs_traversal(graph, 'A') == ['A', 'B', 'C']

def test_dfs_invalid_start_node():
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': []
    }
    with pytest.raises(KeyError):
        dfs_traversal(graph, 'D')

def test_dfs_empty_graph():
    graph = {}
    with pytest.raises(KeyError):
        dfs_traversal(graph, 'A')
