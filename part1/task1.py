import numpy as np
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)

xdeg = np.linspace(-360, 360, 1000)
xrad = np.deg2rad(xdeg)
p = np.exp(np.sin(xrad)) + np.log((np.sin(0.5 * xrad))**2 + 1) * np.cos(xrad)
q = - np.log((np.sin(xrad) - np.cos(xrad))**2 + 2) + 8

ax1.plot(xdeg, p, label = "p(x)")
ax1.legend()
ax1.set_xticks(np.arange(-360, 361, 90))
ax1.set_ylabel("y")
ax1.set_title("p(x) = e^(sin x) + ln(sin²(0.5x) + 1) · cos x")
ax1.grid(True)

ax2.plot(xdeg, q, label = "q(x)")
ax2.legend()
ax2.set_ylabel("y")
ax2.set_xlabel("x")
ax2.set_title("q(x) = −ln((sin x − cos x)² + 2) + 8")
ax2.grid(True)


plt.show()