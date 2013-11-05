#!/usr/bin/python
from __future__ import division
from functools import partial
import math as m
import weib
import numpy as np

weib_par = 2.5
size = 100000

def psi_rescale(x, i, t):
    return x - abs(i) * m.log(m.log(size)) / (weib_par * size)


def psi_rescale_new(x, i, t):
    return psi_rescale(x, i, t) + 1 / x


for i in range(5):
    potential = np.random.weibull(weib_par, (size))
    potential = [x for x in potential if x > 0.5]
    size = len(potential)
    psi = [psi_rescale(x, i, size) for x, i in zip(potential, range(len(potential)))]
    psi_new = [psi_rescale_new(x, i, size) for x, i in zip(potential, range(len(potential)))]

    print np.argmax(psi), np.argmax(psi_new)
    print np.max(psi), np.max(psi_new)
