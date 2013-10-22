#!/usr/bin/python
from __future__ import division
import numpy as np
import math as m
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.lines as ln
from functools import partial
import weib
import datetime
import os
from pylab import rand
from matplotlib.patches import Ellipse
from matplotlib import rc
rc('text', usetex=True)
rc('font', family='serif')

weib_par = 50
time = 10 ** 3
a = partial(weib.a, par=weib_par)
d = partial(weib.d, par=weib_par)
r = partial(weib.r, par=weib_par)
rescale = partial(weib.rescale, par=weib_par)
maxrandom = partial(weib.maxrandom, par=weib_par)
size = int(10 * r(time))

save = False


def psi_rescale(x, rt):
    return rescale(x, rt) - abs(x) / rt


#potential = np.zeros(2 * size)
#for i in range(2 * size):
    #print potential[i]
potential = np.random.weibull(weib_par, (2 * size))

fig = plt.figure()
ax = fig.add_subplot(111)
#el = Ellipse(xy=(-350, -6), width=800, height=10, angle=0, alpha=0.4)
#ax.text(-540, -2.5, "A", fontsize=25)
#ax.text(-100, 0.6, r'Number of points $\sim \mathrm{Poisson}(\int_{A} e^{-y})$', fontsize=14)
#ax.add_artist(el)
#ax.annotate("",
            #xy=(-550, -2), xycoords='data',
            #xytext=(-100, 0.8), textcoords='data',
            #arrowprops=dict(arrowstyle="fancy", color="0.5",
                            #connectionstyle="arc3, rad=0.3"),
            #)
ax.autoscale_view()
ax.set_ylim((-6, 4.0))
#ax.relim()
#ax.set_axis_off()
plot_pp, = ax.plot(range(-size, size), [psi_rescale(x, r(time)) for x in
                                        potential], 'r.', animated=False)

if save:
    basename = "pp"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix])
    plt.savefig(os.path.join("animations", filename + ".pdf"), format='PDF')
try:
    plt.show()
except AttributeError:
    pass
