#!/usr/bin/env python3
#
# Number of repeats that gave the same result, per cell, per method
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
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import results


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) > 0:
    print('Syntax: ' + base)
    sys.exit(1)

cell_list = list(range(1, 10))


# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)


# Create figure
fig = plt.figure(figsize=mm(82, 35), dpi=200)
fig.subplots_adjust(0.1, 0.18, 0.985, 0.99)

ax = fig.add_subplot(1, 1, 1)

ax.set_ylabel(r'RMSE withint 1% of best')

colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

xticks = []
xtickl = []
for method in [2, 3, 4]:
    imethod = method - 1

    # Count number of scores that were the same
    ns = []
    ms = []
    for cell in 1 + np.arange(9):

        # Get scores
        fs = results.load_errors(cell, method)

        # Cut-off at 1% deviation
        c = 1e-2

        # Count how many scores were the same
        n = np.sum(fs / fs[0] - 1 < 1e-2)
        ns.append(n)
        ms.append(len(fs))

    # Y-position for bar charts
    d = 1 / 11
    x = method + d * (np.arange(9) - 4)

    kargs = {
        'align': 'center',
        'edgecolor': 'k',
        'width': d,
        'color': colors[imethod],
        'alpha': 0.15,
    }
    ax.bar(x, ms, **kargs)
    kargs['alpha'] = 1
    ax.bar(x, ns, **kargs)

    xticks.extend(x)
    xtickl.extend([str(1 + i) for i in range(9)])

ax.set_xticks(xticks)
ax.set_xticklabels(xtickl)

ax.text(2, -11, 'Method 2', horizontalalignment='center')
ax.text(3, -11, 'Method 3', horizontalalignment='center')
ax.text(4, -11, 'Method 4', horizontalalignment='center')

# Store
name = base
fig.savefig(name + '.png')
fig.savefig(name + '.pdf')

