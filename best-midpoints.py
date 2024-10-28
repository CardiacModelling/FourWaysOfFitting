#!/usr/bin/env python3
#
# Table: Best midpoints for all 9 cells, for all 4 methods.
#
from __future__ import division, print_function
import os
import sys
import numpy as np

# Load project modules
sys.path.append(os.path.abspath(os.path.join('python')))
import results

# Parameter formatting string
fmat = '{:<2.1f}'

# Load and format parameters
tables = []
for icell in range(10):
    cell = 1 + icell
    head = ['Cell ' + str(cell)]
    body = [['V_a'], ['V_i']]
    for imethod in range(4):
        method = 1 + imethod
        head.append('Method ' + str(method))
        parameters = results.load_parameters(cell, method)
        a1, a2, a3, a4 = [np.log(x) for x in parameters[0:8:2]]
        b1, b2, b3, b4 = parameters[1::2]
        body[0].append(fmat.format((a2 - a1) / (b1 + b2)))
        body[1].append(fmat.format((a4 - a3) / (b3 + b4)))

    tables.append([head] + body)

# Print parameters
for i, table in enumerate(tables):
    print()
    ncol = [0] * len(table[0])
    for row in table:
        for i, col in enumerate(row):
            if len(col) > ncol[i]:
                ncol[i] = len(col)
    for row in table:
        row = [col + ' ' * (n - len(col)) for col, n in zip(row, ncol)]
        print(' | '.join(row))

