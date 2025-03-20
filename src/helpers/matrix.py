from typing import List

Matrix = List[List[float]]


def matrix_add(A: Matrix, B: Matrix) -> Matrix:
    """
    Returns the element-wise sum of two matrices A and B.
    Raises ValueError if dimensions do not match.
    """
    if not A or not B or len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Matrix dimensions must match for addition.")
    rows = len(A)
    cols = len(A[0])
    return [
        [A[i][j] + B[i][j] for j in range(cols)]
        for i in range(rows)
    ]


def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """
    Returns the product of two matrices A (MxN) and B (NxP).
    Result is an MxP matrix.
    Raises ValueError if the inner dimensions do not match.
    """
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Inner dimensions must match for multiplication.")
    M = len(A)
    N = len(A[0])
    P = len(B[0])

    # Initialize result matrix with zeros
    result = [[0.0 for _ in range(P)] for _ in range(M)]
    for i in range(M):
        for j in range(P):
            for k in range(N):
                result[i][j] += A[i][k] * B[k][j]
    return result


def matrix_transpose(A: Matrix) -> Matrix:
    """
    Returns the transpose of matrix A.
    """
    if not A:
        return []
    rows = len(A)
    cols = len(A[0])
    return [
        [A[r][c] for r in range(rows)]
        for c in range(cols)
    ]


def matrix_determinant(A: Matrix) -> float:
    """
    Computes the determinant of a square matrix A using a
    recursive definition (not optimized for large matrices).
    Raises ValueError if A is not square.
    """
    n = len(A)
    if n == 0:
        raise ValueError("Cannot compute determinant of empty matrix.")
    for row in A:
        if len(row) != n:
            raise ValueError("Matrix must be square to compute determinant.")

    # Base case for 1x1 matrix
    if n == 1:
        return A[0][0]

    # Base case for 2x2 matrix
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]

    # General case (recursive)
    det = 0.0
    for col in range(n):
        # Minor of A[0][col]
        submatrix = [
            [A[i][j] for j in range(n) if j != col]
            for i in range(1, n)
        ]
        sign = (-1) ** col
        det += sign * A[0][col] * matrix_determinant(submatrix)
    return det
