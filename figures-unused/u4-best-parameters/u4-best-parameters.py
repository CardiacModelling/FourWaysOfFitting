#!/usr/bin/env python3
#
# Synthetic data study: Obtained parameter values for the solutions with a
# score within 1% of best.
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
import seaborn
import pandas

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import results


relative = True


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 0:
    print('Syntax: ' + base + '.py')
    sys.exit(1)
cell = 10

# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)


# Create figure
fig = plt.figure(figsize=mm(170, 170), dpi=200)
fig.subplots_adjust(0.1, 0.03, 0.98, 0.95)
grid = GridSpec(9, 3, hspace=0.6, wspace=0.4)

colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

# Load kylie parameters
ks = results.load_kylie_parameters(5 if cell == 10 else 99)

# Plot data
axes = []
for method in [2, 3, 4]:
    imethod = method - 1
    axrow = []

    # Get scores, parameters
    fs = results.load_errors(cell, method)
    ps = results.load_parameters(cell, method, repeats=True)

    # Cut-off at 1% deviation
    ifs = fs / fs[0] - 1 < 1e-2
    fs = fs[ifs]
    ps = ps[ifs]

    if relative:
        ps = 100 * (ps - ks) / ks

    # Create subfigures
    for i in range(9):
        ax = fig.add_subplot(grid[i, method - 2])
        axrow.append(ax)

        psi = ps[:, i]
        xs = np.arange(len(psi))
        ax.vlines(xs, 0, psi, colors='k', alpha=0.3)
        ax.plot(xs, psi, 'x', color=colors[imethod])

        if relative:
            ax.axhline(0, color='k')

            ax.ticklabel_format(
                axis='y', style='plain', useOffset=False,
                scilimits=(0, 0), useMathText=True)

            for ylim in [0.05, 0.11, 0.21, 0.6, 1.1, 2.1, 3.5, 5.1]:
                if np.max(np.abs(psi)) * 1.1 < ylim:
                    ax.set_ylim(-ylim, ylim)
                    break

        else:
            ax.plot([-1, len(xs)], [ks[i], ks[i]])
            ax.ticklabel_format(
                axis='y', style='scientific', useOffset=False,
                scilimits=(0, 0), useMathText=True)

        ax.set_ylabel('p' + str(1 + i))

    axes.append(axrow)

# Add labels
opts = {
    'horizontalalignment': 'center',
    'verticalalignment': 'center',
    'fontsize': 14,
}
y = 0.975
fig.text(0.21, y, 'Method 2', **opts)
fig.text(0.54, y, 'Method 3', **opts)
fig.text(0.86, y, 'Method 4', **opts)

fig.text(
    0.02, 0.5,
    'Error relative to true solution (%), for the N fits with a score within'
    '1% of the best obtained score',
    rotation='vertical', **opts)
fig.text(0.01, 0.98, 'Cell S', fontdict={'size': 14, 'fontweight':'bold'})


# Store
name = base
fig.savefig(name + '.png')
fig.savefig(name + '.pdf')

