#!/usr/bin/env python3
#
# Figure: Prior
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
import boundaries
import cells
import plots
import transformations


# Filename
base = os.path.splitext(os.path.basename(__file__))[0]

# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Create figure
fig = plt.figure(figsize=mm(82, 120), dpi=200)
fig.subplots_adjust(0.13, 0.08, 0.98, 0.98)
grid = GridSpec(3, 1, hspace=0.35)
g1 = SubGridSpec(1, 2, subplot_spec=grid[0, 0], wspace=0.40)
g2 = SubGridSpec(1, 2, subplot_spec=grid[1, 0], wspace=0.40)
g3 = SubGridSpec(1, 2, subplot_spec=grid[2, 0], wspace=0.40)

# Linear plots
ax0 = fig.add_subplot(g1[0, 0])
ax0.set_xlabel('p1 (or p5)')
ax0.set_ylabel('p2 (or p6)')
plots.prior12(ax0, False)

ax1 = fig.add_subplot(g1[0, 1])
ax1.set_xlabel('p3 (or p7)')
ax1.set_ylabel('p4 (or p8)')
plots.prior34(ax1, False, labels=False)

# Log plots
ax2 = fig.add_subplot(g2[0, 0])
ax2.set_xlabel('p1 (or p5)')
ax2.set_ylabel('p2 (or p6)')
plots.prior12(ax2, True)

ax3 = fig.add_subplot(g2[0, 1])
ax3.set_xlabel('p3 (or p7)')
ax3.set_ylabel('p4 (or p8)')
plots.prior34(ax3, True,)

# Log-log plots
ax4 = fig.add_subplot(g3[0, 0])
ax4.set_xlabel('p1 (or p5)')
ax4.set_ylabel('p2 (or p6)')
plots.prior12(ax4, True, True)

ax5 = fig.add_subplot(g3[0, 1])
ax5.set_xlabel('p3 (or p7)')
ax5.set_ylabel('p4 (or p8)')
plots.prior34(ax5, True, True)

# Draw samples
t0 = transformations.NullTransformation()
t1 = transformations.ATransformation()
t2 = transformations.FullTransformation()
labels = ['n-space', 'a-space', 'f-space']
markers = ['_', '+', 'x']

for i, trans in enumerate([t0, t1, t2]):

    # Sample
    b = boundaries.Boundaries(t0, trans)
    ps = np.array([b.sample() for i in range(50)])
    for p in ps:
        assert(b.check(p))

    # Join (p1, p5), (p2, p6), etc., discard conductances
    p1 = np.concatenate((ps[:, 0], ps[:, 4]))
    p2 = np.concatenate((ps[:, 1], ps[:, 5]))
    p3 = np.concatenate((ps[:, 2], ps[:, 6]))
    p4 = np.concatenate((ps[:, 3], ps[:, 7]))

    alpha = 0.6

    ax0.plot(p1, p2, markers[i], alpha=alpha)
    ax2.plot(p1, p2, markers[i], alpha=alpha)
    ax4.plot(p1, p2, markers[i], alpha=alpha)

    ax1.plot(p3, p4, markers[i], alpha=alpha, label=labels[i])
    ax3.plot(p3, p4, markers[i], alpha=alpha)
    ax5.plot(p3, p4, markers[i], alpha=alpha)


# Labels
font = {'weight': 'bold', 'fontsize': 14}
ax0.text(0.84, 0.84, 'A', font, transform=ax0.transAxes)
ax1.text(0.84, 0.84, 'B', font, transform=ax1.transAxes)
ax2.text(0.84, 0.84, 'C', font, transform=ax2.transAxes)
ax3.text(0.84, 0.84, 'D', font, transform=ax3.transAxes)
ax4.text(0.84, 0.84, 'E', font, transform=ax4.transAxes)
ax5.text(0.84, 0.84, 'F', font, transform=ax5.transAxes)
ax0.legend(loc='center', frameon=False)
ax1.legend(loc='center', frameon=False)


# Finalise
fig.savefig(base + '.pdf')
fig.savefig(base + '.png')

#plt.show()
