#!/usr/bin/env python3
#
# Validation on AP signal
#
#
from __future__ import division
from __future__ import print_function
import os
import sys
import pints
import numpy as np
import myokit
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
from model import Model
import cells
import data
import results


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
    cell_list = [int(args[0])]


# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Zooms
cm = plt.cm.get_cmap('Pastel2_r')
limits = [
    [(0, 8700), (-0.1, 0.9), 5],
    [(2410, 2480), (-0.2, 0.9), 1],
    [(5500, 7300), (-0.05, 1.5), 3],
    [(7250, 7900), (-1.5, 0.5), 1],
]
org_limits = [list(x) for x in limits]
nw = sum([lim[2] for lim in limits])
ba1 = 0.4
ba2 = 0.2

labelv = 'Pr6'
labels = [
    'Prediction 1',
    'Prediction 2',
    'Prediction 3',
    'Prediction 4',
]

colorv = 'k'
color0 = '#999999'
colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]
# purple, brown

for cell in cell_list:
    print('Selected cell ' + str(cell))
    label0 = 'Cell ' + str(cell)

    # Tweak y-limits per cell
    if cell == 1:
        limits[0][1] = (-0.15, 0.7)
        limits[1][1] = (-0.05, 0.6)
        limits[2][1] = (-0.09, 1.2)
        limits[3][1] = (-1.6, 0.5)
    elif cell == 2:
        limits[0][1] = (-0.13, 0.7)
        limits[1][1] = (-0.05, 0.8)
        limits[2][1] = (-0.1, 1.3)
        limits[3][1] = (-1.3, 0.5)
    elif cell == 3:
        limits[0][1] = (-0.15, 0.7)
        limits[1][1] = (-0.1, 0.8)
        limits[2][1] = (-0.15, 1.5)
        limits[3][1] = (-1.8, 0.5)
    elif cell == 4:
        limits[0][1] = (-0.15, 0.7)
        limits[1][1] = (-0.05, 1.0)
        limits[2][1] = (-0.13, 1.6)
        limits[3][1] = (-1.4, 0.5)
    elif cell == 5:
        limits[0][1] = (-0.15, 1.4)
        limits[1][1] = (-0.1, 1.7)
        limits[2][1] = (-0.08, 2.65)
        limits[3][1] = (-2.2, 0.6)
    elif cell == 6:
        limits[0][1] = (-0.05, 0.5)
        limits[1][1] = (-0.045, 0.69)
        limits[2][1] = (-0.07, 1.06)
        limits[3][1] = (-0.5, 0.3)
    elif cell == 7:
        limits[0][1] = (-0.15, 1.3)
        limits[1][1] = (-0.1, 2.4)
        limits[2][1] = (-0.25, 4.95)
        limits[3][1] = (-2.9, 0.9)
    elif cell == 8:
        limits[0][1] = (-0.15, 0.8)
        limits[1][1] = (-0.1, 1.1)
        limits[2][1] = (-0.2, 2.2)
        limits[3][1] = (-1.4, 0.7)
    elif cell == 9:
        limits[0][1] = (-0.1, 0.4)
        limits[1][1] = (-0.09, 0.7)
        limits[2][1] = (-0.2, 1.0)
        limits[3][1] = (-0.65, 0.3)

    # Create figure
    fig = plt.figure(figsize=mm(170, 130), dpi=200)
    fig.subplots_adjust(0.07, 0.065, 0.985, 0.99)
    grid1 = GridSpec(5, nw, hspace=0.05, wspace=0.05)
    grid2 = SubGridSpec(
        4, nw, hspace=0, wspace=0.05, subplot_spec=grid1[1:, 0:])

    # Load parameters
    fits = [results.load_parameters(cell, i) for i in range(1, 5)]

    # Load data
    print('Loading data files for cell ' + str(cell))
    log = data.load(cell, 6)
    time = log.time()
    current = log['current']
    voltage = log['voltage']

    # Create forward model
    model = Model(
        (time, voltage),
        cells.reversal_potential(cells.temperature(cell)),
        sine_wave=False,
    )

    # Define problem
    problem = pints.SingleOutputProblem(model, time, current)

    # Run simulations
    i0 = current

    # Row 1: Voltage
    lo = 0
    hi = lo + limits[0][2]
    ax = fig.add_subplot(grid1[0, lo:hi])
    lo = hi
    ax.set_ylabel('V (mV)')
    ax.tick_params('x', labelbottom=False, direction='in')
    ax.set_xlim(*limits[0][0])
    for i, lim in enumerate(limits[1:]):
        ax.axvspan(lim[0][0], lim[0][1], color=cm(i), alpha=ba1)
    else:
        ax.set_xlabel('Time (ms)')
    ax.plot(time, voltage, color=colorv, label=labelv)
    ax.legend(loc='upper left', frameon=False)

    for i, lim in enumerate(limits[1:]):
        hi = lo + lim[2]
        ax = fig.add_subplot(grid1[0, lo:hi])
        ax.tick_params('x', labelbottom=False, direction='in')
        ax.set_yticks([])
        ax.set_xlim(*lim[0])
        ax.axvspan(lim[0][0], lim[0][1], color=cm(i), alpha=ba2)
        ax.plot(time, voltage, color=colorv, label=labelv)
        lo = hi

    # Rows: Methods 1-4
    for i, fit in enumerate(fits):
        ix = problem.evaluate(fit)

        lo = 0
        hi = lo + limits[0][2]
        ax = fig.add_subplot(grid2[i, lo:hi])
        lo = hi
        ax.set_ylabel('I (nA)')
        if i != 3:
            ax.tick_params('x', labelbottom=False, direction='in')
        ax.set_xlim(*limits[0][0])
        ax.set_ylim(*limits[0][1])
        for j, lim in enumerate(limits[1:]):
            ax.axvspan(lim[0][0], lim[0][1], color=cm(j), alpha=ba1)
        ax.plot(time, i0, color=color0, label=label0)
        ax.plot(time, ix, color=colors[i], label=labels[i])
        ax.legend(loc='upper left', frameon=False)

        # X-axis labels
        if i == 3:
            ax.set_xlabel('Time (ms)')

        for j, lim in enumerate(limits[1:]):
            hi = lo + lim[2]
            ax = fig.add_subplot(grid2[i, lo:hi])
            lo = hi
            ax.set_yticks([])
            ax.set_xlim(*lim[0])
            ax.set_ylim(*lim[1])
            ax.axvspan(lim[0][0], lim[0][1], color=cm(j), alpha=ba2)
            ax.plot(time, i0, color=color0, label=label0)
            ax.plot(time, ix, color=colors[i], label=labels[i])
            if i != 3:
                ax.tick_params('x', labelbottom=False, direction='in')
            elif j == 0:
                ax.set_xticks([2420, 2460])
            elif j == 1:
                ax.set_xticks([5600, 6000, 6500, 7000])
            elif j == 2:
                ax.set_xticks([7400, 7800])

            # X-axis labels
            if i == 3:
                ax.set_xlabel('Time (ms)')

    # Restore shared limits
    limits = org_limits

    # Store
    print('Storing figure for cell ' + str(cell))
    plt.savefig(base + '-cell-' + str(cell) + '.png')
    plt.savefig(base + '-cell-' + str(cell) + '.pdf')
    plt.close(fig)

#plt.show()
