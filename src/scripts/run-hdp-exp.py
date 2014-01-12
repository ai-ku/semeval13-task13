#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import os
import numpy as np

#gammas = np.linspace(0.00001, 0.001, 10)
#print gammas
alphas = map(int, np.linspace(1, 30, 10))
print alphas

for a in  alphas[1:]:
    command = "make hdp.exp-alpha-{}".format(a)
    os.system(command)
