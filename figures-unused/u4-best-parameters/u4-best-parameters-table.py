#!/usr/bin/env python3
#
# Table: Synthetic data study, real parameters and pararms for fits within 1%
# of the best fit.
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


pfmat = '{:<1.5e}'
efmat = '{:<1.8e}'
cell = 10



rows = []

# Add header row
cols = [''] + ['p' + str(i) for i in range(9)] + ['score']
rows.append(cols)

# Add true parameters row
assert cell == 10
ps = results.load_kylie_parameters(5)
cols = ['True'] + [pfmat.format(p) for p in ps] + ['']
rows.append(cols)

# Add method 2-4 parameters
for method in [2, 3, 4]:
    imethod = method - 1

    # Get scores, parameters, etc.
    rs, ps, es, ts, ns = results.load(cell, method)

    if len(rs):

        # Cut-off at 1% deviation
        ies = es / es[0] - 1 < 1e-2     # 50 True/Falses
        ies = np.arange(len(es))[ies]   # N indices 0, 1, 2, ...

        # Add parameter rows
        for i in ies:
            cols = ['M' + str(method) + ' #' + str(1 + i)]

            cols.extend([pfmat.format(p) for p in ps[i]])
            cols.append(efmat.format(es[i]))
            rows.append(cols)

    else:

        pass




# Show table
for row in rows:
    print(' & '.join(row) + r' \\')
    pass

