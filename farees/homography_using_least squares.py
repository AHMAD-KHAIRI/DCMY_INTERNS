import numpy as np

# Define Matrix A (18x6) with specific values
A = np.array([
    [70, 62, 1,     0, 0, 0],
    [0, 0, 0,       70, 62, 1],
    [645, 71, 1,    0, 0, 0],
    [0, 0, 0,       645, 71, 1,],
    [1251, 61, 1,   0, 0, 0],
    [0, 0, 0,       1251, 61, 1],
    [68, 144, 1,    0, 0, 0],
    [0, 0, 0,       68, 144, 1],
    [650, 150, 1,   0, 0, 0],
    [0, 0, 0,       650, 150, 1],
    [1254, 135,     1, 0, 0, 0],
    [0, 0, 0,       1254, 135, 1],
    [69, 217, 1,    0, 0, 0],
    [0, 0, 0,       69, 217, 1],
    [648, 231, 1,   0, 0, 0],
    [0, 0, 0,       648, 231, 1],
    [1260, 218, 1,  0, 0, 0],
    [0, 0, 0,       1260, 218, 1]
])  

# Define Matrix B (18x1) with specific values
B = np.array([
    [452],
    [-154],
    [458],
    [65],
    [457],
    [289],
    [484.4],
    [-155.2],
    [487],
    [66],
    [484.4],
    [290.1],
    [511],
    [-155],
    [517.7],
    [66.2],
    [515.5],
    [291.3]
])  

# 1. Transpose of A
A_transposed = A.T
print("A Transposed (A^T):")
print(A_transposed)

# 2. Compute (A^T A)
ATA = np.dot(A_transposed, A)
print("\n(A^T A):")
print(ATA)

# 3. Compute the inverse of (A^T A)
ATA_inv = np.linalg.inv(ATA)
print("\n(A^T A)^(-1):")
print(ATA_inv)

# 4. Compute A^T B
ATB = np.dot(A_transposed, B)
print("\n(A^T B):")
print(ATB)

# 5. Compute h = (A^T A)^(-1) A^T b
h = np.dot(ATA_inv, ATB)
print("\nh = (A^T A)^(-1) A^T B:")
print(h)

