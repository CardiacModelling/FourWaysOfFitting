#!/usr/bin/env python3
#
# Compare method 2b results (single run) with method 2 (several runs)
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

method = 2

rows = []
rows.append([
    'Cell', 'Method ' + str(method) + '    ', 'Method ' + str(method) + 'b'])

for i in range(9):
    cell = i + 1

    e = results.load_errors(cell, method)
    b = results.load_errors(cell, method, start_from_m1=True)

    e = 'N/A         ' if len(e) == 0 else fmat.format(e[0])
    b = 'N/A         ' if len(b) == 0 else fmat.format(b[0])

    rows.append([str(cell) + '   ', e, b])

for row in rows:
    print('  '.join(row))

