#!/usr/bin/env python3
#
# Compare fits using any of the 5 criteria.
#
from __future__ import division, print_function
import myokit
import numpy as np
import os
import sys

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import errors
import results
import sumstat


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) not in (2, 3):
    print('Syntax: ' + base + '.py <cell|all> <criterium|all> <variant>')
    sys.exit(1)

if args[0] == 'all':
    cell_list = range(1, 10)
else:
    cell_list = [int(args[0])]

if args[1] == 'all':
    crit_list = range(1, 6)
else:
    crit_list = [int(args[1])]

variant = False
if len(args) == 3:
    variant = args[2] == 'variant'
if variant:
    print('Running for method 1b variant')

#
# Run
#
criteria = [errors.E1, errors.E2, errors.E3, errors.E4, errors.EAP]
for cell in cell_list:
    print('Selected cell ' + str(cell))

    # Load parameters
    ps = [results.load_parameters(cell, i) for i in [1, 2, 3, 4]]

    # Use method 1b instead of method 1
    if variant:
        ps[0] = results.load_parameters(cell, 1, method_1b=True)

    for icrit in crit_list:
        print('Validating on criterium ' + str(icrit))
        crit = criteria[icrit - 1]

        # Calculate errors
        f = crit(cell)
        fs = np.array([f(p) for p in ps])

        print('RMS errors:')
        print(fs[0])
        print(fs[1])
        print(fs[2])
        print(fs[3])

        rs = fs / np.min(fs)
        print('Relative RMS errors:')
        print(rs[0])
        print(rs[1])
        print(rs[2])
        print(rs[3])

        # Store rms errors
        fname = 'rms-errors-cell-' + str(cell)
        if variant:
            fname += '-with-1b'
        fname += '.csv'
        if os.path.isfile(fname):
            d = myokit.DataLog.load_csv(fname)
        else:
            d = myokit.DataLog()
        d['rms' + str(icrit)] = fs
        d['rms' + str(icrit) + '_rel'] = rs
        print('Saving rms to ' + fname)
        d.save_csv(fname)

