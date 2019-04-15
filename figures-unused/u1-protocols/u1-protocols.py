#!/usr/bin/env python3
#
# Alternative figure 2: All protocols and results
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
    print('Syntax: ' + base + '.py <cell>')
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
    print('Selected cell ' + str(cell))

    # Create figure
    fig = plt.figure(figsize=mm(170, 85), dpi=200)
    grid = GridSpec(2, 3, hspace=0.15, wspace=0.17)

    for i in range(6):
        protocol = 2 + i
        row = i // 3
        col = i % 3

        g = SubGridSpec(3, 1, subplot_spec=grid[row, col], hspace=0.01)

        v = fig.add_subplot(g[0, 0])
        tc = protocol < 6
        plots.voltage(v, cell, protocol, technicolor=tc)

        c = fig.add_subplot(g[1:, 0])
        plots.current(c, cell, protocol, technicolor=tc)

        if col == 0:
            v.set_ylabel('V (mV)')
            c.set_ylabel('I (nA)', labelpad=(9 if row == 0 else 14))
        v.set_xticklabels([])
        if row == 1:
            c.set_xlabel('Time (ms)')

        v.yaxis.set_tick_params(labelsize=8)
        c.xaxis.set_tick_params(labelsize=8)
        c.yaxis.set_tick_params(labelsize=8)


    # Finalise
    fig.subplots_adjust(0.065, 0.09, 0.98, 0.99)
    fig.savefig(base + '-cell-' + str(cell) + '.png')

    #plt.show()

