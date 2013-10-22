#!/usr/bin/python
from __future__ import division
import time
import numpy as np
import math as m
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.lines as ln
from functools import partial
import weib
import datetime
import os

time_step = 1
initial_time = 100
weib_par = 50
pareto_par = 1
MAX_ARRAY_SIZE = 10000
model = False
save = False
blit = True

linestyle_max = {'color': 'black', 'ls': '--', 'lw': 2, 'animated': blit}
linestyle_sec = {'color': 'green', 'ls': ':', 'lw': 2, 'animated': blit}

# if weibul...
a = partial(weib.a, par=weib_par)
d = partial(weib.d, par=weib_par)
r = partial(weib.r, par=weib_par)
rescale = partial(weib.rescale, par=weib_par)


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
    return (pot[i] - a(r(t)) + nbgh1 + nbgh2) / d(r(t)) - abs(i) / r(t)


def data_gen(framenumber, soln):
    global plot_pp, plot_pam, plot_pp_max, plot_pp_sec, lines

    curr_time = 2 * framenumber * time_step + initial_time
    size = int(m.log(m.log(curr_time)) * curr_time) // 2
    halfrt = int(r(curr_time)) // 2

    points = [0] * (2 * size)
    max_points = [float("-inf"), float("-inf")]
    max_index = [0, 0]
    for i in (range(-size, size)):
        points[i] = psi_rescale(i, curr_time, potential)
        if points[i] > max_points[0]:
            max_points[1] = max_points[0]
            max_index[1] = max_index[0]
            max_index[0] = i
            max_points[0] = points[i]
        else:
            if points[i] > max_points[1]:
                max_index[1] = i
                max_points[1] = points[i]
    if blit:
        for index in max_index:
            points[index] = float("-inf")
        plot_pp.set_data(range(0, size) + range(-size, 0), points)
        lines[0].set_data((-size, size), (max_points[1],
                                                    max_points[1]))
        plot_pp_max.set_data([max_index[0]], [max_points[0]])
        plot_pp_sec.set_data([max_index[1]], [max_points[1]])
    else:
        ax_pp.clear()
        ax_pp.set_title("Rescaled point process in PAM")
        plot_pp, = ax_pp.plot(range(0, size) + range(-size, 0),
                              points, 'r.')
        plot_pp_max, = ax_pp.plot([max_index[0]], [max_points[0]])
        plot_pp_sec, = ax_pp.plot([max_index[1]], [max_points[1]])
        lines[0] = ln.Line2D([(-size, size)], (max_points[1],
                                                         max_points[1]),
                             **linestyle_sec)
        ax_pp.add_line(lines[0])

    ax_pp.set_xlim((-size, size))
    ax_pp.set_ylim((max_points[0] - 10, max_points[0] + 1))
    #ax_pp.set_axis_off()
    #ax_pp.set_ylim(0, 1)

    if model:
        for i in range(2):
            oldsoln = np.copy(soln)
            for n in range(-halfrt, halfrt):
                soln[n] = oldsoln[n] + time_step * (
                    oldsoln[n] * (potential[n])
                    + oldsoln[n - 1] + oldsoln[n + 1])

            norm = max(soln)
            for x in np.nditer(soln, op_flags=['readwrite']):
                x[...] = x / norm

        soln_slice = np.concatenate([soln[-halfrt:MAX_ARRAY_SIZE],
                                    soln[:halfrt]])
        if blit:
            plot_pam.set_data(range(-halfrt, halfrt), soln_slice)
        else:
            plot_pam, = ax_pp.plot(range(-halfrt, halfrt), soln_slice,
                                   linewidth=1.0)

        return lines + [plot_pp_max, plot_pp_sec] + [plot_pp, plot_pam]
    else:
        return lines + [plot_pp_max, plot_pp_sec] + [plot_pp]

potential = np.random.weibull(weib_par, (MAX_ARRAY_SIZE))

fig = plt.figure()

ax_pp = fig.add_subplot(111)
plot_pp, = ax_pp.plot([], [], 'r.', animated=blit)
plot_pp_max, = ax_pp.plot([], [], 'bo', animated=blit)
plot_pp_sec, = ax_pp.plot([], [], 'go', animated=blit)
lines = [ln.Line2D([], [], **linestyle_sec)]
ax_pp.add_line(lines[0])

plot_pam, = ax_pp.plot([], [], linewidth=1.0, animated=blit)

soln = np.zeros(MAX_ARRAY_SIZE)
soln[0] = 1
initial_size = r(initial_time) // 2

for line in lines:
    ax_pp.add_line(line)

pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(soln, ),
                                  interval=4, blit=blit, frames=600)
if save:
    basename = "pp"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix])
    pam_ani.save(os.path.join("animations", filename + ".mp4"),
                 writer="ffmpeg", fps=30, bitrate=20000)

try:
    plt.show()
except AttributeError:
    pass
