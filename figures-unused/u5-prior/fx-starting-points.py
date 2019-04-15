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
import transformation


# Filename
base = os.path.splitext(os.path.basename(__file__))[0]




#
#
#
print('Testing sampling without a transformation')
fig = plt.figure(figsize=(15, 3))
fig.subplots_adjust(0.1, 0.1, 0.98, 0.98)
grid = GridSpec(1, 2, wspace=0.25)
g1 = SubGridSpec(1, 2, subplot_spec=grid[0, 0], wspace=0.35)
g2 = SubGridSpec(1, 2, subplot_spec=grid[0, 1], wspace=0.35)

# Linear plots
ax0 = fig.add_subplot(g1[0, 0])
ax0.set_xlabel('p1 (or p5)')
ax0.set_ylabel('p2 (or p6)')
plots.prior12(ax0, False)
ax0.legend(loc='center', frameon=False)

ax1 = fig.add_subplot(g1[0, 1])
ax1.set_xlabel('p3 (or p7)')
ax1.set_ylabel('p4 (or p8)')
plots.prior34(ax1, False)

# Log plots
ax2 = fig.add_subplot(g2[0, 0])
ax2.set_xlabel('p1 (or p5)')
ax2.set_ylabel('p2 (or p6)')
plots.prior12(ax2, True)

ax3 = fig.add_subplot(g2[0, 1])
ax3.set_xlabel('p3 (or p7)')
ax3.set_ylabel('p4 (or p8)')
plots.prior34(ax3, True)

font = {'weight': 'bold', 'fontsize': 14}
ax0.text(0.84, 0.84, 'A', font, transform=ax0.transAxes)
ax1.text(0.84, 0.84, 'B', font, transform=ax1.transAxes)
ax2.text(0.84, 0.84, 'C', font, transform=ax2.transAxes)
ax3.text(0.84, 0.84, 'D', font, transform=ax3.transAxes)

b = boundaries.Boundaries(1)
for i in range(100):
    p = b.sample()
    assert(b.check(p))

    ax0.plot(p[0], p[1], 'x')
    ax1.plot(p[2], p[3], 'x')
    ax0.plot(p[4], p[5], 'o')
    ax1.plot(p[6], p[7], 'o')

    ax2.plot(p[0], p[1], 'x')
    ax3.plot(p[2], p[3], 'x')
    ax2.plot(p[4], p[5], 'o')
    ax3.plot(p[6], p[7], 'o')

fig.savefig(base + '-no-transformation.png')


#
#
#
print('Testing sampling with a transformation')
fig = plt.figure(figsize=(15, 4))
fig.subplots_adjust(0.1, 0.1, 0.98, 0.98)
grid = GridSpec(1, 2, wspace=0.25)
g1 = SubGridSpec(1, 2, subplot_spec=grid[0, 0], wspace=0.35)
g2 = SubGridSpec(1, 2, subplot_spec=grid[0, 1], wspace=0.35)

# Linear plots
ax0 = fig.add_subplot(g1[0, 0])
ax0.set_xlabel('p1 (or p5)')
ax0.set_ylabel('p2 (or p6)')
plots.prior12(ax0, False)
ax0.legend(loc='center', frameon=False)

ax1 = fig.add_subplot(g1[0, 1])
ax1.set_xlabel('p3 (or p7)')
ax1.set_ylabel('p4 (or p8)')
plots.prior34(ax1, False)

# Log plots
ax2 = fig.add_subplot(g2[0, 0])
ax2.set_xlabel('p1 (or p5)')
ax2.set_ylabel('p2 (or p6)')
plots.prior12(ax2, True)

ax3 = fig.add_subplot(g2[0, 1])
ax3.set_xlabel('p3 (or p7)')
ax3.set_ylabel('p4 (or p8)')
plots.prior34(ax3, True)

font = {'weight': 'bold', 'fontsize': 14}
ax0.text(0.84, 0.84, 'A', font, transform=ax0.transAxes)
ax1.text(0.84, 0.84, 'B', font, transform=ax1.transAxes)
ax2.text(0.84, 0.84, 'C', font, transform=ax2.transAxes)
ax3.text(0.84, 0.84, 'D', font, transform=ax3.transAxes)

trans = transformation.Transformation()
b = boundaries.Boundaries(1, trans)
for i in range(100):
    q = b.sample()
    assert(b.check(q))
    p = trans.detransform(q)

    ax0.plot(p[0], p[1], 'x')
    ax1.plot(p[2], p[3], 'x')
    ax0.plot(p[4], p[5], 'o')
    ax1.plot(p[6], p[7], 'o')

    ax2.plot(p[0], p[1], 'x')
    ax3.plot(p[2], p[3], 'x')
    ax2.plot(p[4], p[5], 'o')
    ax3.plot(p[6], p[7], 'o')

fig.savefig(base + '-with-transformation.png')

plt.show()
