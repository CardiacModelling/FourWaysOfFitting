#!/usr/bin/env python3
#
# Figure 3: Summary curves (alternative)
#
from __future__ import division
from __future__ import print_function
import os
import sys
import numpy as np
import myokit
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import cells
import data
import plots
import sumstat


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

for cell in cell_list:
    # Create figure
    fig = plt.figure(figsize=mm(140, 140), dpi=200)
    grid = GridSpec(2, 2, wspace=0.2, hspace=0.2)

    # Steady state of activation
    ax00 = fig.add_subplot(grid[0, 0])
    ax00.set_xlabel('V (mV)')
    ax00.set_ylabel('Steady state activation')
    ax00.set_ylim(-0.1, 1.1)

    # Steady state of inactivation
    ax01 = fig.add_subplot(grid[0, 1])
    ax01.set_xlabel('V (mV)')
    ax01.set_ylabel('Steady state inactivation')
    #ax01.set_ylim(-2, 4)

    # Time constant of activation
    ax10 = fig.add_subplot(grid[1, 0])
    ax10.set_xlabel('V (mV)')
    ax10.set_ylabel('Time constant of activation')

    # Time constant of inactivation
    ax11 = fig.add_subplot(grid[1, 1])
    ax11.set_xlabel('V (mV)')
    ax11.set_ylabel('Time constant of inactivation')

    # Plot all data
    marker = plots.cell_markers[cell - 1]
    label = 'Cell' + str(cell)

    ta, tr, ai, ri, iv = sumstat.all_summary_statistics(cell)
    if True:
        p = sumstat.direct_fit_logarithmic(ta, tr, ai, ri, iv)

        v = np.linspace(-60, 60)
        y = sumstat.model_steady_state_activation(v, p)
        ax00.plot(v, y, 'k:')

        v = np.linspace(-120, 0)
        y = sumstat.model_steady_state_inactivation(v, p)
        ax01.plot(v, y, 'k:')

        v = np.linspace(-120, 40)
        y = sumstat.model_time_constant_of_activation(v, p)
        ax10.plot(v, y, 'k:')

        v = np.linspace(-120, 60)
        y = sumstat.model_time_constant_of_inactivation(v, p)
        ax11.plot(v, y, 'k:')

    ax00.plot(ai[0], ai[1], marker, label=label)
    ax01.plot(ri[0], ri[1], marker, label=label)
    ax10.plot(ta[0], ta[1], marker, label=label)
    ax11.plot(tr[0], tr[1], marker, label=label)

    # Set limits for ss inact
    ax01.set_ylim(min(1.1 * min(ri[1]), -0.1), max(1.1 * max(ri[1]), 1.1))

    # Add legends
    ax00.legend(loc='lower right')
    ax01.legend(loc='lower left')
    ax10.legend()
    ax11.legend()

    # Finalise
    fig.subplots_adjust(0.09, 0.15, 0.98, 0.98)
    fig.savefig(base + '-cell-' + str(cell) + '.png')

