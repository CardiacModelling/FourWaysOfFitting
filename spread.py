#!/usr/bin/env python3
#
# Dispersion of good results, per method, per cell
#
from __future__ import division, print_function
import os
import sys
import myokit
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('python')))
import results


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 0:
    print('Syntax: ' + base + '.py')
    sys.exit(1)


fmat1 = ' {:<1.2e}'
fmat2 = '{:>2.6f}'

# Analyse obtained parameters
data = []
for cell in range(1, 11):
    row = [cell]
    for method in [2, 3, 4]:
        imethod = method - 1

        # Get scores, parameters
        rs, ps, es, ts, ns = results.load(cell, method)
        if len(rs) == 0:
            row.extend([0, 0, 0])
            continue

        # Get scores within 1% of best
        ies = es / es[0] - 1 < 0.01
        es = es[ies]

        # Get relative deviation of parameters within this subset
        ps = ps[ies]
        ps = np.abs(ps / ps[0] - 1)

        # Add max deviation for all e-close parameters
        value = 100 * np.max(ps)
        if value < 0.1:
            row.append(fmat1.format(value))
        else:
            row.append(fmat2.format(value))
        row.append(len(ps))

        # Count n with max deviation also < 1%
        ips = np.max(ps, axis=1) < 0.01
        ps = ps[ips]
        row.append(len(ps))

    data.append(row)


# Pad table and print
rows = [['Cell', 'M2', 'n', 'c', 'M3', 'n', 'c', 'M4', 'n', 'c']]
rows += [[str(x) for x in row] for row in data]

widths = [0] * len(rows[0])
for row in rows:
    for i, x in enumerate(row):
        widths[i] = max(len(x), widths[i])

for row in rows:
    for i, w in enumerate(widths):
        row[i] += ' ' * (w - len(row[i]))
    print(' | '.join(row))

