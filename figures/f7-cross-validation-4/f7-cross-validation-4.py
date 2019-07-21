#!/usr/bin/env python3
#
# Cross-validation on sine wave signal
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
    [(0, 7900), (-0.8, 0.9), 3],
    [(1400, 2050), (-3, 0.4), 1],
    [(3550, 6450), (-1, 1), 5],
    [(6450, 6700), (-1.5, 0.4), 1],
]
org_limits = [list(x) for x in limits]
nw = sum([x[2] for x in limits])
ba1 = 0.35
ba2 = 0.3

labelv = 'Pr7'
label0 = None
labels = [
    'Prediction 1',
    'Prediction 2',
    'Prediction 3',
    'Fit 4',
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
        limits[0][1] = (-0.7, 0.8)
        limits[1][1] = (-3.0, 0.6)
        limits[2][1] = (-0.7, 0.8)
        limits[3][1] = (-1.1, 0.4)
    elif cell == 2:
        limits[0][1] = (-0.8, 0.7)
        limits[1][1] = (-2.0, 0.6)
        limits[2][1] = (-0.6, 0.7)
        limits[3][1] = (-1.1, 0.5)
    elif cell == 3:
        limits[0][1] = (-1.1, 1.0)
        limits[1][1] = (-2.7, 0.6)
        limits[2][1] = (-1.1, 1.0)
        limits[3][1] = (-1.7, 0.6)
    elif cell == 4:
        limits[0][1] = (-0.9, 0.9)
        limits[1][1] = (-2.0, 0.6)
        limits[2][1] = (-0.75, 0.9)
        limits[3][1] = (-1.45, 0.6)
    elif cell == 5 or cell == 10:
        limits[0][1] = (-1.2, 1.2)
        limits[1][1] = (-3.8, 0.6)
        limits[2][1] = (-1.2, 1.4)
        limits[3][1] = (-1.9, 0.7)
    elif cell == 6:
        limits[0][1] = (-0.4, 0.5)
        limits[1][1] = (-0.75, 0.25)
        limits[2][1] = (-0.35, 0.45)
        limits[3][1] = (-0.5, 0.3)
    elif cell == 7:
        limits[0][1] = (-1.4, 1.6)
        limits[1][1] = (-4.6, 0.7)
        limits[2][1] = (-1.6, 2.0)
        limits[3][1] = (-2.4, 1.0)
    elif cell == 8:
        limits[0][1] = (-0.7, 0.8)
        limits[1][1] = (-2.5, 0.6)
        limits[2][1] = (-0.7, 0.9)
        limits[3][1] = (-1.1, 0.4)
    elif cell == 9:
        limits[0][1] = (-0.4, 0.4)
        limits[1][1] = (-1.1, 0.2)
        limits[2][1] = (-0.43, 0.43)
        limits[3][1] = (-0.6, 0.3)
    else:
        raise ValueError('Unknown cell')

    # Create figure
    fig = plt.figure(figsize=mm(170, 130), dpi=200)
    fig.subplots_adjust(0.063, 0.06, 0.995, 0.995)
    grid1 = GridSpec(5, nw, hspace=0.05, wspace=0.05)
    grid2 = SubGridSpec(
        4, nw, hspace=0, wspace=0.05, subplot_spec=grid1[1:, 0:])

    # Load parameters
    fits = []
    for i in range(1, 5):
        try:
            fits.append(results.load_parameters(cell, i))
        except ValueError:
            fits.append(None)

    # Load data
    print('Loading data files for cell ' + str(cell))
    log = data.load(cell, 7)
    time = log.time()
    current = log['current']
    voltage = log['voltage']

    # Create forward model
    model = Model(
        data.load_myokit_protocol(7),
        cells.reversal_potential(cells.temperature(cell)),
        sine_wave=True,
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
    ax.set_ylim(-145, 105)
    for i, lim in enumerate(limits[1:]):
        ax.axvspan(lim[0][0], lim[0][1], color=cm(i), alpha=ba1)
    ax.plot(time, voltage, color=colorv, label=labelv)
    ax.legend(loc='upper left').get_frame().set_alpha(1)

    for i, lim in enumerate(limits[1:]):
        hi = lo + lim[2]
        ax = fig.add_subplot(grid1[0, lo:hi])
        ax.tick_params('x', labelbottom=False, direction='in')
        ax.set_yticks([])
        ax.set_xlim(*lim[0])
        ax.axvspan(lim[0][0], lim[0][1], color=cm(i), alpha=ba2)
        ax.plot(time, voltage, color=colorv, label=labelv)
        lo = hi

    # Rows: Method 1-4
    for i, fit in enumerate(fits):
        if fit is not None:
            ix = problem.evaluate(fit)
        lo = 0
        hi = lo + limits[0][2]
        ax = fig.add_subplot(grid2[i, lo:hi])
        lo = hi
        ax.set_ylabel('I (nA)')
        if i < 3:
            ax.tick_params('x', labelbottom=False, direction='in')
        ax.set_xlim(*limits[0][0])
        ax.set_ylim(*limits[0][1])
        for j, lim in enumerate(limits[1:]):
            ax.axvspan(lim[0][0], lim[0][1], color=cm(j), alpha=ba1)
        ax.plot(time, i0, color=color0, label=label0)
        if fit is not None:
            ax.plot(time, ix, color=colors[i], label=labels[i])
        ax.legend(loc='upper left').get_frame().set_alpha(1)

        # Thick borders for fit 4
        if i == 3:
            for spine in ax.spines.values():
                spine.set_linewidth(2)
                spine.set_color('blue')

        # X-axis label
        if i == 3:
            ax.set_xlabel('Time (ms)')

        for j, lim in enumerate(limits[1:]):
            hi = lo + lim[2]
            ax = fig.add_subplot(grid2[i, lo:hi])
            lo = hi
            if i < 3:
                ax.tick_params('x', labelbottom=False, direction='in')
            elif j == 2:
                ax.set_xticks([6500, 6650])
            ax.set_yticks([])
            ax.set_xlim(*lim[0])
            ax.set_ylim(*lim[1])
            ax.axvspan(lim[0][0], lim[0][1], color=cm(j), alpha=ba2)
            ax.plot(time, i0, color=color0, label=label0)
            if fit is not None:
                ax.plot(time, ix, color=colors[i], label=labels[i])

            # Thick borders for fit 4
            if i == 3:
                for spine in ax.spines.values():
                    spine.set_linewidth(2)
                    spine.set_color('blue')

            # X-axis label
            if i == 3 and j == 1:
                ax.set_xlabel('Time (ms)')

    # Restore shared limits
    limits = org_limits

    # Store
    print('Storing figure for cell ' + str(cell))
    plt.savefig(base + '-cell-' + str(cell) + '.png')
    plt.savefig(base + '-cell-' + str(cell) + '.pdf')
    plt.close(fig)

#plt.show()
