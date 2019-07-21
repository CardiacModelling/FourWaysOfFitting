#!/usr/bin/env python3
#
# Method and protocol performance, with and without log transforms
#
from __future__ import division, print_function
import os
import sys
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn
import pandas
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import results
import transformations


full_with_conductance = True



#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 2:
    print('Syntax: ' + base + '.py <cell|all> <method>')
    sys.exit(1)

if args[0] == 'all':
    cell_list = range(1, 10)
else:
    cell_list = [int(x) for x in args[0].split(',')]

method = int(args[1])


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
        [method, 'n', 'a'],
        [method, 'a', 'a'],
        [method, ftr, 'a'],
    ], [
        [method, 'a', 'n'],
        [method, 'a', 'a'],
        [method, 'a', ftr],
    ], [
        [method, 'n', 'n'],
        [method, 'a', 'a'],
        [method, ftr, ftr],
    ],
]
opt_names = [
    'Searching',
    'Starting',
    'Both',
]

# Y-axis cut-offs
if method == 3:
    ylimit = 30000
elif method == 4:
    ylimit = 30000
else:
    raise ValueError('Method not implemented: ' + str(method))

# Method colors
method_colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

# Marker size
size = 5

# Box plots
boxargs = {
    'dodge': False,
    'whis': np.inf,
    'boxprops': {
        'alpha': 0.2,
    },
    'whiskerprops': {
        'alpha': 0.2,
    },
    'capprops': {
        'alpha': 0.2,
    },
    'width': 0.9,
}


#
# Create figure
#
for cell in cell_list:

    fig = plt.figure(figsize=mm(170, 50), dpi=200)
    fig.subplots_adjust(0.08, 0.1, 0.98, 0.98)
    grid = GridSpec(1, 3, hspace=0.25, wspace=0.28)

    for irow, row in enumerate(options):

        # Load computational time and evaluations per method
        xs, times, evals = [], [], []
        labels, colors = [], []
        for config in row:
            method, search, sample = config

            label = 'M' + str(method) + '-' + search + sample
            color = method_colors[method - 1]
            labels.append(label)
            colors.append(color)

            rs, ps, es, ts, ns = results.load(cell, *config)
            xs.append([label] * len(ts))
            times.append(ts)
            evals.append(ns)
        xs = np.concatenate(xs)
        times = np.concatenate(times) / 60      # In minutes, not seconds
        evals = np.concatenate(evals)

        df1 = pandas.DataFrame({'method': xs, 'time': times, 'eval': evals})
        df1['method'] = df1['method'].astype('category')
        args = {
            'data': df1,
            'x': 'method',
            'order': labels,
            'hue': 'method',
            'palette': dict(zip(labels, colors)),
        }

        # Plot evaluations
        ax = fig.add_subplot(grid[0, irow])
        if ylimit:
            ax.set_ylim(-0.02 * ylimit, ylimit * 1.02)
        args['ax'] = ax
        args['y'] = 'eval'
        seaborn.boxplot(**args, **boxargs)
        seaborn.swarmplot(size=size, **args)
        ax.get_legend().remove()
        ax.set_xlabel(None)
        if irow == 0:
            ax.set_ylabel('Evaluations per optimisation')
        else:
            ax.set_ylabel(None)

        # Add option label
        ax.text(
            0.5, 0.9, opt_names[irow],
            horizontalalignment='center', fontsize=12, transform=ax.transAxes)

    # Add cell name
    cell_name = 'Cell ' + ('S' if cell == 10 else str(cell))
    fig.text(0.03, 0.02, cell_name, horizontalalignment='center', fontsize=12)

    # Store
    name = base + '-cell-' + str(cell) + '-m' + str(method)
    if not full_with_conductance:
        name += '-kinetic'
    plt.savefig(name + '.png')
    plt.savefig(name + '.pdf')

