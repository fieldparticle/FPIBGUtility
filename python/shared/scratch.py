import numpy as np
import matplotlib.pyplot as plt
n= 50
x = np.linspace(0, 2 * np.pi, n)
y = np.sin(x)
mx = np.max(x)
nx = np.min(x)
my = max (y)
ny = min (y)

fig, ax = plt.subplots()
plt.plot(nx,ny, mx,my) # keeps the rectangle from changing size
for i in range(1,n):
    plt.plot(x[i],y[i],'k.')
    plt.pause(0.001)
plt.show()
    