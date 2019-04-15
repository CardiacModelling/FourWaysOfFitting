#!/usr/bin/env python3
#
# Perform a 'direct fit', using method 1.
#
#
#
from __future__ import division, print_function
import myokit
import numpy as np
import os
import sys

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import sumstat


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 1:
    print('Syntax: ' + base + '.py <cell|all>')
    sys.exit(1)

if args[0] == 'all':
    cell_list = range(1, 10)
else:
    cell_list = [int(args[0])]


for cell in cell_list:
    print('Selected cell ' + str(cell))

    # Calculate summary statistics
    ta, tr, ai, ri, iv = sumstat.all_summary_statistics(cell)

    # Perform direct fit
    direct = sumstat.direct_fit_logarithmic(ta, tr, ai, ri, iv)
    for i, p in enumerate(direct):
        print('p' + str(1 + i) + ' = ' + str(p))

    # Estimate conductance
    print('Estimating conductance')
    g = sumstat.fit_conductance_to_iv_curve(cell, direct)
    print(g)

    # Store parameters
    parameters = direct + [g]
    fname = 'cell-' + str(cell) + '-fit-1.txt'
    print('Storing parameters (with g) in ' + fname)
    with open(fname, 'w') as f:
        for p in parameters:
            f.write(myokit.strfloat(p) + '\n')

