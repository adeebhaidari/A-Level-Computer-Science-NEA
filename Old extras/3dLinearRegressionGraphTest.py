from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# Parameters
theta0 = 1
theta1 = 2
theta2 = 3

# Input grid
x0 = np.linspace(0, 10, 50)
x1 = np.linspace(0, 10, 50)
X0, X1 = np.meshgrid(x0, x1)

# Linear regression plane
Y = theta0*X0 + theta1*X1 + theta2

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X0, X1, Y, alpha=0.7, cmap='viridis')
ax.set_xlabel('x0')
ax.set_ylabel('x1')
ax.set_zlabel('y')
plt.title('Linear Regression Plane')
plt.show()