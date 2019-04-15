#!/usr/bin/env python3
#
# Pr2 step by step (start only)
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
    print('Syntax:  ' + base + '.py')
    sys.exit(1)

protocol = 2

limits = [
    (264000, 265812),
    (264700, 266000),
    (264700, 275812),
    (264700, 300812),
    (264700, 312000),
]
n = len(limits)

# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Run simulation
m, t, v, i, a, r = plots._phase_simulation(protocol, all_signals=True)
sim = (m, a, r)

plt.figure()
for lim in limits:
    lo, hi = lim
    plt.plot(t[lo:hi], v[lo:hi])

ainf = m.get('ikr.act.inf').pyfunc()
rinf = m.get('ikr.rec.inf').pyfunc()

# Create figure
fig = plt.figure(figsize=mm(170, 60), dpi=200)
fig.subplots_adjust(0.065, 0.12, 0.99, 0.96)
grid = GridSpec(3, n, wspace=0.05, hspace=0.9)

ilo, ihi = limits[0][0], limits[-1][1]
tlo, thi = t[ilo] * 1e-3, t[ihi - 1] * 1e-3

for i, lim in enumerate(limits):

    # Protocol
    ax0 = fig.add_subplot(grid[0, i])
    if i == 0:
        ax0.set_ylabel('V (mV)')
    else:
        ax0.tick_params(labelleft=False)
    ax0.set_xlabel('Time (s)')
    ax0.set_xlim(tlo, thi)
    ax0.set_ylim(-135, 55)

    lo, hi = lim
    ax0.plot(t[ilo:ihi] * 1e-3, v[ilo:ihi], color='#dddddd')
    ax0.plot(t[lo:hi] * 1e-3, v[lo:hi])

    # Annotated phase plot
    ax1 = fig.add_subplot(grid[1:, i])
    lim = (265800, hi)
    plots.phase(ax1, protocol, limits=lim, sim=sim)
    ax1.set_xlim(-0.1, 1.1)
    ax1.set_ylim(-0.1, 1.1)

    j = lim[1] - 1
    ax1.plot(ainf(v[j]), rinf(v[j]), 'kx')

    ax1.set_xlabel('Activation, $a$')
    if i == 0:
        ax1.set_ylabel('Recovery, $r$', fontsize=9)
    else:
        ax1.tick_params(labelleft=False)

    if i == 0:
        ax1.text(
            0.15, 0.95, 'At rest, before P1',
            verticalalignment='top')
        ax1.arrow(
            ainf(v[j]) + 0.05, rinf(v[j]) - 0.05, 0.2, -0.1, color='gray')
        ax1.text(0.3, 0.40, 'Stable point')
    elif i == 1:
        ax1.text(
            0.15, 0.95, 'Start of P1:\nrapid inactivation',
            verticalalignment='top')
        ax1.arrow(
            ainf(v[j]) - 0.05, rinf(v[j]) + 0.05, -0.2, 0.2, color='gray')
        ax1.text(0.3, 0.3, 'New stable point')
    elif i == 2:
        ax1.text(
            0.15, 0.95,
            'During P1: \nrapid inactivation\nis followed by\nslow activation',
            verticalalignment='top')
    elif i == 3:
        ax1.text(0.15, 1.03, 'During P2', verticalalignment='top')
        ax1.arrow(
            ainf(v[j]) + 0.05, rinf(v[j]) - 0.05, 0.2, -0.2, color='gray')
        ax1.text(
            0.12, 0.60,
            'New stable point\nFast recovery\nis followed by\nslow deactivation',
            verticalalignment='top')
    elif i == 4:
        ax1.text(0.15, 1.03, 'After P2', verticalalignment='top')
        ax1.text(
            0.12, 0.50,
            'Return to the\n-80mV steady\nstate')

# Finalise
fig.savefig(base + '.png')
fig.savefig(base + '.pdf')

#plt.show()

