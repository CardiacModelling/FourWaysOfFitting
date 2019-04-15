#!/usr/bin/env python3
#
# Figure: Fitting method 1
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
if len(args) != 1:
    print('Syntax:  ' + base + '.py <cell|all>')
    sys.exit(1)

if args[0] == 'all':
    cell_list = range(1, 10)
else:
    cell = int(args[0])

# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

for cell in cell_list:
    print('Selected cell ' + str(cell))

    # Create figure
    fig = plt.figure(figsize=mm(140, 140), dpi=200)
    grid = GridSpec(4, 2, wspace=0.2, hspace=0.2)

    # Steady state of activation
    ax00 = fig.add_subplot(grid[0, 0])
    ax00.set_xlabel('V (mV)')
    ax00.set_ylabel('Steady state activation')
    ax00.set_xlim(-124, 64)
    ax00.set_ylim(-0.1, 1.1)

    # Steady state of inactivation
    ax01 = fig.add_subplot(grid[0, 1])
    #ax01.set_xlabel('V (mV)')
    ax01.set_ylabel('Steady state inactivation')
    ax01.set_xlim(-130, 60)
    #ax01.set_ylim(-2, 4)

    # Rates
    ax10 = fig.add_subplot(grid[1, 0])
    #ax10.set_xlabel('V (mV)')
    ax10.set_ylabel('k1')
    ax10.set_xlim(-130, 70)

    ax11 = fig.add_subplot(grid[1, 1])
    #ax11.set_xlabel('V (mV)')
    ax11.set_ylabel('k4')
    ax11.set_xlim(-130, 70)

    # Log of rates
    ax20 = fig.add_subplot(grid[2, 0])
    #ax20.set_xlabel('V (mV)')
    ax20.set_ylabel('log k1')
    ax20.set_xlim(-130, 70)

    ax21 = fig.add_subplot(grid[2, 1])
    #ax21.set_xlabel('V (mV)')
    ax21.set_ylabel('log k4')
    ax21.set_xlim(-130, 70)

    # Time constant of activation
    ax30 = fig.add_subplot(grid[3, 0])
    ax30.set_xlabel('V (mV)')
    ax30.set_ylabel('Time constant of activation')
    ax30.set_xlim(-130, 70)

    # Time constant of inactivation
    ax31 = fig.add_subplot(grid[3, 1])
    ax31.set_xlabel('V (mV)')
    ax31.set_ylabel('Time constant of inactivation')
    ax31.set_xlim(-130, 70)

    # Plot all data
    marker = plots.cell_markers[cell - 1]
    label = 'Cell' + str(cell)

    ta, tr, ai, ri, iv = sumstat.all_summary_statistics(cell)
    ax00.plot(ai[0], ai[1], marker, label=label)
    ax01.plot(ri[0], ri[1], marker, label=label)
    ax30.plot(ta[0], ta[1], marker, label=label)
    ax31.plot(tr[0], tr[1], marker, label=label)

    def boltzmann(v, h, s):
        return 1 / (1 + np.exp(s * (h - v)))

    def rate_pos(v, a, b):
        return np.exp(a + b * v)

    def rate_neg(v, a, b):
        return np.exp(a - b * v)

    def line(v, a, b):
        return a + b * v


    from scipy.optimize import curve_fit
    popt, pcov = curve_fit(boltzmann, ai[0], ai[1], [-20, 0.03])
    ha, sa = popt
    va = np.linspace(-131, 71, 200)
    ax00.plot(va, boltzmann(va, ha, sa), 'k:')

    popt, pcov = curve_fit(boltzmann, ri[0], ri[1], [-60, -0.03])
    hr, sr = popt
    vr = np.linspace(-131, 71, 200)
    ax01.plot(vr, boltzmann(vr, hr, sr), 'k:')

    # Fit in normal space and log space
    x = ta[0]
    y = boltzmann(x, ha, sa) / ta[1]
    popt, pcov = curve_fit(rate_pos, x, y, [-10, 0.1])
    a1, b1 = popt
    r = ta[1] - boltzmann(x, ha, sa) / rate_pos(x, a1, b1)
    e = np.sqrt(np.sum(r**2) / len(r))
    popt, pcov = curve_fit(line, x, np.log(y), [-10, 0.1])
    a1x, b1x = popt
    rx = ta[1] - boltzmann(x, ha, sa) / rate_pos(x, a1x, b1x)
    ex = np.sqrt(np.sum(rx**2) / len(rx))
    print(a1)
    print(a1x)
    print(b1)
    print(b1x)
    print('rms act lin: ' + str(e))
    print('rms act log: ' + str(ex))
    ax10.plot(x, y, marker, label=label)
    ax10.plot(va, rate_pos(va, a1, b1), 'k:', label='Lin-fit')
    ax20.plot(x, np.log(y), marker, label=label)
    ax20.plot(va, line(va, a1x, b1x), 'k--', label='Log-fit')
    ax30.plot(
        va, boltzmann(va, ha, sa) / rate_pos(va, a1, b1), 'k:',
        label='Lin-fit RMS=' + str(round(e, 1)))
    ax30.plot(
        va, boltzmann(va, ha, sa) / rate_pos(va, a1x, b1x), 'k--',
        label='Log-fit RMS=' + str(round(ex, 1)))

    # Recovery
    x = tr[0]
    y = boltzmann(x, hr, sr) / tr[1]
    popt, pcov = curve_fit(rate_neg, x, y, [-5, 0.03])
    a4, b4 = popt
    r = tr[1] - boltzmann(x, hr, sr) / rate_neg(x, a4, b4)
    e = np.sqrt(np.sum(r**2) / len(r))
    popt, pcov = curve_fit(line, x, np.log(y), [-5.0, -0.03])
    a4x, b4x = popt
    b4x = -b4x
    rx = tr[1] - boltzmann(x, hr, sr) / rate_neg(x, a4x, b4x)
    ex = np.sqrt(np.sum(rx**2) / len(rx))
    print(a4)
    print(a4x)
    print(b4)
    print(b4x)
    print('rms act lin: ' + str(e))
    print('rms act log: ' + str(ex))
    ax11.plot(x, y, marker, label=label)
    ax11.plot(vr, rate_neg(vr, a4, b4), 'k:', label='Lin-fit')
    ax21.plot(x, np.log(y), marker, label=label)
    ax21.plot(vr, line(vr, a4x, -b4x), 'k--', label='Log-fit')
    ax31.plot(
        vr, boltzmann(vr, hr, sr) / rate_neg(vr, a4, b4), 'k:',
        label='Lin-fit RMS=' + str(round(e, 3)))
    ax31.plot(
        vr, boltzmann(vr, hr, sr) / rate_neg(vr, a4x, b4x), 'k--',
        label='Log-fit RMS=' + str(round(ex, 3)))


    # Set limits for ss inact
    ax01.set_ylim(min(1.1 * min(ri[1]), -0.1), max(1.1 * max(ri[1]), 1.1))

    # Add legends
    ax00.legend(loc='lower right')
    ax01.legend(loc='lower left')
    ax10.legend()
    ax11.legend()
    ax20.legend()
    ax21.legend()
    ax30.legend()
    ax31.legend()

    # Finalise
    fig.subplots_adjust(0.09, 0.07, 0.99, 0.99)
    fig.savefig(base + '-' + str(cell) + '.png')
    fig.savefig(base + '-' + str(cell) + '.pdf')


#plt.show()
