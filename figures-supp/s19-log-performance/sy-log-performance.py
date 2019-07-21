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
options = [
    [
        [method, 'n', 'a'],
        [method, 'a', 'a'],
        [method, 'f', 'a'],
    ], [
        [method, 'a', 'n'],
        [method, 'a', 'a'],
        [method, 'a', 'f'],
    ], [
        [method, 'n', 'n'],
        [method, 'a', 'a'],
        [method, 'f', 'f'],
    ],
]

# Y-axis cut-offs
if method == 3:
    ylimits = [60, None]
elif method == 4:
    ylimits = [10, None]
else:
    raise ValueError('Unsupported method: ' + str(method))

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

    fig = plt.figure(figsize=mm(170, 145), dpi=200)
    fig.subplots_adjust(0.1, 0.04, 0.98, 0.99)
    grid = GridSpec(3, 2, hspace=0.25, wspace=0.28)

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

        # Plot times
        ax0 = fig.add_subplot(grid[irow, 0])
        args['ax'] = ax0
        args['y'] = 'time'
        seaborn.boxplot(**args, **boxargs)
        seaborn.swarmplot(size=size, **args)
        ax0.get_legend().remove()
        ax0.set_xlabel('')
        ax0.set_ylabel('Time per optimisation (min)')
        if ylimits[0]:
            ax0.set_ylim(-0.02 * ylimits[0], 1.02 * ylimits[0])

        # Plot evaluations
        ax1 = fig.add_subplot(grid[irow, 1])
        args['ax'] = ax1
        args['y'] = 'eval'
        seaborn.boxplot(**args, **boxargs)
        seaborn.swarmplot(size=size, **args)
        ax1.get_legend().remove()
        ax1.set_xlabel('')
        ax1.set_ylabel('Evaluations per optimisation')
        if ylimits[1]:
            ax0.set_ylim(-0.02 * ylimits[1], ylimits[1] * 1.02)

        # Add cell name
        cell_name = 'Cell ' + ('S' if cell == 10 else str(cell))
        ax0.text(
            0.5, 0.9, cell_name, horizontalalignment='center', fontsize=12,
            transform=ax0.transAxes)
        ax1.text(
            0.5, 0.9, cell_name, horizontalalignment='center', fontsize=12,
            transform=ax1.transAxes)

    # Major labels
    font = {'weight': 'bold', 'fontsize': 14}
    args = {
        'fontdict': font,
        'horizontalalignment': 'center',
        'verticalalignment': 'center',
        'rotation': 90,
    }
    fig.text(0.02, 0.854, 'Search space', **args)
    fig.text(0.02, 0.515, 'Starting position', **args)
    fig.text(0.02, 0.18, 'Both', **args)

    # Store
    name = base + '-cell-' + str(cell) + '-m' + str(method)
    plt.savefig(name + '.png')
    #plt.savefig(name + '.pdf')

