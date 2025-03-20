import pytest
from src.algorithms.merge_sort import merge_sort, merge

def test_merge_sort_empty_list():
    assert merge_sort([]) == []

def test_merge_sort_single_element():
    assert merge_sort([1]) == [1]

def test_merge_sort_already_sorted():
    assert merge_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

def test_merge_sort_reverse_sorted():
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

def test_merge_sort_random_order():
    assert merge_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

def test_merge_sort_duplicate_elements():
    assert merge_sort([2, 2, 2, 2]) == [2, 2, 2, 2]

def test_merge_sort_negative_numbers():
    assert merge_sort([-3, -1, -4, -1, -5]) == [-5, -4, -3, -1, -1]

def test_merge_sort_mixed_numbers():
    assert merge_sort([-2, 0, 3, -1, 4]) == [-2, -1, 0, 3, 4]

def test_merge_empty_lists():
    assert merge([], []) == []

def test_merge_one_empty_list():
    assert merge([1, 3, 5], []) == [1, 3, 5]
    assert merge([], [2, 4, 6]) == [2, 4, 6]

def test_merge_equal_length_lists():
    assert merge([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

def test_merge_different_length_lists():
    assert merge([1, 3], [2, 4, 6, 8]) == [1, 2, 3, 4, 6, 8]
    assert merge([1, 3, 5, 7], [2, 4]) == [1, 2, 3, 4, 5, 7]

def test_merge_with_duplicates():
    assert merge([1, 2, 2], [2, 3, 3]) == [1, 2, 2, 2, 3, 3]

def test_merge_negative_numbers():
    assert merge([-3, -1], [-2, 0]) == [-3, -2, -1, 0]

def test_merge_mixed_numbers():
    assert merge([-2, 1, 4], [-3, 0, 2]) == [-3, -2, 0, 1, 2, 4]
