import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Generate the vector data
x, y, z = np.meshgrid(np.arange(-2, 3, 1), np.arange(-2, 3, 1), np.arange(-2, 3, 1))
u = np.sin(x)
v = np.cos(y)
w = np.sin(z)

# Plot the vectors
ax.quiver(x, y, z, u, v, w)

# Set plot limits and labels
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()