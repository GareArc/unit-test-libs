import pytest
from src.algorithms.dijkstra import dijkstra

def test_basic_graph():
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2)],
        'E': [('C', 10), ('D', 2)]
    }
    result = dijkstra(graph, 'A')
    assert result == {'A': 0, 'B': 3, 'C': 2, 'D': 8, 'E': 10}

def test_single_node():
    graph = {'A': []}
    result = dijkstra(graph, 'A')
    assert result == {'A': 0}

def test_disconnected_graph():
    graph = {
        'A': [('B', 1)],
        'B': [('A', 1)],
        'C': []
    }
    result = dijkstra(graph, 'A')
    assert result == {'A': 0, 'B': 1, 'C': float('inf')}

def test_cyclic_graph():
    graph = {
        'A': [('B', 1)],
        'B': [('C', 2)],
        'C': [('A', 3)]
    }
    result = dijkstra(graph, 'A')
    assert result == {'A': 0, 'B': 1, 'C': 3}

def test_negative_weights():
    graph = {
        'A': [('B', -1)],
        'B': [('C', -2)],
        'C': []
    }
    result = dijkstra(graph, 'A')
    assert result == {'A': 0, 'B': -1, 'C': -3}

def test_multiple_paths():
    graph = {
        'A': [('B', 2), ('C', 4)],
        'B': [('C', 1)],
        'C': []
    }
    result = dijkstra(graph, 'A')
    assert result == {'A': 0, 'B': 2, 'C': 3}

def test_large_graph():
    graph = {str(i): [(str(j), abs(i-j)) for j in range(100) if i != j] for i in range(100)}
    result = dijkstra(graph, '0')
    assert result['0'] == 0
    assert result['99'] == 99
    assert len(result) == 100

def test_self_loops():
    graph = {
        'A': [('A', 1), ('B', 2)],
        'B': [('B', 3)]
    }
    result = dijkstra(graph, 'A')
    assert result == {'A': 0, 'B': 2}

def test_empty_graph():
    with pytest.raises(KeyError):
        dijkstra({}, 'A')

def test_invalid_source():
    graph = {'A': [('B', 1)], 'B': []}
    with pytest.raises(KeyError):
        dijkstra(graph, 'C')
