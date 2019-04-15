#!/usr/bin/env python3
#
# Figure: Cross validation on simulated summary statistic
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
import results
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

labels = [
    'Prediction 1',
    'Fit 2',
    'Prediction 3',
    'Prediction 4',
]

colorv = 'k'
color0 = '#000000'
colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

marker0 = 's-'
markers = [
    'o--',
    'o--',
    'o--',
    'o--',
]

for cell in cell_list:
    print('Selected cell ' + str(cell))
    label0 = 'Cell' + str(cell)

    # Create figure
    fig = plt.figure(figsize=mm(82, 78), dpi=200)
    fig.subplots_adjust(0.15, 0.092, 0.99, 0.88)

    grid = GridSpec(2, 2, wspace=0.4, hspace=0.2)
    ax0 = fig.add_subplot(grid[0, 0])
    #ax0.set_xlabel('V (mV)')
    ax0.set_ylabel('Steady state of act.')
    ax0.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax1 = fig.add_subplot(grid[0, 1])
    #ax1.set_xlabel('V (mV)')
    ax1.set_ylabel('Pr5 peak current (nA)')
    ax2 = fig.add_subplot(grid[1, 0])
    ax2.set_xlabel('V (mV)')
    ax2.set_ylabel('Time constant of act. (ms)')
    ax3 = fig.add_subplot(grid[1, 1])
    ax3.set_xlabel('V (mV)')
    ax3.set_ylabel('Time constant of inact. (ms)')

    # Show x and y axes
    ax1.axhline(0, color='gray', lw=0.5)

    # Plot
    ta, tr, ai, ri, iv = sumstat.all_summary_statistics(cell)
    args = {
        'color': color0,
        'label': label0,
    }
    ax0.plot(ai[0], ai[1], marker0, **args)
    ax1.plot(iv[0], iv[1], marker0, **args)
    ax2.plot(ta[0], ta[1], marker0, **args)
    ax3.plot(tr[0], tr[1], marker0, **args)

    for j in range(4):
        p = results.load_parameters(cell, j + 1)
        print(p)

        ta, tr, ai, ri, iv = sumstat.simulate_all_summary_statistics(cell, p)
        args = {
            'color': colors[j],
            'label': labels[j],
            'fillstyle': 'none',
            'lw': 1,
        }
        if j == 1:
            args['lw'] = 2

        ax0.plot(ai[0], ai[1], markers[j], **args)
        ax1.plot(iv[0], iv[1], markers[j], **args)
        ax2.plot(ta[0], ta[1], markers[j], **args)
        ax3.plot(tr[0], tr[1], markers[j], **args)

    # Legend on top of figure
    ax0.legend(ncol=3, loc=(0, 1.05))

    # Axes limits
    ax0.set_xlim(-65, 65)
    ax0.set_ylim(-0.05, 1.05)

    # Finalise
    fig.savefig(base + '-cell-' + str(cell) + '.png')
    fig.savefig(base + '-cell-' + str(cell) + '.pdf')
    plt.close(fig)

#plt.show()
