#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import os
import numpy as np

gammas = np.linspace(0.001, 0.9, 15)
print gammas

for g in  gammas:
    command = "make hdp.exp-gamma-{}".format(g)
    os.system(command)
