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
if len(args) != 1:
    print('Syntax: ' + base + '.py <cell|all>')
    sys.exit(1)

if args[0] == 'all':
    cell_list = range(1, 10)
else:
    cell_list = [int(x) for x in args[0].split(',')]



hide_outliers = True




# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Method colors
colors = [
    'tab:blue',
    'tab:orange',
    'tab:orange',
    'tab:orange',
    'tab:green',
    'tab:green',
    'tab:green',
    'tab:red',
    'tab:red',
    'tab:red',
]

labels = [
    'M1',
    'M2-na',
    'M2-aa',
    'M2-fa',
    'M3-na',
    'M3-aa',
    'M3-fa',
    'M4-na',
    'M4-aa',
    'M4-fa',
]

log_labels = ['-na', '-aa', '-fa']
log_args = ['n', 'a', 'f']

# Tell seaborn to use my colours
palette = dict(zip(labels, colors))

#
# Create figure
#
for cell in cell_list:

    fig = plt.figure(figsize=mm(170, 60), dpi=200)
    fig.subplots_adjust(0.06, 0.08, 0.98, 0.99)
    grid = GridSpec(1, 2, hspace=0.2, wspace=0.25)

    # Marker size
    size = 2

    #
    # Graph 2: Computational time per method
    #
    ax0 = fig.add_subplot(grid[0, 0])

    xs = []
    ys = []
    for method in [2, 3, 4]:
        for ilog in [0, 1, 2]:
            label = 'M' + str(method) + log_labels[ilog]
            t = results.load_times(cell, method, log_args[ilog])
            xs.extend([label] * len(t))
            ys.append(t)
    xs = np.array(xs)
    ys = np.concatenate(ys) / 60        # Use minutes, not seconds

    # Create 'data frame'
    df1 = pandas.DataFrame({'method': xs, 'time': ys})
    df1['method'] = df1['method'].astype('category')

    # Hide extremes
    if hide_outliers:
        ax0.set_ylim(-5, 305)
        i = ys < 300
        xs = xs[i]
        ys = ys[i]
        plt.arrow(
            0.25, 255, 0, 30, width=0.05, head_length=10, color=colors[1])

        df2 = pandas.DataFrame({'method': xs, 'time': ys})
        df2['method'] = df2['method'].astype('category')
    else:
        df2 = df1

    args = {
        'ax': ax0,
        'x': 'method',
        'y': 'time',
        'order': labels[1:],
        'hue': 'method',
        'palette': palette,
    }
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

    seaborn.boxplot(data=df1, **args, **boxargs)
    seaborn.swarmplot(data=df2, size=size, **args)

    # Set labels
    ax0.get_legend().remove()
    ax0.set_xlabel('')
    ax0.set_ylabel('Time per optimisation (min)')

    #
    # Graph 3: Evaluation count per method
    #
    ax1 = fig.add_subplot(grid[0, 1])

    xs = []
    ys = []
    for method in [2, 3, 4]:
        for ilog in [0, 1, 2]:
            label = 'M' + str(method) + log_labels[ilog]
            f = results.load_evaluations(cell, method, log_args[ilog])
            xs.extend([label] * len(f))
            ys.append(f)
    xs = np.array(xs)
    ys = np.concatenate(ys)

    # Create 'data frame'
    df1 = pandas.DataFrame({'method': xs, 'evals': ys})
    df1['method'] = df1['method'].astype('category')

    # Hide extremes
    if hide_outliers:
        ax1.set_ylim(-100, 28100)
        ymax = 28000
        i = ys < ymax
        xs = xs[i]
        ys = ys[i]
        plt.arrow(
            0.25, 23300, 0, 3000, width=0.05, head_length=800,
            color=colors[1])
        plt.ylim(-700, ymax)

        df2 = pandas.DataFrame({'method': xs, 'evals': ys})
        df2['method'] = df2['method'].astype('category')
    else:
        df2 = df1

    args['ax'] = ax1
    args['y'] = 'evals'
    seaborn.boxplot(data=df1, **args, **boxargs)
    seaborn.swarmplot(data=df2, size=size, **args)

    # Set labels
    ax1.get_legend().remove()
    ax1.set_xlabel('')
    ax1.set_ylabel('Evaluations per optimisation')

    # Add cell name
    cell_name = 'Cell ' + ('S' if cell == 10 else str(cell))
    ax0.text(
        0.9, 0.9, cell_name, horizontalalignment='center', fontsize=12,
        transform=ax0.transAxes)
    ax1.text(
        0.9, 0.9, cell_name, horizontalalignment='center', fontsize=12,
        transform=ax1.transAxes)

    #
    # Store
    #

    name = base + '-cell-' + str(cell)
    plt.savefig(name + '.png')
    #plt.savefig(name + '.pdf')

