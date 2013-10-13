#!/usr/bin/python
from __future__ import division
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import numpy as np

size = 30
time_step = 0.1
weib_par = 1.5
pareto_par = 1
plot_args = {'rstride': 1, 'cstride': 1, 'cmap':
             cm.bwr, 'linewidth': 0.01, 'antialiased': True, 'color': 'w',
             'shade': True}


def data_gen(framenumber, soln, plot):
    oldsoln = np.copy(soln)
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            soln[i, j] = oldsoln[i, j] + time_step * (
                potential[i, j] * oldsoln[i, j]
                + oldsoln[i - 1, j] + oldsoln[i + 1, j]
                + oldsoln[i, j - 1] + oldsoln[i, j + 1]
                - 4 * oldsoln[i, j])
    norm = soln.max()
    for x in np.nditer(soln, op_flags=['readwrite']):
        x[...] = x / norm
    ax.clear()
    plot = ax.plot_surface(X, Y, soln, **plot_args)
    return plot,


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d([0.0, size])
ax.set_ylim3d([0.0, size])
ax.set_zlim3d(1.0)
ax.set_zlabel('renormolised solution')
ax.set_title('Parabolic Anderson Model')

potential = np.random.weibull(weib_par, (size, size))
#potential = np.random.pareto(pareto_par, (size, size))
# potential = np.zeros((size, size))

soln = np.zeros((size, size))
midpoint = size // 2
soln[midpoint, midpoint] = 1

X = range(size)
Y = range(size)
X, Y = np.meshgrid(X, Y)
plot = ax.plot_surface(X, Y, soln, **plot_args)

counter = 0
pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(soln, plot),
                                  interval=30, blit=False)
#pam_ani.save('pamPareto.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
