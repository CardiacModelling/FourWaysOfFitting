#!/usr/bin/env python3
#
# Compare method 2b results (single run) with method 2 (50 runs)
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

print('Cell  Method 2      Method 2b')
for i in range(9):
    cell = i + 1

    # Get method 2 best result
    e2 = results.load_errors(cell, 2)[0]

    # Get method 2b best result
    with open('cell-' + str(cell) + '-fit-2b-errors.txt', 'r') as f:
        e2b = float(f.readlines()[0])

    print(str(cell) + '     ' + fmat.format(e2) + '  ' + fmat.format(e2b))
