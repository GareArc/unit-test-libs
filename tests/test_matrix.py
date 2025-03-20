import pytest
from src.helpers.matrix import matrix_add, matrix_multiply, matrix_transpose, matrix_determinant

def test_matrix_add_valid():
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[5.0, 6.0], [7.0, 8.0]]
    expected = [[6.0, 8.0], [10.0, 12.0]]
    assert matrix_add(A, B) == expected

def test_matrix_add_empty():
    with pytest.raises(ValueError):
        matrix_add([], [[1.0]])

    with pytest.raises(ValueError):
        matrix_add([[1.0]], [])

def test_matrix_add_mismatched_dimensions():
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[1.0], [2.0]]
    with pytest.raises(ValueError):
        matrix_add(A, B)

def test_matrix_multiply_valid():
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[5.0, 6.0], [7.0, 8.0]]
    expected = [[19.0, 22.0], [43.0, 50.0]]
    assert matrix_multiply(A, B) == expected

def test_matrix_multiply_empty():
    with pytest.raises(ValueError):
        matrix_multiply([], [[1.0]])

    with pytest.raises(ValueError):
        matrix_multiply([[1.0]], [])

def test_matrix_multiply_mismatched_dimensions():
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[1.0], [2.0], [3.0]]
    with pytest.raises(ValueError):
        matrix_multiply(A, B)

def test_matrix_multiply_non_square():
    A = [[1.0, 2.0, 3.0]]
    B = [[4.0], [5.0], [6.0]]
    expected = [[32.0]]
    assert matrix_multiply(A, B) == expected

def test_matrix_transpose_valid():
    A = [[1.0, 2.0], [3.0, 4.0]]
    expected = [[1.0, 3.0], [2.0, 4.0]]
    assert matrix_transpose(A) == expected

def test_matrix_transpose_empty():
    assert matrix_transpose([]) == []

def test_matrix_transpose_non_square():
    A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    expected = [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    assert matrix_transpose(A) == expected

def test_matrix_determinant_valid():
    A = [[1.0, 2.0], [3.0, 4.0]]
    assert matrix_determinant(A) == -2.0

    B = [[1.0, 2.0, 3.0],
         [4.0, 5.0, 6.0],
         [7.0, 8.0, 9.0]]
    assert matrix_determinant(B) == 0.0

def test_matrix_determinant_empty():
    with pytest.raises(ValueError):
        matrix_determinant([])

def test_matrix_determinant_non_square():
    A = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    with pytest.raises(ValueError):
        matrix_determinant(A)

def test_matrix_determinant_1x1():
    assert matrix_determinant([[5.0]]) == 5.0

def test_matrix_determinant_2x2():
    A = [[4.0, 3.0], [2.0, 1.0]]
    assert matrix_determinant(A) == -2.0
