#!/usr/bin/env python3
#
# Figure: Optimisation tips
#
from __future__ import division
from __future__ import print_function
import myokit
import numpy as np
import os
import pints
import sys

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import cells
import data
import model
import plots
import results

debug = False

# Filename
base = os.path.splitext(os.path.basename(__file__))[0]

# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

#
#
# Create figure
#
#
fig = plt.figure(figsize=mm(82, 58), dpi=200)
fig.subplots_adjust(0.09, 0.12, 0.985, 0.99)
grid = GridSpec(7, 1, hspace=30)
grid_prior = SubGridSpec(1, 2, subplot_spec=grid[:3, 0], wspace=0.3)
grid_prior1 = SubGridSpec(1, 2, subplot_spec=grid_prior[0, 0], wspace=0.5)
grid_prior2 = SubGridSpec(1, 2, subplot_spec=grid_prior[0, 1], wspace=0.5)
grid_toler = SubGridSpec(1, 3, subplot_spec=grid[3:, 0], wspace=0.05)

# Add letters
letter_font = {'weight': 'bold', 'fontsize': 14}
fig.text(0.003, 0.95, 'A', letter_font)
fig.text(0.503, 0.95, 'B', letter_font)
fig.text(0.003, 0.52, 'C', letter_font)

#
#
# Prior
#
#

font = {'size': 9}
xpad = 3
ypad = -10

ax0 = fig.add_subplot(grid_prior1[0, 0])
plots.prior12(ax0, False)
ax0.set_xlabel('p1 & p5', fontdict=font, labelpad=xpad)
ax0.set_ylabel('p2 & p6', fontdict=font, labelpad=ypad)
ax0.set_xticks([0, 500, 1000])
ax0.set_yticks([0, 0.4])

ax1 = fig.add_subplot(grid_prior1[0, 1])
plots.prior34(ax1, False)
ax1.set_xlabel('p3 & p7', fontdict=font, labelpad=xpad)
ax1.set_ylabel('p4 & p8', fontdict=font, labelpad=ypad)
ax1.set_xticks([0, 500, 1000])
ax1.set_yticks([0, 0.4])

ax2 = fig.add_subplot(grid_prior2[0, 0])
plots.prior12(ax2, True)
ax2.set_xlabel('p1 & p5 (log)', fontdict=font, labelpad=xpad)
ax2.set_ylabel('p2 & p6', fontdict=font, labelpad=ypad)
ax2.set_xticks([1e-7, 1e-2, 1e3])
ax2.set_yticks([0, 0.4])

ax3 = fig.add_subplot(grid_prior2[0, 1])
plots.prior34(ax3, True)
ax3.set_xlabel('p3 & p7 (log)', fontdict=font, labelpad=xpad)
ax3.set_ylabel('p4 & p8', fontdict=font, labelpad=ypad)
ax3.set_xticks([1e-7, 1e-2, 1e3])
ax3.set_yticks([0, 0.4])

for ax in [ax0, ax1, ax2, ax3]:
    for label in ax.get_xticklabels():
        label.set_fontsize(8)
    for label in ax.get_yticklabels():
        label.set_fontsize(8)
for ax in [ax2, ax3]:
    for tick in ax.xaxis.get_major_ticks():
        tick.set_pad(-0.5)

#
#
# Solver tolerance
#
#
cell = 5
protocol = 7

# Create forward model
model = model.Model(
    data.load_myokit_protocol(protocol),
    cells.reversal_potential(cells.temperature(cell)),
    sine_wave=(protocol == 7),
    start_steady=True,
)

# Load data, create single output problem
log = data.load(cell, protocol)
time = log.time()
current = log['current']
voltage = log['voltage']
del(log)

# Create single output problem
problem = pints.SingleOutputProblem(model, time, current)

# Define error function
f = pints.RootMeanSquaredError(problem)

# Load solution from sine wave fitting
popt = results.load_parameters(cell, 4)

tolerances = ['1e-4', 1e-6, 1e-8]
n = 2 if debug else 100
xlo = 0.995
xhi = 1.005
p1s = np.linspace(popt[0] * xlo, popt[0] * xhi, n)
ps = popt.reshape(1, 9).repeat(n, axis=0)
ps[:, 0] = p1s

for i, tol in enumerate(tolerances):
    print('Evaluating for ' + str(tol))
    model.set_tolerances(float(tol))
    fs = [f(p) for p in ps]

    ax = fig.add_subplot(grid_toler[0, i])
    ax.set_xlabel('$p_1$')
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    ax.ticklabel_format(axis='y', useOffset=False)
    if i == 0:
        ax.set_ylabel('$E_{M4}$')
    ax.yaxis.set_tick_params(direction='in')

    ax.plot(p1s, fs, lw=1, label='tol=' + str(tol))
    ax.tick_params(labelleft=False)
    ax.legend().get_frame().set_alpha(1)

    #if debug:
    #    break


#
#
# Store
#
#
fig.savefig(base + '.png')
fig.savefig(base + '.pdf')

