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
if len(args) not in (2, 3):
    print('Syntax: ' + base + '.py <cell|all> <method> (kinetic)')
    sys.exit(1)

if args[0] == 'all':
    cell_list = range(1, 10)
else:
    cell_list = [int(x) for x in args[0].split(',')]

method = int(args[1])
assert(method in [2, 3, 4])

kinetic = False
if len(args) == 3:
    kinetic = args[2].lower() == 'kinetic'
if kinetic:
    print('Looking at "k-space" transformation')


# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Options
ftr = 'k' if kinetic else 'f'
baseline = [method, 'a', 'a']
options = [
    [
        [method, 'n', 'a'],
        [method, ftr, 'a'],
    ], [
        [method, 'a', 'n'],
        [method, 'a', ftr],
    ], [
        [method, 'n', 'n'],
        [method, ftr, ftr],
    ],
]
opt_labels = [
    'Searching',
    'Starting',
    'Both',
]

# Method colors
colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

def count(config):
    method, search, sample = config

    # Get scores
    rs, ps, es, ts, ns = results.load(cell, method, search, sample)
    if len(rs) == 0:
        return 0, 0

    # Count how many scores were within 1% of best
    i = es / es[0] - 1 < 0.01
    es = es[i]
    ps = ps[i]
    eclose = 100 * len(es) / len(rs)

    # Count how many results were also close in parameter space
    ds = np.max(ps / ps[0] - 1, axis=1)
    ds = ds[ds < 0.01]
    pclose = 100 * len(ds) / len(rs)

    return eclose, pclose


for cell in cell_list:
    # Create figure
    fig = plt.figure(figsize=mm(82, 40), dpi=200)
    fig.subplots_adjust(0.12, 0.19, 0.985, 0.99)
    grid = GridSpec(1, 1, hspace=0, wspace=0)
    ax = fig.add_subplot(grid[0, 0])
    ax.set_ylabel(r'Results within 1% of best (%)')

    xticks = []
    xtickl = []

    e, p = count(baseline)
    label = baseline[1] + ',' + baseline[2]

    xticks.append(0)
    xtickl.append(label)

    d = 1 / 3
    imethod = baseline[0] - 1
    kargs = {
        'align': 'center',
        'edgecolor': 'k',
        'width': d,
        'color': colors[imethod],
    }

    ax.bar([0], e, **kargs)
    ax.axhline(e, color='k', linestyle='--', zorder=0, lw=1)

    # Add bars for groups
    for irow, row in enumerate(options):

        # Count number of scores that were the same
        eclose = []
        pclose = []
        for config in row:
            e, p = count(config)
            eclose.append(e)
            pclose.append(p)
            xtickl.append(config[1] + ',' + config[2])

        # Y-position for bar charts
        x = 1 + irow + d * (np.arange(len(row)) - int(1 + np.floor(d / 2)))
        ax.bar(x, eclose, **kargs)
        xticks.extend(x)

    ax.set_ylim(0, 102)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtickl)

    #for iopt, label in enumerate(opt_labels):
    #    ax.text(iopt, -22, label, horizontalalignment='center')

    # Store
    name = base + '-cell-' + str(cell) + '-m' + str(method)
    if kinetic:
        name += '-kinetic'
    print('Saving results to ' + name)
    fig.savefig(name + '.png')
    fig.savefig(name + '.pdf')

