#!/usr/bin/env python3
#
# Figure: One over (V - E) issues
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
#fig = plt.figure(figsize=mm(82, 82), dpi=200)
#grid = GridSpec(2, 2, wspace=0.35, hspace=0.35)
fig = plt.figure(figsize=mm(170, 40), dpi=200)
fig.subplots_adjust(0.045, 0.17, 0.91, 0.96)

grid = GridSpec(1, 4, wspace=0.35)

legend_location = [1.06, 0.02]

# Add panels
ax0 = fig.add_subplot(grid[0, 0])
ax0.set_xlabel('V (mV)')
ax0.set_ylabel('I (nA)')
ax1 = fig.add_subplot(grid[0, 1])
ax1.set_xlabel('V (mV)')
ax1.set_ylabel('Multiplier, with noise on E')
ax2 = fig.add_subplot(grid[0, 2])
ax2.set_xlabel('V (mV)')
ax2.set_ylabel('Steady-state of inactivation')
ax3 = fig.add_subplot(grid[0, 3])
ax3.set_xlabel('V (mV)')
#ax3.set_ylabel('Steady-state of inactivation')


# Plot all data
ri_mean1 = []
ri_mean2 = []
ri_v1 = None
ri_v2 = None
for i in range(9):
    cell = i + 1
    marker = plots.cell_markers[i]
    label = 'Cell ' + str(cell)
    pr5 = data.load(cell, 5)

    iv = sumstat.iv_curve(cell, pr5)
    if i == 0:
        ax0.axhline(0, color='k', alpha=0.2)
    ax0.plot(iv[0], iv[1], marker, label=label)

    ri = sumstat.steady_state_inactivation_pr5(
        cell, pr5, include_minus_90=True)
    ri_mean1.append(ri[1])
    if i == 0:
        ri_v1 = ri[0]
        ax2.axhline(0, color='k', alpha=0.2)
        ax2.axhline(1, color='k', alpha=0.2)
    ax2.plot(ri[0], ri[1], marker, label=label)
    ax2.set_ylim(-2, 3)

    ri = sumstat.steady_state_inactivation_pr5(
        cell, pr5, include_minus_90=False)
    ri_mean2.append(ri[1])
    if i == 0:
        ri_v2 = ri[0]
        ax3.axhline(0, color='k', alpha=0.2)
        ax3.axhline(1, color='k', alpha=0.2)
    ax3.plot(ri[0], ri[1], marker, label=label)
    ax3.set_ylim(-0.1, 1.3)

# Plot mean ri
ri_mean1 = np.mean(np.array(ri_mean1), axis=0)
ax2.plot(ri_v1, ri_mean1, 'k:', zorder=0, lw=1, label='Mean')
ri_mean2 = np.mean(np.array(ri_mean2), axis=0)
ax3.plot(ri_v2, ri_mean2, 'k:', zorder=0, lw=1, label='Mean')

if False:
    def boltzmann(v, h, s):
        return 1 / (1 + np.exp(s * (h - v)))

    from scipy.optimize import curve_fit
    popt, pcov = curve_fit(boltzmann, ri_v, ri_mean, [-60, -0.03])
    hr, sr = popt
    v = np.linspace(-120, 0)
    ax2.plot(v, boltzmann(v, hr, sr), 'tab:blue', lw=1, zorder=0)
    ax3.plot(v, boltzmann(v, hr, sr), 'tab:blue', lw=1, zorder=0)


# Plot effect of noise on 1 / (V - E) multiplier
sigma = 2
x = np.random.normal(scale=sigma, size=(1000,))
E = -88.4
dV = 0.01
V = np.arange(-120, -40, dV)
g = np.zeros((len(x), len(V)))
for i, v in enumerate(V):
    g[:, i] = 1 / (v - E + x)
g = np.sort(g, axis=0)
del(v)

V1 = np.arange(-120, E, dV)
V2 = np.array([E - dV, E + dV])
V3 = np.arange(E + dV, -40, dV)

ax1.plot(V, g[100,:], 'r', lw=1, alpha=0.5)
ax1.plot(V, g[900,:], 'r', lw=1, alpha=0.5)
ax1.fill_between(V, g[100,:], g[900,:], color='r', alpha=0.02)
ax1.plot(V1, 1 / (V1 - E), color='tab:blue', lw=1)
ax1.plot(V2, 1 / (V2 - E), ':', color='tab:blue', lw=1)
ax1.plot(V3, 1 / (V3 - E), color='tab:blue', lw=1)
ax1.set_ylim(-0.5, 0.5)
#ax2.legend()

# Add labels to panels
font = {'weight': 'bold', 'fontsize': 14}
ax0.text(0.05, 0.88, 'A', font, transform=ax0.transAxes)
ax1.text(0.05, 0.88, 'B', font, transform=ax1.transAxes)
ax2.text(0.05, 0.88, 'C', font, transform=ax2.transAxes)
ax3.text(0.05, 0.88, 'D', font, transform=ax3.transAxes)

# Add legend
ax3.legend(loc=legend_location)

# Store
fig.savefig(base + '.png')
fig.savefig(base + '.pdf')
fig.savefig(base + '.eps')

