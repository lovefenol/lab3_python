import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, Polygon, Arc

fig, ax = plt.subplots(figsize = (10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.set_aspect("equal")
ax.axis("off")

ax.add_patch(Rectangle((0, 0), 10, 7, color = "lightskyblue"))
ax.add_patch(Rectangle((0, 0), 10, 1, color = "dimgray"))
ax.add_patch(Circle((8.3, 6), 0.5, color = "gold"))
ax.add_patch(Arc((8.3, 6), 1.5, 1.5, theta1 = 0, theta2 = 360, color = "orange", linestyle = "--"))

ax.add_patch(Ellipse((2, 6.2), 1.8, 0.7, color = "white"))
ax.add_patch(Ellipse((2.6, 6.1), 1.2, 0.5, color = "white"))

ax.add_patch(Rectangle((0.5, 1), 1.6, 3, color = "slategray"))
ax.add_patch(Rectangle((2.5, 1), 1.4, 4.5, color = "gray"))
ax.add_patch(Rectangle((4.3, 1), 1.8, 2.5, color = "dodgerblue"))

ax.add_patch(Polygon([(4.3, 3.5), (6.1, 3.5), (5.2, 4.4)], color = "darkred"))

ax.add_patch(Rectangle((0.8, 2.8), 0.4, 0.5, color = "yellow"))
ax.add_patch(Rectangle((1.4, 2.8), 0.4, 0.5, color = "yellow"))
ax.add_patch(Rectangle((2.8, 4.2), 0.4, 0.5, color = "yellow"))
ax.add_patch(Rectangle((2.8, 3.0), 0.4, 0.5, color = "yellow"))
ax.add_patch(Rectangle((4.7, 2.4), 0.4, 0.5, color = "yellow"))

ax.add_patch(Rectangle((8.4, 1), 0.2, 1, color = "saddlebrown"))
ax.add_patch(Circle((8.5, 2.3), 0.6, color = "forestgreen"))

ax.set_title("Городской пейзаж")

fig.savefig("img/task3.png", dpi = 150)
plt.show()