import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-8, 8, 2000)

with np.errstate(divide = "ignore", invalid = "ignore"):
    y = 4 / (x**2 - 4)

y = np.ma.masked_where(np.abs(x**2 - 4) < 0.05, y)

fig, ax = plt.subplots()

ax.plot(x, y, label = "y = 4 / (x² − 4)")

ax.axvline(-2, color = "gray", linestyle = "--", label = "асимптоты x = ±2")
ax.axvline(2, color = "gray", linestyle = "--")
ax.set_ylim(-10, 10)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("y = 4 / (x² − 4)")
ax.grid(True)
ax.legend()

plt.show()