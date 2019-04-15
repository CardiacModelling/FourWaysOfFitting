#!/usr/bin/env python3
#
# Figure: Pr3 and analysis
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
protocol = 3
model, time, voltage, current, act, rec = plots._phase_simulation(
    protocol, True)

# Find (indices of) peaks during P2
ipeaks = []
for i, j in sumstat.pr3_steps_nocap:
    ipeaks.append(i + np.argmax(current[i:i + j]))


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
#ax.text(0.35, 0.12, 'P1', transform=ax.transAxes)
ax.text(5800, -30, 'P2')

ax.set_xlim(5500, 6700)


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

# Show peaks
for i, ipeak in enumerate(ipeaks):
    ax.plot(time[ipeak - i * 82580], current[ipeak], 's', color='tab:blue')

ax.set_xlim(5500, 6700)

#
# Add phase diagram
#
ax = fig.add_subplot(grid[0:3, 1])
ax.set_xlabel('a')
ax.set_ylabel('r')
plots.phase(ax, protocol, sim=(model, act, rec))

# Show peaks
r = []
for i, ipeak in enumerate(ipeaks):
    ax.plot(act[ipeak], rec[ipeak], 's', color='tab:blue')
    r.append(rec[ipeak])
r = np.mean(r)
ax.axhline(r, linestyle=':')


#
# Add plot of peaks
#
ax = fig.add_subplot(grid[0:3, 2])
ax.set_xlabel('P1 voltage (mV)')
ax.set_ylabel('$I_{peak}$ (nA)')
voltages = sumstat.pr3_voltages
peaks = []
for i, ipeak in enumerate(ipeaks):
    peak = current[ipeak]
    ax.plot(voltages[i], peak, 's', color='tab:blue')
    peaks.append(peak)


#
# Show model equation and approximation
#
ax = fig.add_subplot(grid[0:3, 3])
ax.set_xlabel('V (mV)')
ax.set_ylabel('Steady state (-)')
p = results.load_kylie_parameters(5)
v = np.linspace(-100, 80, 180)
ax.plot(v, sumstat.model_steady_state_activation(v, p), label='Model')
peaks = np.array(peaks)
peaks /= np.max(peaks)
ax.plot(voltages, peaks, 's', color='tab:orange', label='Approximation')
ax.set_ylim(-0.03, 1.4)

#ax.set_ylim(0, 1000)
ax.legend(loc='upper left').get_frame().set_alpha(1)


# Finalise
fig.subplots_adjust(0.055, 0.17, 0.98, 0.97)
fig.savefig(base + '.png')

#plt.show()

