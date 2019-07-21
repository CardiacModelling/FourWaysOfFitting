#!/usr/bin/env python3
#
# Figure: Influence of error in inf on Method 1 tau estimation
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
from sumstat import simulate_all_summary_statistics as sim
from sumstat import model_steady_state_inactivation as ssi
from sumstat import model_time_constant_of_inactivation as tau
from sumstat import direct_fit_logarithmic as fit

cell = 5
base = os.path.splitext(os.path.basename(__file__))[0]

v = np.linspace(-140, 70)



#
# Shift and skey
#
dv1 = -20
dv2 = 20

ds1 = 0.7
ds2 = 1 / ds1



# Load Beattie et al. parameters for selected cell
p = results.load_kylie_parameters(cell)

# Create fake summary statistics (really good ones) with cell 5
ai = [np.array([-60, -40, -20, 0, 20, 40, 60])]
ai.append(sumstat.model_steady_state_activation(ai[0], p))
ta = [np.array([-120, -110, -100, -80, -70, -60, -50, -40, 40])]
ta.append(sumstat.model_time_constant_of_activation(ta[0], p))

tr = [np.array(
    [-120,-110,-100,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50])]
tr.append(tau(tr[0], p))
ri = [np.array([-120,-110,-100,-80,-70,-60,-50,-40])]
ri.append(tau(ri[0], p))
iv = [np.array([-120, -110, -100,  -80,  -70,  -60,  -50,  -40]),
      np.array([-3.1, -2.1, -1.11, 0.68, 1.29, 1.63,  1.74, 1.65])]


# Set font and legend handle length
font = {'family': 'arial', 'size': 9}
matplotlib.rc('font', **font)
matplotlib.rc('legend', handlelength=1)
matplotlib.rc('lines', markersize=4)
matplotlib.rc('lines', lw=1)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Create figure
fig = plt.figure(figsize=mm(170, 40), dpi=200)
grid = GridSpec(1, 2, wspace=0.25)

g0 = SubGridSpec(1, 2, subplot_spec=grid[0, 0], wspace=0.3)
g1 = SubGridSpec(1, 2, subplot_spec=grid[0, 1], wspace=0.3)

#
# Influence of shift
#

# r_inf
ax0 = fig.add_subplot(g0[0, 0])
ax0.set_xlabel('V (mV)')
ax0.set_ylabel('Steady state of inactivation')
ax0.set_ylim(-0.1, 1.1)
ax0.plot(v, ssi(v, p), 'k', lw=2)
ax0.plot(v, ssi(v, p, shift=dv1))
ax0.plot(v, ssi(v, p, shift=dv2))

# tau_r
ax1 = fig.add_subplot(g0[0, 1])
ax1.set_xlabel('V (mV)')
ax1.set_ylabel('Time constant of inactivation (ms)')
ax1.plot(tr[0], tr[1], 'ks')
ri[1] = ssi(ri[0], p)
q = fit(ta, tr, ai, ri, iv)
ax1.plot(v, tau(v, q), 'k', lw=2)
ri[1] = ssi(ri[0], p, shift=dv1)
q = fit(ta, tr, ai, ri, iv)
ax1.plot(v, tau(v, q))
ri[1] = ssi(ri[0], p, shift=dv2)
q = fit(ta, tr, ai, ri, iv)
ax1.plot(v, tau(v, q))



#
# Influence of slope
#

# r_inf
ax2 = fig.add_subplot(g1[0, 0])
ax2.set_xlabel('V (mV)')
ax2.set_ylabel('Steady state of inactivation')
ax2.set_ylim(-0.1, 1.1)
y = ssi(v, p, skew=1)
ax2.plot(v, y, 'k', lw=2)
y = ssi(v, p, skew=ds1)
ax2.plot(v, y)
y = ssi(v, p, skew=ds2)
ax2.plot(v, y)

# tau_r
ax3 = fig.add_subplot(g1[0, 1])
ax3.set_xlabel('V (mV)')
ax3.set_ylabel('Time constant of inactivation (ms)')
ax3.plot(tr[0], tr[1], 'ks')
ri[1] = ssi(ri[0], p, skew=1)
q = fit(ta, tr, ai, ri, iv)
ax3.plot(v, tau(v, q), 'k', lw=2)
ri[1] = ssi(ri[0], p, skew=ds1)
q = fit(ta, tr, ai, ri, iv)
ax3.plot(v, tau(v, q))
ri[1] = ssi(ri[0], p, skew=ds2)
q = fit(ta, tr, ai, ri, iv)
ax3.plot(v, tau(v, q))



# Finalise
fig.subplots_adjust(0.05, 0.17, 0.98, 0.98)
plt.savefig(base + '.png')
plt.savefig(base + '.pdf')

#plt.show()
