#!/usr/bin/env python3
#
# Figure: Best solutions for all 9 cells, for all 4 methods, plotted inside
# the prior
#
from __future__ import division
from __future__ import print_function
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import plots
import results


# Filename
base = os.path.splitext(os.path.basename(__file__))[0]

# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)


# Create figure
fig = plt.figure(figsize=mm(82, 84), dpi=200)
fig.subplots_adjust(0.12, 0.10, 0.98, 0.91)
grid = GridSpec(2, 2, wspace=0.4, hspace=0.4)

# P1/P2
log = True
ax0 = fig.add_subplot(grid[0, 0])
ax0.set_xlabel('p1 (log)')
ax0.set_ylabel('p2')
plots.prior12(ax0, log, labels=False)

# P3/P4
ax1 = fig.add_subplot(grid[0, 1])
ax1.set_xlabel('p3 (log)')
ax1.set_ylabel('p4')
plots.prior34(ax1, log, labels=False)

# P5/P6
ax2 = fig.add_subplot(grid[1, 0])
ax2.set_xlabel('p5 (log)')
ax2.set_ylabel('p6')
plots.prior12(ax2, log, labels=False)

# P7/P8
ax3 = fig.add_subplot(grid[1, 1])
ax3.set_xlabel('p7 (log)')
ax3.set_ylabel('p8')
plots.prior34(ax3, log, labels=False)

colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

markers = [
    'o',
    's',
    'x',
    '+',
]

text = False

for icell in range(9):
    for imethod in range(4):
        cell = 1 + icell
        method = 1 + imethod
        p = results.load_parameters(cell, method)
        color = colors[imethod]
        if not text:
            marker = markers[imethod]
            label = 'Method ' + str(method) if icell == 0 else None
            kw = {
                'color': color,
                'marker': marker,
                'label': label,
                'fillstyle': 'none',
                'linestyle': '',
            }
            ax0.plot(p[0], p[1], **kw)
            ax1.plot(p[2], p[3], **kw)
            ax2.plot(p[4], p[5], **kw)
            ax3.plot(p[6], p[7], **kw)
        else:
            fd = {}
            kw = {
                'horizontalalignment': 'center',
                'verticalalignment': 'center',
                'color': color,
                'fontdict': fd,
            }

            ax0.text(p[0], p[1], str(cell), **kw)
            ax1.text(p[2], p[3], str(cell), **kw)
            ax2.text(p[4], p[5], str(cell), **kw)
            ax3.text(p[6], p[7], str(cell), **kw)

if not text:
    ax0.legend(loc=(0, 1.05), ncol=4, handletextpad=0, columnspacing=1.5)


font = {'weight': 'bold', 'fontsize': 14}
ax0.text(0.88, 0.88, 'A', font, transform=ax0.transAxes)
ax1.text(0.88, 0.88, 'B', font, transform=ax1.transAxes)
ax2.text(0.88, 0.88, 'C', font, transform=ax2.transAxes)
ax3.text(0.88, 0.88, 'D', font, transform=ax3.transAxes)

# Save without zoom
fig.savefig(base + '-no-zoom.pdf')
fig.savefig(base + '-no-zoom.png')


# Save with zoom
ax0.set_xlim(5e-5, 1e-3)
ax0.set_ylim(0.02, 0.12)

ax1.set_xlim(2e-6, 2e-4)
ax1.set_ylim(0.03, 0.08)

ax2.set_xlim(3e-2, 3e-1)
ax2.set_ylim(0, 0.035)
ax2.xaxis.set_tick_params(which='minor', labelbottom=False)
ax2.set_xticks([4e-2, 0.1, 0.3])

ax3.set_xlim(9e-4, 1.1e-2)
ax3.set_ylim(0.02, 0.065)

fig.savefig(base + '.pdf')
fig.savefig(base + '.png')

