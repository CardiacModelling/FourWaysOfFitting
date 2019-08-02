#!/usr/bin/env python3
#
# Validation on traditional protocols
#
from __future__ import division
from __future__ import print_function
import gc
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
import plots
import results


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) not in (1, 2):
    print('Syntax: ' + base + '.py <cell|all> (pdf)')
    sys.exit(1)

if args[0] == 'all':
    cell_list = range(1, 10)
else:
    cell_list = [int(args[0])]
pdf = (len(args) > 1 and args[1] == 'pdf')


# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Limits
limits = [
    [(600, 1900),  (-3.0, 0.3)],
    [(5550, 6500), (-0.1, 1.5)],
    [(1200, 1350), (-0.1, 4.0)],
    [(2600, 3800), (-3.2, 1.5)],
]
org_limits = [list(x) for x in limits]

label0 = None
labels = [
    'Prediction 1',
    'Prediction 2',
    'Fit 3',
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
    #label0 = 'Cell ' + str(cell)

    # Adapt x-limits for Pr2 variant in cell 7 and 8
    if cell in (7, 8):
        limits[0][0] = (490, 1150)

    # Tweak y-limits per cell
    if cell == 1:
        limits[0][1] = (-3.0, 0.3)
        limits[1][1] = (-0.2, 1.55)
        limits[2][1] = (-1.1, 3.4)
        limits[3][1] = (-3.4, 1.9)
    elif cell == 2:
        limits[0][1] = (-1.9, 0.5)
        limits[1][1] = (-0.1, 0.9)
        limits[2][1] = (-0.8, 3.2)
        limits[3][1] = (-2.0, 1.3)
    elif cell == 3:
        limits[0][1] = (-2.7, 0.5)
        limits[1][1] = (-0.2, 0.85)
        limits[2][1] = (-0.8, 2.1)
        limits[3][1] = (-2.6, 1.4)
    elif cell == 4:
        limits[0][1] = (-1.8, 0.5)
        limits[1][1] = (-0.2, 0.85)
        limits[2][1] = (-0.8, 2.8)
        limits[3][1] = (-2.0, 1.1)
    elif cell == 5 or cell == 10:
        limits[0][1] = (-3.6, 0.5)
        limits[1][1] = (-0.1, 1.8)
        limits[2][1] = (-1.4, 6.5)
        limits[3][1] = (-4.1, 2.2)
    elif cell == 6:
        limits[0][1] = (-0.95, 0.25)
        limits[1][1] = (-0.1, 0.5)
        limits[2][1] = (-0.4, 2.0)
        limits[3][1] = (-0.7, 0.55)
    elif cell == 7:
        limits[0][1] = (-3.1, 0.5)
        limits[1][1] = (-0.4, 2.5)
        limits[2][1] = (-1.9, 9.5)
        limits[3][1] = (-4.5, 2.8)
    elif cell == 8:
        limits[0][1] = (-2.1, 0.5)
        limits[1][1] = (-0.2, 2.2)
        limits[2][1] = (-0.8, 4.2)
        limits[3][1] = (-2.7, 1.8)
    elif cell == 9:
        limits[0][1] = (-1.2, 0.3)
        limits[1][1] = (-0.1, 0.6)
        limits[2][1] = (-0.4, 1.9)
        limits[3][1] = (-1.3, 0.9)
    else:
        raise ValueError('Unknown cell: ' + str(cell))

    # Create figure
    fig = plt.figure(figsize=mm(170, 130), dpi=200)
    fig.subplots_adjust(0.05, 0.055, 0.995, 0.995)
    grid1 = GridSpec(5, 4, hspace=0.05, wspace=0.20)
    grid2 = SubGridSpec(4, 4, subplot_spec=grid1[1:, 0:], hspace=0, wspace=0.20)

    # Load parameters
    fits = [None]*4
    for j in range(4):
        try:
            fits[j] = results.load_parameters(cell, 1 + j)
        except ValueError:
            print('Skipping method ' + str(1 + j))
            pass

    # Create columns
    for i in range(4):
        protocol = 2 + i
        row = i // 2
        col = i % 2
        variant = protocol == 2 and cell in (7, 8)

        # Load data
        log = data.load(cell, protocol)
        i0 = log['current']
        times = log.time()

        # Create forward model and problem
        model = Model(
            data.load_myokit_protocol(protocol, variant),
            cells.reversal_potential(cells.temperature(cell)),
            sine_wave=False,
            analytical=True,
        )
        problem = pints.SingleOutputProblem(model, times, i0)

        # Run simulations
        d = [log.clone(), log.clone(), log.clone(), log.clone()]
        for j, fit in enumerate(fits):
            if fit is not None:
                d[j]['current'] = problem.evaluate(fit)
            else:
                print('No current for method ' + str(1 + j))

        # Limits
        xlo, xhi = limits[i][0]
        ylo, yhi = limits[i][1]

        # Top row: voltage
        ax = fig.add_subplot(grid1[0, i])
        ax.xaxis.set_tick_params(direction='in', labelbottom=False)
        ax.yaxis.set_tick_params(labelsize=8)
        ax.text(
            0.95, 0.87, 'Pr' + str(protocol),
            horizontalalignment='right', transform=ax.transAxes)
        ax.axvspan(xlo, xhi, color='blue', alpha=0.1)
        plots.voltage(ax, cell, protocol, lw=1, technicolor=True)
        if i == 0:
            ax.set_ylabel('V (mV)', labelpad=0.0, fontsize=9)

        # Next rows: fits
        for j in range(4):
            ax = fig.add_subplot(grid2[j, i])
            ax.set_xlim(xlo, xhi)
            ax.set_ylim(ylo, yhi)
            if j < 3:
                ax.xaxis.set_tick_params(direction='in', labelbottom=False)
            ax.yaxis.set_tick_params(labelsize=8)
            if i == 0:
                ax.set_ylabel('I (nA)', fontsize=9)
            if fits[j] is not None:
                plots.current(
                    ax, cell, protocol, lw=1.5, technicolor=True, log=log,
                    alpha=0.5, label=label0)
                plots.current(
                    ax, cell, protocol, lw=1, technicolor=False, log=d[j],
                    alpha=0.5, label=labels[j])
            else:
                print('Not plotting method ' + str(i + 1))

            # Thick borders for fit 3
            if j == 2:
                for spine in ax.spines.values():
                    spine.set_linewidth(2)
                    spine.set_color('blue')

            # Legends in left-most panels
            if i == 0:
                ax.legend(loc='lower left')

            # Labels on lowest rows
            if j == 3:
                ax.set_xlabel('Time (ms)')

        # Clear up a bit
        del(log, d, i0, times, model, problem)

    # Restore shared limits
    limits = org_limits

    # Finalise
    fig.savefig(base + '-cell-' + str(cell) + '.png')
    if pdf:
        fig.savefig(base + '-cell-' + str(cell) + '.pdf')

    plt.close(fig)
    del(fig, ax, grid1, grid2)
    gc.collect()

#plt.show()

