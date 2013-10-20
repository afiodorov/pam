#!/usr/bin/python
from __future__ import division
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import numpy as np
import datetime
import os

size = 30
time_step = 0.1
weib_par = 1.5
pareto_par = 1
save = 1
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
    ax.set_zlabel('renormolised solution')
    ax.set_title('Parabolic Anderson Model. Time: ' + str(framenumber))
    plot = ax.plot_surface(X, Y, soln, **plot_args)
    return plot,


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d([0.0, size])
ax.set_ylim3d([0.0, size])
ax.set_zlim3d([0.0, 1.0])

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

pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(soln, plot),
                                  interval=10, blit=False, frames=1000)

if save:
    basename = "pam"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix])
    pam_ani.save(os.path.join("animations", filename + ".mp4"),
                 writer="ffmpeg", fps=30, bitrate=20000)

# swallow .tk exception - I believe it is a bug in matplotlib
try:
    plt.show()
except AttributeError:
    pass
