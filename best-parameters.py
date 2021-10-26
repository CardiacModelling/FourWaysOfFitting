#!/usr/bin/env python3
#
# Figure: Best parameters for all 9 cells, for all 4 methods, shows in a table.
#
from __future__ import division, print_function
import os
import sys
#import numpy as np

# Load project modules
sys.path.append(os.path.abspath(os.path.join('python')))
import results

# Parameter formatting string
pfmat = '{:<1.5e}'

# Load and format parameters
tables = []
for icell in range(9):
    cell = 1 + icell
    head = ['Cell ' + str(cell)]
    body = [['p' + str(1 + i)] for i in range(9)]
    for imethod in range(4):
        method = 1 + imethod
        head.append('Method ' + str(method))
        parameters = results.load_parameters(cell, method)
        for p, b in zip(parameters, body):
            b.append(pfmat.format(p))
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

