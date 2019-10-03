#!/usr/bin/env python3
#
# Figure 1: Attractor and a*r in the plane
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


# Get filename
base = os.path.splitext(os.path.basename(__file__))[0]

# Set font
font = {'family': 'arial', 'size': 9}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Create figure
fig = plt.figure(figsize=mm(94, 40), dpi=200)
fig.subplots_adjust(0.13, 0.17, 0.98, 0.98)
grid = GridSpec(1, 2, wspace=0.44)

# Plot attractor for various voltages
p = 9
xlabel = 'Deactivated' + ' '*p + 'a' + ' '*p + 'Activated'
ylabel = 'Inactivated' + ' '*p + 'r' + ' '*p + 'Recovered'

ax0 = fig.add_subplot(grid[0, 0])
ax0.set_xlabel(xlabel)
ax0.set_ylabel(ylabel)

vs = [-120, -100, -80, -60, -40, -20, -10, 0]
plots._phase_attractor(ax0, numbers=vs, color='#999999')

# Plot iso-conductance lines
ax1 = fig.add_subplot(grid[0, 1])
ax1.set_xlabel(xlabel)
ax1.set_ylabel(ylabel)

def iso(g, label=None):
    x = np.linspace(g, 1, 100)
    y = g / x
    ax1.plot(x, y)

    if label:
        c = np.sqrt(g) + 0.008
        ax1.text(c, c, label, fontsize=8)

iso(1/64, '1/64')
iso(1/16, '1/16')
iso(1/8, '1/8')
iso(2/8, '1/4')
iso(3/8, '3/8')
iso(4/8, '1/2')
iso(5/8, '5/8')
iso(6/8, '3/4')
iso(7/8, '7/8')

# Add letters
font = {'weight': 'bold', 'fontsize': 14}
ax0.text(-0.36, 0.92, 'A', font, transform=ax0.transAxes)
ax1.text(-0.36, 0.92, 'B', font, transform=ax1.transAxes)


# Finalise
fig.savefig(base + '.png')
fig.savefig(base + '.pdf')
fig.savefig(base + '.eps')

#plt.show()
