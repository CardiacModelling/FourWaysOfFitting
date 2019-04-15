#!/usr/bin/env python3
#
# Figure 3: Summary curves
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
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Create figure
fig = plt.figure(figsize=mm(170, 90), dpi=200)
fig.subplots_adjust(0.062, 0.082, 0.89, 0.99)
legend_location = (1.05, 0.0)
grid = GridSpec(2, 1, hspace=0.3)
hi_grid = SubGridSpec(1, 3, subplot_spec=grid[0, 0], wspace=0.3)
lo_grid = SubGridSpec(1, 2, subplot_spec=grid[1, 0], wspace=0.35)

ax0 = fig.add_subplot(hi_grid[0, 0])
ax0.set_xlabel('V (mV)')
ax0.set_ylabel('Steady state of activation')
ax0.set_ylim(-0.1, 1.1)
ax1 = fig.add_subplot(hi_grid[0, 1])
ax1.set_xlabel('V (mV)')
ax1.set_ylabel('Steady state of inactivation')
ax1.set_ylim(-0.1, 1.3)
#ax1.set_ylim(-2, 4)
ax1.set_ylim(-0.1, 1.27)
ax2 = fig.add_subplot(hi_grid[0, 2])
ax2.set_xlabel('V (mV)')
ax2.set_ylabel('Pr5 Peak current (nA)')
ax3 = fig.add_subplot(lo_grid[0, 0])
ax3.set_xlabel('V (mV)')
ax3.set_ylabel('Time constant of activation (ms)')
ax4 = fig.add_subplot(lo_grid[0, 1])
ax4.set_xlabel('V (mV)')
ax4.set_ylabel('Time constant of inactivation (ms)')

ax0.axvline(0, color='gray', lw=0.5)
#ax1.axvline(0, color='gray', lw=0.5)
#ax2.axvline(0, color='gray', lw=0.5)
ax3.axvline(0, color='gray', lw=0.5)
ax4.axvline(0, color='gray', lw=0.5)

ax2.axhline(0, color='gray', lw=0.5)

# Plot time constant of activation
ai_v = ri_v = iv_v = ta_v = tr_v = None
ai_m, ri_m, iv_m, ta_m, tr_m = [], [], [], [], []

for i in range(9):
    cell = i + 1
    ta, tr, ai, ri, iv = sumstat.all_summary_statistics(cell)
    ai_v, ri_v, ta_v, tr_v, iv_v = ai[0], ri[0], ta[0], tr[0], iv[0]
    ai_m.append(ai[1])
    ri_m.append(ri[1])
    iv_m.append(iv[1])
    ta_m.append(ta[1])
    tr_m.append(tr[1])
    marker = plots.cell_markers[i]
    label = 'Cell ' + str(cell)
    ax0.plot(ai[0], ai[1], marker, label=label)
    ax1.plot(ri[0], ri[1], marker, label=label)
    ax2.plot(iv[0], iv[1], marker, label=label)
    ax3.plot(ta[0], ta[1], marker, label=label)
    ax4.plot(tr[0], tr[1], marker, label=label)

ax0.plot(ai_v, np.mean(ai_m, axis=0), 'k:', label='Mean', lw=1)
ax1.plot(ri_v, np.mean(ri_m, axis=0), 'k:', label='Mean', lw=1)
ax2.plot(iv_v, np.mean(iv_m, axis=0), 'k:', label='Mean', lw=1)
ax3.plot(ta_v, np.mean(ta_m, axis=0), 'k:', label='Mean', lw=1)
ax4.plot(tr_v, np.mean(tr_m, axis=0), 'k:', label='Mean', lw=1)

font = {'weight': 'bold', 'fontsize': 14}
ax0.text(0.03, 0.92, 'A', font, transform=ax0.transAxes)
ax1.text(0.91, 0.92, 'B', font, transform=ax1.transAxes)
ax2.text(0.03, 0.92, 'C', font, transform=ax2.transAxes)
ax3.text(0.02, 0.92, 'D', font, transform=ax3.transAxes)
ax4.text(0.02, 0.92, 'E', font, transform=ax4.transAxes)

ax2.legend(loc=legend_location)

# Finalise
fig.savefig(base + '.png')
fig.savefig(base + '.pdf')

