#!/usr/bin/env python3
#
# Dispersion of solutions, per cell, per method, shown in prior
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
import plots
import results



#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) not in [1, 2]:
    print('Syntax: ' + base + ' <cell|all> <zoom_method>')
    sys.exit(1)

if args[0] == 'all':
    cell_list = list(range(1, 10))
else:
    cell_list = [int(args[0])]

zoom = False
methods = [3, 4]
if len(args) == 2:
    methods = [int(args[1])]
    zoom = True


# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)


# Create figure
fig = plt.figure(figsize=mm(170, 47), dpi=200)
fig.subplots_adjust(0.057, 0.18, 0.99, 0.87)
grid = GridSpec(1, 4, wspace=0.33)

# P1/P2
ax0 = fig.add_subplot(grid[0, 0])
ax0.set_xlabel('p1 (log)')
ax0.set_ylabel('p2')
plots.prior12(ax0, True, labels=False)

# P3/P4
ax1 = fig.add_subplot(grid[0, 1])
ax1.set_xlabel('p3 (log)')
ax1.set_ylabel('p4')
plots.prior34(ax1, True, labels=False)

# P5/P6
ax2 = fig.add_subplot(grid[0, 2])
ax2.set_xlabel('p5 (log)')
ax2.set_ylabel('p6')
plots.prior12(ax2, True, labels=False)

# P7/P8
ax3 = fig.add_subplot(grid[0, 3])
ax3.set_xlabel('p7 (log)')
ax3.set_ylabel('p8')
plots.prior34(ax3, True, labels=False)

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


#
# Run
#
for cell in cell_list:

    for method in methods:
        imethod = method - 1
        ps = results.load_parameters(cell, method, True)
        kw = {
            'color': colors[imethod],
            'marker': markers[imethod],
            'label': 'Method ' + str(method),
            'fillstyle': 'none',
            'linestyle': '',
        }

        ax0.plot(ps[:, 0], ps[:, 1], **kw)
        ax1.plot(ps[:, 2], ps[:, 3], **kw)
        ax2.plot(ps[:, 4], ps[:, 5], **kw)
        ax3.plot(ps[:, 6], ps[:, 7], **kw)

        if zoom:
            kw['color'] = 'black'
            kw['fillstyle'] = 'full'
            kw['marker'] = 's'
            ax0.plot(ps[0, 0], ps[0, 1], **kw)
            ax1.plot(ps[0, 2], ps[0, 3], **kw)
            ax2.plot(ps[0, 4], ps[0, 5], **kw)
            ax3.plot(ps[0, 6], ps[0, 7], **kw)

    ax0.legend(loc=(0, 1.05), ncol=4)

    font = {'weight': 'bold', 'fontsize': 14}
    ax0.text(0.88, 0.88, 'A', font, transform=ax0.transAxes)
    ax1.text(0.88, 0.88, 'B', font, transform=ax1.transAxes)
    ax2.text(0.88, 0.88, 'C', font, transform=ax2.transAxes)
    ax3.text(0.88, 0.88, 'D', font, transform=ax3.transAxes)

    if zoom:
        p = ps[0]
        r = np.sqrt(np.sum((ps - p)**2, axis=1))
        pnear = ps[r < 10*np.median(r[1:10])]
        lo = np.min(pnear, axis=0)
        hi = np.max(pnear, axis=0)
        ra = hi - lo
        lo -= ra * 0.05
        hi += ra * 0.05

        ax0.set_xlim(lo[0], hi[0])
        ax0.set_ylim(lo[1], hi[1])
        ax1.set_xlim(lo[2], hi[2])
        ax1.set_ylim(lo[3], hi[3])
        ax2.set_xlim(lo[4], hi[4])
        ax2.set_ylim(lo[5], hi[5])
        ax3.set_xlim(lo[6], hi[6])
        ax3.set_ylim(lo[7], hi[7])

    name = base + '-cell-' + str(cell)
    if zoom:
        name += '-zoom-' + str(methods[0])

    plt.savefig(name + '.png')
    plt.savefig(name + '.pdf')
    plt.close()



#plt.show()
