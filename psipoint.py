#!/usr/bin/python
from __future__ import division
import matplotlib.animation as animation
import datetime, os
import matplotlib.pyplot as plt
import matplotlib.axes as axes
from functools import partial
import math as m
import numpy as np
import weib

weib_par = 6
save = True
a = partial(weib.a, par=weib_par)
d = partial(weib.d, par=weib_par)
r = partial(weib.r, par=weib_par)
rescale = partial(weib.rescale, par=weib_par)

fig = plt.figure()
ax = fig.add_subplot(111)
#ax1 = axes.Axes(fig, [0, 0, 0, 0])

z = 10
xi = a(abs(z)) + 0.3
ran = [x ** 3 for x in range(int(30 ** (1 / 3)), int(10000 ** (1 / 3)))]
x = [abs(z) / r(t) for t in ran]
y = [rescale(xi, r(t)) - abs(z) / r(t) for t in ran]
ax.set_title("Trajectories of points in the transformed pointed process with time")
plot, = ax.plot([-s for s in x], y, 'r<')
plotl, = ax.plot([-s for s in x], y)
plot2, = ax.plot(x, y, 'r>')
plot2l, = ax.plot(x, y, 'b')
ax.relim()
ax.autoscale_view()
ax.set_axis_off()

if save:
    basename = "psi_trajectory"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix])
    plt.savefig(os.path.join("animations", filename + ".pdf"), format='PDF')

plt.show()
