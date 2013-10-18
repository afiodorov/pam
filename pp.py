#!/usr/bin/python
from __future__ import division
import numpy as np
import math as m
import matplotlib.animation as animation
import matplotlib.pyplot as plt

time_step = 1
weib_par = 20
num_of_points_per_frame = 10
initial_size = 300


def a(time):
    return m.log(time) ** (1 / weib_par)


def d(time):
    return (1 / weib_par) * (m.log(time) ** (1 / weib_par - 1))


def rescale(x, time):
    return (x - a(time)) / d(time)


def psi_rescale(x, i, time):
    return (x - a(time) - i * m.log(m.log(time)) / (time * weib_par)) / d(time)


initial_time = 1.2
#initial_time = initial_size * time_step // (num_of_points_per_frame + 1)


def data_gen(framenumber, potential):
    for i in range(num_of_points_per_frame):
        potential.append(np.random.weibull(weib_par))
    time = framenumber * time_step + initial_time
    #points = [rescale(x, time) for x in potential]
    points = [psi_rescale(x, i, time) for x, i in zip(potential,
                                                               range(len(potential)))]
    #ax.relim()
    #ax.autoscale_view()
    ax.set_xlim((1, len(points)))
    #ax.set_xlim((1, 100))
    ax.set_ylim((-10, 10))
    plot.set_data(range(len(points)), points)
    return plot,


potential = np.random.weibull(weib_par, initial_size).tolist()
points = [rescale(x, initial_time) for x in potential]

fig = plt.figure()
ax = fig.add_subplot(111)
plot, = plt.plot(range(initial_size), points, 'ro')
ax.cla()
pam_ani = animation.FuncAnimation(fig, data_gen, fargs=([potential]),
                                  interval=1, blit=True)
plt.show()
