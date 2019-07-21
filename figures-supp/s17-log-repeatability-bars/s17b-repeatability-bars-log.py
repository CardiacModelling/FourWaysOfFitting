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



full_with_conductance = False



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
    cell_list = [int(x) for x in args[0].split(',')]


# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Options
ftr = 'f' if full_with_conductance else 'k'
options = [
    [
        [3, 'n', 'a'],
        [3, 'a', 'a'],
        [3, ftr, 'a'],
    ], [
        [4, 'n', 'a'],
        [4, 'a', 'a'],
        [4, ftr, 'a'],
    ], [
        [3, 'a', 'n'],
        [3, 'a', 'a'],
        [3, 'a', ftr],
    ], [
        [4, 'a', 'n'],
        [4, 'a', 'a'],
        [4, 'a', ftr],
    ], [
        [3, 'n', 'n'],
        [3, 'a', 'a'],
        [3, ftr, ftr],
    ], [
        [4, 'n', 'n'],
        [4, 'a', 'a'],
        [4, ftr, ftr],
    ],
]
opt_labels = [
    'Searching',
    'Searching',
    'Starting',
    'Starting',
    'Both',
    'Both',
]

# Method colors
colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]


for cell in cell_list:
    # Create figure
    fig = plt.figure(figsize=mm(82, 40), dpi=200)
    fig.subplots_adjust(0.12, 0.19, 0.985, 0.99)
    grid = GridSpec(1, 1, hspace=0, wspace=0)
    ax = fig.add_subplot(grid[0, 0])
    ax.set_ylabel(r'Results within 1% of best (%)')

    xticks = []
    xtickl = []
    for irow, row in enumerate(options):

        # Count number of scores that were the same
        eclose = []
        pclose = []
        labels = []
        for config in row:
            method, search, sample = config
            imethod = method - 1

            labels.append(search + sample)

            # Get scores
            rs, ps, es, ts, ns = results.load(cell, method, search, sample)
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
            ds = np.max(ps / ps[0] - 1, axis=1)
            if method == 2:
                print(ds)
            ds = ds[ds < 0.01]
            pclose.append(100 * len(ds) / len(rs))

        # Y-position for bar charts
        d = 1 / (1 + len(row))
        x = irow + d * (np.arange(len(row)) - int(1 + np.floor(d / 2)))

        kargs = {
            'align': 'center',
            'edgecolor': 'k',
            'width': d,
            'color': colors[imethod],
        }

        kargs['alpha'] = 0.5
        ax.bar(x, eclose, **kargs)

        kargs['alpha'] = 1
        ax.bar(x, pclose, **kargs)

        xticks.extend(x)
        xtickl.extend(labels)

    ax.set_ylim(0, 102)

    ax.set_xticks(xticks)
    ax.set_xticklabels(xtickl)

    for iopt, label in enumerate(opt_labels):
        ax.text(iopt, -22, label, horizontalalignment='center')


    # Store
    name = base + '-cell-' + str(cell)
    if full_with_conductance:
        name += '-kinetic'
    fig.savefig(name + '.png')
    fig.savefig(name + '.pdf')

