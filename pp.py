#!/usr/bin/python
from __future__ import division
import numpy as np
import math as m
import matplotlib.animation as animation
import matplotlib.pyplot as plt

time_step = 1
num_of_points_per_frame = 1
initial_size = 10
weib_par = 0.1
pareto_par = 1
MAX_ARRAY_SIZE = 10000

#gen_potential = lambda: np.random.pareto(pareto_par)
gen_potential = lambda: np.random.weibull(weib_par)

def a(time):
    return m.log(time) ** (1 / weib_par)


def d(time):
    return (1 / weib_par) * (m.log(time) ** (1 / weib_par - 1))


def rescale(x, time):
    return (x - a(time)) / d(time)


def psi_rescale(x, i, time):
    return (x - a(time) - abs(i) * m.log(m.log(time)) / (time * weib_par)) / d(time)


initial_time = initial_size
#initial_time = initial_size * time_step // (num_of_points_per_frame + 1)


def data_gen(framenumber, soln):
    ARR_LIMIT = initial_size + (framenumber + 3) * num_of_points_per_frame

    time = 2 * framenumber * time_step + initial_time
    pot_slice = np.concatenate([potential[-ARR_LIMIT:MAX_ARRAY_SIZE],
                                potential[:ARR_LIMIT]])
    points = [psi_rescale(x, i, time) for x, i in
              zip(pot_slice, range(-ARR_LIMIT, ARR_LIMIT))]
    ax_pp.set_xlim((-ARR_LIMIT, ARR_LIMIT))
    ax_pp.set_ylim((max(points) - 8, max(points) + 0.1))
    plot_pp.set_data(range(-ARR_LIMIT, ARR_LIMIT), points)

    time_step_pam = time_step // num_of_points_per_frame
    for i in range(num_of_points_per_frame):
        oldsoln = np.copy(soln)
        for n in range(-ARR_LIMIT + 1, ARR_LIMIT - 1):
            soln[n] = oldsoln[n] + time_step_pam * (
                        oldsoln[n] * (potential[n] - 2)
                        + oldsoln[n - 1] + oldsoln[n + 1])

        norm = soln.max()
        for x in np.nditer(soln, op_flags=['readwrite']):
            x[...] = x / norm

    ax_pam.set_xlim((-ARR_LIMIT, ARR_LIMIT))
    ax_pam.set_ylim((0,1))
    soln_slice = np.concatenate([soln[-ARR_LIMIT:MAX_ARRAY_SIZE],
                                 soln[:ARR_LIMIT]])
    plot_pam.set_data(range(-ARR_LIMIT, ARR_LIMIT), soln_slice)

    return plot_pp, plot_pam


potential = np.random.weibull(weib_par, (MAX_ARRAY_SIZE))

fig = plt.figure()
ax_pp = fig.add_subplot(121)
ax_pam = fig.add_subplot(122)
plot_pp, = ax_pp.plot([1], [1], 'ro', animated=True)
plot_pam, = ax_pam.plot([0], [0], linewidth=1.0, animated=True)
ax_pp.cla()

soln = np.zeros(MAX_ARRAY_SIZE)
soln[0] = 1

pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(soln, ),
                                  interval=10, blit=True)
plt.show()
