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

plots.voltage(ax00, 1, 3)

# Plot steady state of activation
ax10 = fig.add_subplot(grid[1, 0])
ax10.set_xlabel('V (mV)')
ax10.set_ylabel('Steady state activation')
ax10.set_ylim(-0.1, 1.1)

for cell in cell_list:

    # Show activation diagram
    ai = sumstat.steady_state_activation(cell)
    ax10.plot(ai[0], ai[1], '-', color='#003388', alpha=0.75)


plt.savefig(base + '.png')
