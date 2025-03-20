import pytest
from src.algorithms.binary_search import binary_search

def test_binary_search_found():
    assert binary_search([1, 2, 3, 4, 5], 3) == 2

def test_binary_search_not_found():
    assert binary_search([1, 2, 3, 4, 5], 6) == -1

def test_binary_search_empty_list():
    assert binary_search([], 1) == -1

def test_binary_search_single_element_found():
    assert binary_search([1], 1) == 0

def test_binary_search_single_element_not_found():
    assert binary_search([1], 2) == -1

def test_binary_search_first_element():
    assert binary_search([1, 2, 3, 4, 5], 1) == 0

def test_binary_search_last_element():
    assert binary_search([1, 2, 3, 4, 5], 5) == 4

def test_binary_search_negative_numbers():
    assert binary_search([-5, -3, -1, 0, 2, 4], -3) == 1

def test_binary_search_duplicate_elements():
    assert binary_search([1, 2, 2, 2, 3], 2) in [1, 2, 3]

def test_binary_search_large_list():
    large_list = list(range(0, 1000000, 2))  # Even numbers from 0 to 999998
    assert binary_search(large_list, 500000) == 250000

@pytest.mark.skip(reason="Binary search requires sorted input")
def test_binary_search_unsorted_list():
    # Binary search requires sorted list
    result = binary_search([3, 1, 4, 2, 5], 4)
    assert result == -1
