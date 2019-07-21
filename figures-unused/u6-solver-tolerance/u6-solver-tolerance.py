#!/usr/bin/env python3
#
# Show difference made by solver tolerances
#
from __future__ import division, print_function
import os
import sys
import pints
import numpy as np

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import cells
import data
import model
import results

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) > 2:
    print('Syntax: ' + base + '.py <cell> <protocol>')
    sys.exit(1)
if len(args) < 2:
    protocol = 7
else:
    protocol = int(args[1])
if len(args) < 1:
    cell = 5
else:
    cell = int(args[0])
print('Selected cell ' + str(cell))
print('Selected protocol ' + str(protocol))

if protocol < 1 or protocol > 7:
    print('Unknown protocol Pr' + str(protocol))
    sys.exit(1)
if protocol == 6:
    raise NotImplementedError

#
# Define error function
#

# Create forward model
m = model.Model(
    data.load_myokit_protocol(protocol),
    cells.reversal_potential(cells.temperature(cell)),
    sine_wave=(protocol == 7),
    start_steady=True,
)

# Load data, create single output problem
log = data.load(cell, 7)
time = log.time()
current = log['current']
voltage = log['voltage']
del(log)

# Create single output problem
problem = pints.SingleOutputProblem(m, time, current)

# Define error function
f = pints.RootMeanSquaredError(problem)

#
# Load solution from sine wave fitting
#
popt = results.load_parameters(cell, 4) # Always from sine wave fitting!

#
# Create figure
#

# Set font
font = {'family': 'arial', 'size': 9}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Create figure
#tolerances = ['1e-1', '1e-2', '1e-3', '1e-4', 1e-6, 1e-8]
tolerances = ['1e-4', 1e-6, 1e-8]
panels = len(tolerances) + (0 if protocol == 7 else 1)

fig = plt.figure(figsize=mm(170, 40), dpi=200)
fig.subplots_adjust(0.06, 0.17, 0.99, 0.92)
grid = GridSpec(1, panels, wspace=0.33)

n = 100
xlo = 0.995
xhi = 1.005
p1s = np.linspace(popt[0] * xlo, popt[0] * xhi, n)
ps = popt.reshape(1, 9).repeat(n, axis=0)
ps[:, 0] = p1s

for i, tol in enumerate(tolerances):
    print('Evaluating for ' + str(tol))
    m.set_tolerances(float(tol))
    fs = [f(p) for p in ps]

    ax = fig.add_subplot(grid[0, i])
    ax.set_xlabel('$p_1$')
    ax.set_ylabel('Score')
    ax.ticklabel_format(style='sci', scilimits=(0, 0))

    ax.plot(p1s, fs, lw=1, label='tol=' + str(tol))
    ax.legend().get_frame().set_alpha(1)

if protocol < 7:
    print('Evaluating in analytical mode')
    m.set_tolerances(1e-4)
    problem._model = model.Model(
        data.load_myokit_protocol(protocol),
        cells.reversal_potential(cells.temperature(cell)),
        sine_wave=False,
        start_steady=True,
        analytical=True,
    )
    fs = [f(p) for p in ps]

    ax = fig.add_subplot(grid[0, -1])
    ax.set_xlabel('$p_1$')
    ax.set_ylabel('Score')
    ax.ticklabel_format(style='sci', scilimits=(0, 0))

    ax.plot(p1s, fs, lw=1, label='analytical')
    ax.legend().get_frame().set_alpha(1)

plt.savefig(base + '-cell-' + str(cell) + '-pr-' + str(protocol) + '.png')
plt.savefig(base + '-cell-' + str(cell) + '-pr-' + str(protocol) + '.pdf')

#plt.show()

