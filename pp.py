#!/usr/bin/python
from __future__ import division
import time
import numpy as np
import math as m
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from functools import partial
import weib
from bottleneck import partsort

time_step = 1
initial_time = 30
weib_par = 4.5
pareto_par = 1
MAX_ARRAY_SIZE = 10000
model = 0

# if weibul...
a = partial(weib.a, par=weib_par)
d = partial(weib.d, par=weib_par)
r = partial(weib.r, par=weib_par)


def rescale(x, t):
    return (x - a(t)) / d(t)


def psi_rescale(i, t, pot):
    size = len(pot) // 2
    if i != size - 1:
        nbgh1 = 1 / (pot[i] - pot[i + 1] + 2)
    else:
        nbgh1 = 0
    if i != -size:
        nbgh2 = 1 / (pot[i] - pot[i - 1] + 2)
    else:
        nbgh2 = 0
    return (pot[i] - a(t) + nbgh1 + nbgh2) / d(t) - abs(i) / (r(t) * weib_par)


def data_gen(framenumber, soln):
    curr_time = 2 * framenumber * time_step + initial_time
    ARR_LIMIT = int(m.log(m.log(curr_time)) * curr_time) // 2
    #ARR_LIMIT = 3 * int(r(curr_time)) // 2
    halfrt = int(r(curr_time)) // 2
    pot_slice = np.concatenate([potential[-ARR_LIMIT:MAX_ARRAY_SIZE],
                                potential[:ARR_LIMIT]])

    points = [0] * (2 * ARR_LIMIT)
    for i in (range(-ARR_LIMIT, ARR_LIMIT)):
        points[i] = psi_rescale(i, curr_time, potential)
    ax_pp.set_xlim((-ARR_LIMIT, ARR_LIMIT))
    #ax_pp.set_ylim((max(points) - 4, max(points) + 0.1))
    ax_pp.set_ylim((-10, 18))
    plot_pp.set_data(range(0, ARR_LIMIT) + range(-ARR_LIMIT, 0), points)
    line_max.set_data((-ARR_LIMIT, ARR_LIMIT), (max(points), max(points)))
    #line_sec.set_data((-ARR_LIMIT, ARR_LIMIT), (max(points), max(points)))

    if model:
        for i in range(2):
            oldsoln = np.copy(soln)
            for n in range(-halfrt, halfrt):
                soln[n] = oldsoln[n] + time_step * (
                    oldsoln[n] * (potential[n])
                    + oldsoln[n - 1] + oldsoln[n + 1])

            norm = soln.max()
            for x in np.nditer(soln, op_flags=['readwrite']):
                x[...] = x / norm

        ax_pam.set_xlim((-halfrt, halfrt))
        ax_pam.set_ylim((0, 1))
        soln_slice = np.concatenate([soln[-halfrt:MAX_ARRAY_SIZE],
                                    soln[:halfrt]])
        plot_pam.set_data(range(-halfrt, halfrt), soln_slice)
        return plot_pp, plot_pam
    else:
        return plot_pp, line_max

potential = np.random.weibull(weib_par, (MAX_ARRAY_SIZE))

fig = plt.figure()

if model:
    ax_pp = fig.add_subplot(121)
else:
    ax_pp = fig.add_subplot(111)

plot_pp, = ax_pp.plot([], [], 'r.', animated=True)
line_max = lines.Line2D([], [], color='black', animated=True)
line_sec = lines.Line2D([], [], color='black', animated=True)
ax_pp.cla()

if model:
    ax_pam = fig.add_subplot(122)
    plot_pam, = ax_pam.plot([], [], linewidth=1.0, animated=True)
soln = np.zeros(MAX_ARRAY_SIZE)
soln[0] = 1
initial_size = r(initial_time) // 2

ax_pp.add_line(line_max)
ax_pp.add_line(line_sec)

pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(soln, ),
                                  interval=4, blit=True)
plt.show()
