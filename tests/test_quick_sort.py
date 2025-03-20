import pytest
from src.algorithms.quick_sort import quick_sort

def test_quick_sort_empty_list():
    assert quick_sort([]) == []

def test_quick_sort_single_element():
    assert quick_sort([1]) == [1]

def test_quick_sort_sorted_list():
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

def test_quick_sort_reverse_sorted_list():
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

def test_quick_sort_duplicate_elements():
    assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

def test_quick_sort_negative_numbers():
    assert quick_sort([-5, -2, -8, -1, -9]) == [-9, -8, -5, -2, -1]

def test_quick_sort_mixed_numbers():
    assert quick_sort([3, -1, 0, 5, -2, 4, -6]) == [-6, -2, -1, 0, 3, 4, 5]

def test_quick_sort_all_same_elements():
    assert quick_sort([4, 4, 4, 4, 4]) == [4, 4, 4, 4, 4]

def test_quick_sort_two_elements():
    assert quick_sort([2, 1]) == [1, 2]
    assert quick_sort([1, 2]) == [1, 2]

def test_quick_sort_large_random_list():
    import random
    random.seed(42)  # For reproducibility
    input_list = [random.randint(-1000, 1000) for _ in range(1000)]
    sorted_list = sorted(input_list)
    assert quick_sort(input_list) == sorted_list
