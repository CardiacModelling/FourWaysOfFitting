#!/usr/bin/env python3
#
# Figure: Simulated summary statistics don't match model variables
#
from __future__ import division, print_function
import os
import sys
import numpy as np
#import myokit
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import plots
import results
import sumstat

base = os.path.splitext(os.path.basename(__file__))[0]
cell = 5


# Load Beattie et al. parameters for selected cell
parameters = results.load_kylie_parameters(5)

# Simulate all protocols for this cell/param combo
pr2, pr3, pr4, pr5 = sumstat.simulate_pr2345(cell, parameters)

# Set font
font = {'family': 'arial', 'size': 9}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Create figure
fig = plt.figure(figsize=mm(170, 38), dpi=200)
grid = GridSpec(1, 4, wspace=0.35)

marker = '??s^+*'
color = ['k', 'k', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red']

# a_inf
ax0 = fig.add_subplot(grid[0, 0])
ax0.set_xlabel('V (mV)')
ax0.set_ylabel('Steady state of activation')
ax0.set_ylim(-0.1, 1.1)
v = np.linspace(-80, 60)
ra = sumstat.model_steady_state_activation(v, parameters)
ax0.plot(v, ra, label='$a_\infty$', color=color[0])
v, ra = sumstat.steady_state_activation_pr3(cell, pr3)
ax0.plot(v, ra, label='Pr3', color=color[3], marker=marker[3])
ax0.legend(loc='upper left')

# r_inf
ax1 = fig.add_subplot(grid[0, 1])
ax1.set_xlabel('V (mV)')
ax1.set_ylabel('Steady state of inactivation')
ax1.set_ylim(-0.1, 1.1)
v = np.linspace(-140, 40)
ri = sumstat.model_steady_state_inactivation(v, parameters)
ax1.plot(v, ri, label='$r_\infty$', color=color[0])
v, ri = sumstat.steady_state_inactivation_pr5(cell, pr5)
ax1.plot(v, ri, label='Pr5', color=color[5], marker=marker[5])
ax1.legend(loc='upper right')

# tau_a
ax2 = fig.add_subplot(grid[0, 2])
ax2.set_xlabel('V (mV)')
ax2.set_ylabel('Time constant of activation (ms)')
v = np.linspace(-140, 40)
ta = sumstat.model_time_constant_of_activation(v, parameters)
ax2.plot(v, ta, label='$\\tau_a$', color=color[0])
v, ta = sumstat.time_constant_of_activation_pr2(cell, pr2)
ax2.plot(v, ta, label='Pr2', color=color[2], marker=marker[2])
v, ta = sumstat.time_constant_of_activation_pr5(cell, pr5)
ax2.plot(v, ta, label='Pr5', color=color[5], marker=marker[5])
ax2.legend(loc='upper left')

# tau_r
ax3 = fig.add_subplot(grid[0, 3])
ax3.set_xlabel('V (mV)')
ax3.set_ylabel('Time constant of inactivation (ms)')
v = np.linspace(-120, 60)
tr = sumstat.model_time_constant_of_inactivation(v, parameters)
ax3.plot(v, tr, label='$\\tau_r$', color=color[0])
v, tr = sumstat.time_constant_of_inactivation_pr4(cell, pr4)
ax3.plot(v, tr, label='Pr4', color=color[4], marker=marker[4])
v, tr = sumstat.time_constant_of_inactivation_pr5(cell, pr5)
ax3.plot(v, tr, label='Pr5', color=color[5], marker=marker[5])
ax3.set_ylim(0, 22)
ax3.legend(loc='upper right')


# Finalise
fig.subplots_adjust(0.05, 0.17, 0.99, 0.96)
plt.savefig(base + '.png')
plt.savefig(base + '.pdf')

#plt.show()
