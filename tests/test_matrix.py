import pytest
from src.helpers.matrix import matrix_add, matrix_multiply, matrix_transpose, matrix_determinant

def test_matrix_add_valid():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    expected = [[6, 8], [10, 12]]
    assert matrix_add(A, B) == expected

def test_matrix_add_empty():
    with pytest.raises(ValueError):
        matrix_add([], [[1, 2]])

def test_matrix_add_mismatched_dimensions():
    A = [[1, 2], [3, 4]]
    B = [[1, 2, 3], [4, 5, 6]]
    with pytest.raises(ValueError):
        matrix_add(A, B)

def test_matrix_multiply_valid():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    expected = [[19, 22], [43, 50]]
    assert matrix_multiply(A, B) == expected

def test_matrix_multiply_empty():
    with pytest.raises(ValueError):
        matrix_multiply([], [[1, 2]])

def test_matrix_multiply_mismatched_dimensions():
    A = [[1, 2], [3, 4]]
    B = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(ValueError):
        matrix_multiply(A, B)

def test_matrix_multiply_different_dimensions():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[1, 2], [3, 4], [5, 6]]
    expected = [[22, 28], [49, 64]]
    assert matrix_multiply(A, B) == expected

def test_matrix_transpose_valid():
    A = [[1, 2, 3], [4, 5, 6]]
    expected = [[1, 4], [2, 5], [3, 6]]
    assert matrix_transpose(A) == expected

def test_matrix_transpose_empty():
    assert matrix_transpose([]) == []

def test_matrix_transpose_square():
    A = [[1, 2], [3, 4]]
    expected = [[1, 3], [2, 4]]
    assert matrix_transpose(A) == expected

def test_matrix_determinant_1x1():
    assert matrix_determinant([[5]]) == 5

def test_matrix_determinant_2x2():
    A = [[1, 2], [3, 4]]
    assert matrix_determinant(A) == -2

def test_matrix_determinant_3x3():
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert matrix_determinant(A) == 0

def test_matrix_determinant_empty():
    with pytest.raises(ValueError):
        matrix_determinant([])

def test_matrix_determinant_non_square():
    A = [[1, 2, 3], [4, 5, 6]]
    with pytest.raises(ValueError):
        matrix_determinant(A)
