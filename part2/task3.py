import numpy as np

A = np.array([[4, -1.5, 2, 0.5],
              [1, 5, -2, 1.2],
              [-2, 1, 6, -1],
              [0.5, 2, -1, 7]])
B = np.array([11.05, -6.82, 11.5, -0.5]).reshape(-1, 1)
det = np.linalg.det(A)
print("det(A) =", det)
if np.isclose(det, 0):
    raise SystemExit("det(A) = 0, система не имеет единственного решения")

print("cond(A) =", np.linalg.cond(A))
X1 = np.linalg.inv(A) @ B
X2 = np.linalg.solve(A, B)
print("норма разности решений:", np.linalg.norm(X1 - X2))
print("проверка ||A*X1 - B|| =", np.linalg.norm(A @ X1 - B))
print("проверка ||A*X2 - B|| =", np.linalg.norm(A @ X2 - B))
print("решение:", np.round(X2.ravel(), 1))