#!/usr/bin/env python3
#
# Dispersion of solutions, per cell, per method
#
from __future__ import division, print_function
import os
import sys
import myokit
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import results


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) > 0:
    print('Syntax: ' + base)
    sys.exit(1)

cell_list = list(range(1, 10))


# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)


# Create figure
fig = plt.figure(figsize=mm(82, 45), dpi=200)
fig.subplots_adjust(0.12, 0.16, 0.985, 0.99)

grid = GridSpec(2, 1, hspace=0.04)
ax0 = fig.add_subplot(grid[0, 0])
ax1 = fig.add_subplot(grid[1, 0])

ax0.set_ylabel(r'$E / E_{best}$')
ax0.set_yscale('log')
ax0.xaxis.set_tick_params(direction='in', labelbottom=False)

ax1.set_xlabel('Repeat (sorted)')
ax1.set_ylabel(r'$R(\theta, \theta_{best})$')
ax1.set_yscale('log')



colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

for method in [2, 3, 4]:
    for cell in 1 + np.arange(9):

        # Get scores
        fs = results.load_errors(cell, method)

        # Normalise w.r.t. first
        fs /= fs[0]

        kw = {
            'color': colors[method - 1],
            'label': 'Method ' + str(method) if cell == 1 else None,
            'lw': 1,
        }
        ax0.plot(1 + np.arange(len(fs)), fs, **kw)

        # Get all parameters
        ps = results.load_parameters(cell, method, repeats=True)

        # Normalise w.r.t. best parameters
        ps /= ps[0]

        # Calculate RMSE for each set, w.r.t. first
        rs = np.sqrt(np.sum((ps - ps[0])**2, axis=1) / 9)

        # Make graph look nicer for first point at -inf
        rs[0] = 1e-20

        kw = {
            'color': colors[method - 1],
            'label': 'Method ' + str(method) if cell == 1 else None,
            'lw': 1,
        }
        ax1.plot(1 + np.arange(len(rs)), sorted(rs), **kw)


# Zoom in on start
ax0.set_xlim(0.5, 50.5)
ax1.set_xlim(0.5, 50.5)

ax0.set_xticks([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
#ax0.set_yticks([1, 1e1, 1e2, 1e3, 1e4])
ax0.set_yticks([1, 1e2, 1e4])

ax1.set_xticks([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
ax1.set_ylim(10**(-9.5), 1e8)
ax1.set_yticks([1e-9, 1e-4, 1e1, 1e6])

# Add legend
ax0.legend()

# Store
name = base
fig.savefig(name + '.png')
fig.savefig(name + '.pdf')

