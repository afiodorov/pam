from __future__ import division
import numpy as np
import math as m


def a(t, par):
    return m.log(t) ** (1 / par)


def d(t, par):
    return (1 / par) * (m.log(t) ** (1 / par - 1))


def r(t, par):
    return par * t * d(t, par) / m.log(m.log(t))


def rescale(x, t, par):
    return (x - a(t, par)) / d(t, par)


def maxrandom(n, par):
    u = np.random.uniform()
    return (-m.log(1 - u ** (1 / n))) ** (1 / par)
