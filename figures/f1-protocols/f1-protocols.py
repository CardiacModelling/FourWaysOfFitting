#!/usr/bin/env python3
#
# Figure 2: Pr2-7 with experimental data and phase planes
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
if len(args) not in (1, 2):
    print('Syntax:  ' + base + '.py <cell> (pdf)')
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


# Create figure
for cell in cell_list:
    print('Selected cell ' + str(cell))

    fig = plt.figure(figsize=mm(170, 135), dpi=200)
    grid = GridSpec(3, 2, hspace=0.42, wspace=0.22)

    letters = 'ABCDEF'
    for i in range(6):
        protocol = 2 + i
        row = i // 2
        col = i % 2

        g = SubGridSpec(
            3, 2, subplot_spec=grid[row, col], hspace=0, wspace=0.33)

        # Add plot of voltage
        v = fig.add_subplot(g[0, 0])
        plots.voltage(v, cell, protocol, lw=1, technicolor=True)
        font = {'weight': 'bold', 'size': 10}
        v.text(0.98, 0.78, 'Pr' + str(protocol),
            fontdict=font, horizontalalignment='right', transform=v.transAxes)

        # Show P1,P2 labels
        font = {'size': 9}
        if protocol == 2:
            v.text(0.35, 0.80, 'P1', fontdict=font, transform=v.transAxes)
            v.text(0.4, 0.1, 'P2', fontdict=font, transform=v.transAxes)
        elif protocol == 3:
            v.text(0.35, 0.12, 'P1', fontdict=font, transform=v.transAxes)
            v.text(0.69, 0.54, 'P2', fontdict=font, transform=v.transAxes)
        elif protocol == 4:
            v.text(0.27, 0.75, 'P1', fontdict=font, transform=v.transAxes)
            v.text(0.305, 0.11, 'P2', fontdict=font, transform=v.transAxes)
            v.text(0.49, 0.75, 'P3', fontdict=font, transform=v.transAxes)
        elif protocol == 5:
            v.text(0.153, 0.75, 'P1', fontdict=font, transform=v.transAxes)
            v.text(0.49, 0.54, 'P2', fontdict=font, transform=v.transAxes)

        # Add plot of current
        c = fig.add_subplot(g[1:, 0])
        plots.current(c, cell, protocol, lw=1, technicolor=True)

        # Add phase diagram
        p = fig.add_subplot(g[:, 1])
        plots.phase(p, protocol)
        font = {'weight': 'bold', 'size': 10}
        p.text(0.98, 0.93, 'Pr' + str(protocol),
            fontdict=font, horizontalalignment='right', transform=p.transAxes)

        c.set_xlabel('Time (ms)', fontsize=9)
        c.set_ylabel('I (nA)', labelpad=9.2, fontsize=9)
        v.set_ylabel('V (mV)', labelpad=0.0, fontsize=9)
        xlabel = 'Deactivated' + ' '*8 + 'a' + ' '*8 + 'Activated'
        ylabel = 'Inactivated' + ' '*9 + 'r' + ' '*9 + 'Recovered'
        p.set_xlabel(xlabel, fontsize=9)
        p.set_ylabel(ylabel, fontsize=9)

        c.xaxis.set_tick_params(labelsize=9)
        c.yaxis.set_tick_params(labelsize=9)
        v.set_xticklabels([])
        v.yaxis.set_tick_params(labelsize=9)
        p.xaxis.set_tick_params(labelsize=9)
        p.yaxis.set_tick_params(labelsize=9)

        # Labels A,B,C,...
        font = {'weight': 'bold', 'size': 13}
        v.text(-0.22, 1.0, letters[i],
            fontdict=font, horizontalalignment='right', transform=v.transAxes)


    # Finalise
    fig.subplots_adjust(0.055, 0.055, 0.985, 0.98)
    fig.savefig(base + '-cell-' + str(cell) + '.png')
    if pdf:
        fig.savefig(base + '-cell-' + str(cell) + '.pdf')

#plt.show()

