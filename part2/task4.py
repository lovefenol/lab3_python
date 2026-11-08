import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, dblquad

I1, err1 = quad(lambda x: x * np.sin(x), 0, np.pi)
print(f"интеграл 1: {I1:.10f}, точное значение {np.pi:.10f}, погрешность {abs(I1 - np.pi):.2e}")

I2, err2 = dblquad(lambda y, x: x + y, 0, 1, lambda x: 0, lambda x: x)
print(f"интеграл 2: {I2:.10f}, точное значение 0.5, погрешность {abs(I2 - 0.5):.2e}")

rng = np.random.default_rng(42)
N_list = [10**3, 10**4, 10**5, 10**6]
errors = []

for N in N_list:
    x = rng.random(N)
    y = rng.random(N)
    estimate = np.mean((x + y) * (y <= x))
    errors.append(abs(estimate - 0.5))
    print(f"N = {N:>7}: оценка {estimate:.5f}, погрешность {errors[-1]:.2e}")

plt.loglog(N_list, errors, "o-", label="погрешность Монте-Карло")
plt.loglog(N_list, 1 / np.sqrt(N_list), "--", color="gray", label="1/sqrt(N) для сравнения")
plt.xlabel("N")
plt.ylabel("абсолютная погрешность")
plt.title("зависимость погрешности от числа точек")
plt.grid(True, which="both")
plt.legend()
plt.show()