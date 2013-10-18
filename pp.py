#!/usr/bin/python
from __future__ import division
import numpy as np
import math as m
import matplotlib.animation as animation
import matplotlib.pyplot as plt

time_step = 1
num_of_points_per_frame = 1
initial_size = 300
weib_par = 20
pareto_par = 1

#gen_potential = lambda: np.random.pareto(pareto_par)
gen_potential = lambda: np.random.weibull(weib_par)

def a(time):
    return m.log(time) ** (1 / weib_par)


def d(time):
    return (1 / weib_par) * (m.log(time) ** (1 / weib_par - 1))


def rescale(x, time):
    return (x - a(time)) / d(time)


def psi_rescale(x, i, time):
    return (x - a(time) - i * m.log(m.log(time)) / (time * weib_par)) / d(time)


initial_time = initial_size
#initial_time = initial_size * time_step // (num_of_points_per_frame + 1)


def data_gen(framenumber, pospotential, negpotential, soln):
    for i in range(num_of_points_per_frame):
        pospotential.append(gen_potential())
        negpotential.append(gen_potential())

    time = 2 * framenumber * time_step + initial_time
    points = [psi_rescale(x, i, time) for x, i in zip(pospotential,
                                                      range(len(pospotential)))]
    negpoints = [psi_rescale(x, i, time) for x, i in zip(negpotential,
                                                         range(len(negpotential)))]
    #ax.relim()
    #ax.autoscale_view()
    negpoints.reverse()
    ax_pp.set_xlim((-len(points), len(points)))
    ax_pp.set_ylim((max(negpoints + points) - 8, max(negpoints + points) +
                    0.1))
    plot_pp.set_data(range(-len(points), len(points)), negpoints + points)

    for i in range(num_of_points_per_frame):
        soln.append(0)
        oldsoln = soln[:]
        time_step_pam = time_step // num_of_points_per_frame
        # time_step_pam = time_step
        for n in range(1, len(pospotential) - 1):
            soln[n] = oldsoln[n] + time_step_pam * (
                        oldsoln[n] * (pospotential[n] - 2)
                        + oldsoln[n - 1] + oldsoln[n + 1])

        norm = max(soln)
        soln[:] = [x / norm for x in soln]
    ax_pam.set_xlim((-len(soln), len(soln)))
    ax_pam.set_ylim((0,1))
    plot_pam.set_data(range(len(soln)), soln)

    return plot_pp, plot_pam



pospotential, negpotential = [], []
for n in range(initial_size):
    pospotential.append(gen_potential())
    negpotential.append(gen_potential())

fig = plt.figure()
ax_pp = fig.add_subplot(121)
ax_pam = fig.add_subplot(122)
plot_pp, = ax_pp.plot([1], [1], 'ro', animated=True)
plot_pam, = ax_pam.plot([0], [0], linewidth=3.0, animated=True)
ax_pp.cla()

soln = [0] * (initial_size + num_of_points_per_frame)
soln[0] = 1

pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(pospotential,
                                                        negpotential, soln),
                                  interval=20, blit=True)
plt.show()
