#!/usr/bin/python
from __future__ import division
import numpy as np
import math as m
import matplotlib.animation as animation
import matplotlib.pyplot as plt

time_step = 0.1
weib_par = 2
num_of_points_per_frame = 0
initial_size = 3000


def rescale(x, time):

    def a(time):
        return m.log(time) ** (1 / weib_par)

    def d(time):
        return (1 / weib_par) * m.log(time) ** (1 / weib_par - 1)

    return (x - a(time)) / d(time)


initial_time = initial_size * time_step // (num_of_points_per_frame + 1)


def data_gen(framenumber, potential, plot):
    for i in range(num_of_points_per_frame):
        potential.append(np.random.weibull(weib_par))
    time = framenumber * time_step + time_step + initial_time
    points = [rescale(x, time) for x in potential]
    #ax.relim()
    #ax.autoscale_view()
    plot.set_data(range(len(points)), points)
    return plot,


potential = np.random.weibull(weib_par, initial_size).tolist()
points = [rescale(x, initial_time) for x in potential]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim((0, 4))
plot, = plt.plot(range(initial_size), points, 'ro')
pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(potential, plot),
                                  interval=10, blit=True)
plt.show()
