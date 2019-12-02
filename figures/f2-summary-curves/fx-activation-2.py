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
if len(args) != 0:
    print('Syntax: ' + base + '.py')
    sys.exit(1)

cell_list = range(1, 10)


def current(ax, cell):
    """
    Creates a (possibly folded) plot on axes ``ax`` of the currents measured in
    the given ``cell`` during the given ``protocol``.
    """
    # Load signal
    log = data.load(cell, 3)
    t = log['time']
    c = log['current']

    # Fold steps
    split = sumstat.split_points(3, False)
    for i, bounds in enumerate(split):
        if i == 5:
            lo, hi = bounds
            ax.plot(t[lo:hi] - t[lo], c[lo:hi], color='#003388', lw=1, alpha=0.75)


def voltage(ax, cell):
    """
    Creates a (possibly folded) plot on axes ``ax`` of the voltage for a given
    ``protocol``.
    """
    # Load voltage signal
    t, v = data.load_protocol_values(3)

    # Plot
    split = sumstat.split_points(3)
    for i, bounds in enumerate(split):
        if i == 5:
            lo, hi = bounds
            ax.plot(t[lo:hi] - t[lo], v[lo:hi], color='k', lw=1)

# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Create figure
fig = plt.figure(figsize=mm(100, 75), dpi=200)
fig.subplots_adjust(0.115, 0.1, 0.98, 0.98)
grid = GridSpec(2, 1, wspace=0.2, hspace=0.35)

# Plot protocol
ax00 = fig.add_subplot(grid[0, 0])
ax00.set_xlabel('Time (ms)')
ax00.set_ylabel('V (mV)')

voltage(ax00, 1)

# Plot steady state of activation
ax10 = fig.add_subplot(grid[1, 0])
ax10.set_xlabel('Time (ms)')
ax10.set_ylabel('I (pA)')
#ax10.set_ylim(-0.1, 1.1)

for cell in cell_list:

    # Show activation diagram
    current(ax10, cell)

plt.savefig(base + '.png')
