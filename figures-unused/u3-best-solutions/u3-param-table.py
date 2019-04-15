#!/usr/bin/env python3
#
# Table: All parameters, all cells
#
from __future__ import division
from __future__ import print_function
import os
import sys
import numpy as np

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import results

# Filename
base = os.path.splitext(os.path.basename(__file__))[0]


fmat = '{:<1.3e}'

rows = []

# Header
row = ['Cell  ', 'Method  '] + ['p' + str(1 + i) for i in range(9)]
rows.append(row)

for cell in 1 + np.arange(9):
    for method in 1 + np.arange(4):
        row = []
        row.append('Cell ' + str(cell) if method == 1 else ' '*6)
        row.append('Method ' + str(method))

        parameters = results.load_parameters(cell, method)
        for p in parameters:
            row.append(fmat.format(p))
        rows.append(row)

# Show table
for row in rows:
    print(' & '.join(row) + r' \\')
