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
protocol = 5
model, time, voltage, current, act, rec = plots._phase_simulation(
    protocol, True)

steps = sumstat.pr5_steps_nocap
voltages = sumstat.pr5_voltages

#
# Create figure
#
fig = plt.figure(figsize=mm(170, 42), dpi=200)
grid = GridSpec(6, 4, wspace=0.35, hspace=0)

#
# Add plot of voltage
#
ax = fig.add_subplot(grid[0:2, 0])
ax.set_ylabel('V (mV)', labelpad=0.0)
ax.set_xticklabels([])
ax.yaxis.set_tick_params(labelsize=9)

plots.voltage(
    ax, 5, protocol, lw=1, technicolor=True, values=(time, voltage),
    cap_filter=False)

# Show P1,P2 labels
ax.text(0.143, 0.75, 'P1', transform=ax.transAxes)
ax.text(0.5, 0.54, 'P2', transform=ax.transAxes)

#xlim = (2650, 2750)
#ax.set_xlim(*xlim)


#
# Add plot of current
#
ax = fig.add_subplot(grid[2:6, 0])
ax.set_xlabel('Time (ms)')
ax.set_ylabel('I (nA)', labelpad=9.2)

d = myokit.DataLog()
d.set_time_key('time')
d['time'] = time
d['current'] = current
plots.current(ax, 5, protocol, lw=1, technicolor=True, log=d, cap_filter=False)

# Show start and end of current
tlo, thi = steps[0]
for lo, hi in steps:
    ax.plot(time[tlo], current[lo], 's', color='tab:blue')
    ax.plot(time[tlo+thi-1], current[lo+hi-1], 's', color='tab:green')

#ax.set_xlim(*xlim)

#
# Add phase diagram
#
ax = fig.add_subplot(grid[0:6, 1])
ax.set_xlabel('a')
ax.set_ylabel('r')
plots.phase(ax, protocol, sim=(model, act, rec))

# Show start and end of steps
for lo, hi in steps:
    ax.plot(act[lo+hi-1], rec[lo+hi-1], 's', color='tab:green')
ax.plot(act[lo], rec[lo], 's', color='tab:blue')


#
# Add plot of currents
#
ax = fig.add_subplot(grid[0:6, 2])
ax.set_xlabel('Time since P2 start')
ax.set_ylabel('I (nA)')

# Single exponential
def single(t, a, b, c):
    if c < 1:
        return np.ones(len(t)) * float('inf')
    return a + b * np.exp(-t / c)

# Double exponental
def f(t, a, b1, c1, b2, c2):
    if c1 < 1 or c2 < c1:
        return np.ones(len(t)) * float('inf')
    if b1 * b2 > 0:
        return np.ones(len(t)) * float('inf')
    return a + b1 * np.exp(-t / c1) + b2 * np.exp(-t / c2)

# Curve fitting
from scipy.optimize import curve_fit

lo, hi = steps[0]
t = time[lo:lo + hi] - time[lo]

cmap = matplotlib.cm.get_cmap(plots.colormap)
norm = matplotlib.colors.Normalize(0, (len(steps) - 1) * plots.cmap_fix)

tau_rec = []
tau_act = []
for i, lohi in enumerate(steps):
    lo, hi = lohi
    c = current[lo:lo + hi]
    ax.plot(t, c, color=cmap(norm(i)), lw=4, alpha=0.2)

    #p0 = c[-1], c[0] - c[-1], 10
    #popt, pcov = curve_fit(f, t, c, p0)
    #taus.append(popt[2])
    #ax.plot(t, f(t, *popt), 'k--', lw=1, alpha=0.5)

    # Guess some exponential parameters
    peak = np.argmax(np.abs(c))

    # Deactivation pre-fit, for guess
    guess = 200 if voltages[i] < -60 else 2000
    a2, b2, c2 = 0, c[peak], guess
    popt, pcov = curve_fit(single, t[peak:], c[peak:], [a2, b2, c2])
    a2, b2, c2 = popt

    # Recovery pre-fit, for guess
    guess = 5
    a1, b1, c1 = c[peak], -c[peak], guess
    if peak < 3:
        # Very fast: Only happens for simulations
        if debug: print('Too fast!')
        peak = 3
        a1, b1, c1 = -3, 3, 0.1
    popt, pcov = curve_fit(single, t[:peak], c[:peak], [a1, b1, c1])
    a1, b1, c1 = popt

    # Double exponential
    popt, pcov = curve_fit(f, t, c, [a1, b1, c1, b2, c2])
    tau_rec.append(popt[2])
    tau_act.append(popt[4])

    plt.plot(t, f(t, *popt), 'k:', lw=1)

    ax.plot(t[0], c[0], 's', color='tab:blue')
    ax.plot(t[-1], c[-1], 's', color='tab:green')



#
# Show model equation and approximation
#
ax = fig.add_subplot(grid[0:3, 3])
ax.set_xlabel('V (mV)')
ax.set_ylabel('Time const. (ms)')
p = results.load_kylie_parameters(5)
v = np.linspace(-160, 80, 180)
ax.plot(v, sumstat.model_time_constant_of_activation(v, p), label='Model')
ax.plot(voltages, tau_act, 's', color='tab:orange', label='Approx.')
#ax.set_ylim(0, 10000)
ax.legend(loc='upper center', ncol=2).get_frame().set_alpha(1)

ax = fig.add_subplot(grid[3:6, 3])
ax.set_xlabel('V (mV)')
ax.set_ylabel('Time const. (ms)')
p = results.load_kylie_parameters(5)
v = np.linspace(-160, 80, 180)
ax.plot(v, sumstat.model_time_constant_of_inactivation(v, p), label='Model')
ax.plot(voltages, tau_rec, 's', color='tab:orange')



# Finalise
fig.subplots_adjust(0.055, 0.17, 0.98, 0.97)
fig.savefig(base + '.png')

#plt.show()

