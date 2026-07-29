def matmul(A, B):
    # A is m×n, B is n×p
    m, n = len(A), len(A[0])
    p = len(B[0])

    # initialise result matrix with zeros
    C = [[0 for _ in range(p)] for _ in range(m)]

    # triple‑loop multiplication
    for i in range(m):
        for j in range(p):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s

    return C
