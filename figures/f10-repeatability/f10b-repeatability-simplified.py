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
fig.subplots_adjust(0.12, 0.21, 0.985, 0.98)

ax = fig.add_subplot(1, 1, 1)

ax.set_ylabel(r'Results within 1% of best (%)    ')

colors1 = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]
colors2 = [
    'tab:blue',
    '#ffbe86',
    'tab:green',#'#95cf95',
    'tab:red',#'#ea9293',
]

xticks = []
xtickl = []
for method in [2, 3, 4]:
    imethod = method - 1

    # Count number of scores that were the same
    eclose = []
    pclose = []
    for cell in 1 + np.arange(9):

        # Get scores
        rs, ps, es, ts, ns = results.load(cell, method)
        if len(rs) == 0:
            eclose.append(0)
            pclose.append(0)
            continue

        # Count how many scores were within 1% of best
        i = es / es[0] - 1 < 0.01
        es = es[i]
        ps = ps[i]
        eclose.append(100 * len(es) / len(rs))

        # Count how many results were also close in parameter space
        #ds = np.max(ps / ps[0] - 1, axis=1)
        #ds = ds[ds < 0.01]
        #pclose.append(100 * len(ds) / len(rs))

    # Y-position for bar charts
    d = 1 / 11
    x = method + d * (np.arange(9) - 4)

    kargs = {
        'align': 'center',
        'edgecolor': 'k',
        'width': d,
    }

    #kargs['alpha'] = 0.5
    kargs['color'] = colors1[imethod],
    ax.bar(x, eclose, **kargs)

    #kargs['alpha'] = 1
    #kargs['color'] = colors2[imethod],
    #ax.bar(x, pclose, **kargs)

    xticks.extend(x)
    xtickl.extend([str(1 + i) for i in range(9)])

ax.set_ylim(0, 102)

ax.set_xticks(xticks)
ax.set_xticklabels(xtickl)

ypos = -25
ax.text(2, ypos, 'Method 2', horizontalalignment='center')
ax.text(3, ypos, 'Method 3', horizontalalignment='center')
ax.text(4, ypos, 'Method 4', horizontalalignment='center')

# Store
name = base
fig.savefig(name + '.png')
fig.savefig(name + '.pdf')
fig.savefig(name + '.eps')

