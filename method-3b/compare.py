#!/usr/bin/env python3
#
# Compare method 3b results (single run) with method 3 (50 runs)
#
from __future__ import division, print_function
import os
import sys
import pints
import numpy as np
import myokit

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import results

fmat = '{:<1.10f}'

print('Cell  Method 3      Method 3b')
for i in range(9):
    cell = i + 1

    # Get method 3 best result
    e3 = results.load_errors(cell, 3)[0]

    # Get method 3b best result
    with open('cell-' + str(cell) + '-fit-3b-errors.txt', 'r') as f:
        e3b = float(f.readlines()[0])

    print(str(cell) + '     ' + fmat.format(e3) + '  ' + fmat.format(e3b))
