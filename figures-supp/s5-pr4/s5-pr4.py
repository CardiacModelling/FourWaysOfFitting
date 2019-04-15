#!/usr/bin/env python3
#
# Figure: Pr4 and analysis
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
import data
import plots
import results
import sumstat


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 0:
    print('Syntax:  ' + base + '.py')
    sys.exit(1)
print('Using parameters from cell 5')


# Set font
font = {'family': 'arial', 'size': 9}
matplotlib.rc('font', **font)


# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Run simulation
protocol = 4
model, time, voltage, current, act, rec = plots._phase_simulation(
    protocol, True)

# Get info about protocol
steps = sumstat.pr4_steps_nocap
voltages = sumstat.pr4_voltages


#
# Create figure
#
fig = plt.figure(figsize=mm(170, 42), dpi=200)
grid = GridSpec(3, 4, wspace=0.35, hspace=0)

#
# Add plot of voltage
#
ax = fig.add_subplot(grid[0, 0])
ax.set_ylabel('V (mV)', labelpad=0.0)
ax.set_xticklabels([])
ax.yaxis.set_tick_params(labelsize=9)

plots.voltage(
    ax, 5, protocol, lw=1, technicolor=True, values=(time, voltage),
    cap_filter=False)

# Show P1,P2 labels
ax.text(0.27, 0.75, 'P1', transform=ax.transAxes)
ax.text(0.305, 0.11, 'P2', transform=ax.transAxes)
ax.text(0.49, 0.75, 'P3', transform=ax.transAxes)


#
# Add plot of current
#
ax = fig.add_subplot(grid[1:3, 0])
ax.set_xlabel('Time (ms)')
ax.set_ylabel('I (nA)', labelpad=9.2)

d = myokit.DataLog()
d.set_time_key('time')
d['time'] = time
d['current'] = current
plots.current(ax, 5, protocol, lw=1, technicolor=True, log=d, cap_filter=False)


#
# Add phase diagram
#
ax = fig.add_subplot(grid[0:3, 1])
ax.set_xlabel('a')
ax.set_ylabel('r')
plots.phase(ax, protocol, sim=(model, act, rec))

# Show start and end of steps
for lo, hi in steps:
    ax.plot(act[lo+hi-1], rec[lo+hi-1], 's', color='tab:green')
ax.plot(act[lo], rec[lo], 's', color='tab:blue')


t, c = data.capacitance(data.load_myokit_protocol(4), 0.1, time, current)
log = myokit.DataLog()
log.set_time_key('time')
log['time'] = t
log['current'] = c
print(sumstat.time_constant_of_inactivation_pr4(5, log))

#
# Add plot of current fitting
#
from scipy.optimize import curve_fit

def f(t, a, b, c):
    if c <= 0:
        return np.ones(t.shape) * float('inf')
    return a + b * np.exp(-t / c)

ax = fig.add_subplot(grid[0:3, 2])
ax.set_xlabel('Time since P3 start (ms)')
ax.set_ylabel('I (nA)')
t = time[steps[0][0]:sum(steps[0])]
t -= t[0]
cmap = matplotlib.cm.get_cmap(plots.colormap)
norm = matplotlib.colors.Normalize(0, (len(steps) - 1) * plots.cmap_fix)
taus = []
for i, lohi in enumerate(steps):
    lo, hi = lohi
    c = current[lo:lo + hi]
    ax.plot(t, c, color=cmap(norm(i)), lw=4, alpha=0.2)

    p0 = c[-1], c[0] - c[-1], 10
    popt, pcov = curve_fit(f, t, c, p0)
    taus.append(popt[2])
    ax.plot(t, f(t, *popt), 'k--', lw=1, alpha=0.5)

    ax.plot(t[0], c[0], 's', color='tab:blue')
    ax.plot(t[-1], c[-1], 's', color='tab:green')

#
# Show model equation and approximation
#
ax = fig.add_subplot(grid[0, 3])
ax.set_xlabel('V (mV)')
ax.set_ylabel('t.c. (ms)')
p = results.load_kylie_parameters(5)
v = np.linspace(-100, 80, 180)
ax.plot(v, sumstat.model_time_constant_of_inactivation(v, p), label='Model')
ax.plot(voltages, taus, 's', color='tab:orange', label='Approximation')
ax.set_xticks([])
ax.set_yticks([0, 100, 200])
ax.legend(loc='upper right')

ax = fig.add_subplot(grid[1:3, 3])
ax.set_xlabel('V (mV)')
ax.set_ylabel('Time constant (ms)')
p = results.load_kylie_parameters(5)
ax.plot(v, sumstat.model_time_constant_of_inactivation(v, p), label='Model')
ax.plot(voltages, taus, 's', color='tab:orange', label='Approximation')
ax.set_ylim(5, 18)
ax.set_yticks([5, 10, 15])


# Finalise
fig.subplots_adjust(0.055, 0.17, 0.98, 0.97)
fig.savefig(base + '.png')

#plt.show()

