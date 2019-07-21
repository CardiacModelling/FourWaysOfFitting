#!/usr/bin/env python3
#
# Computation time versus number of evaluations
#
from __future__ import division, print_function
import os
import sys
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import results



hide_outliers = True



base = os.path.splitext(os.path.basename(__file__))[0]

# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

# Method colors
colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

labels = [
    'Method 1',
    'Method 2',
    'Method 3',
    'Method 4',
]

# Marker
marker = '.'
size = 2



#
# Create figure
#
fig = plt.figure(figsize=mm(90, 80), dpi=200)
fig.subplots_adjust(0.11, 0.1, 0.98, 0.99)

ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Evaluations per optimisation')
ax.set_ylabel('Time per optimisation (min)')

for method in [2, 3, 4]:
    i = method - 1
    xs = []
    ys = []

    for cell in range(1, 10):
        rs, ps, es, ts, ns = results.load(cell, method)
        xs.extend(ns)
        ys.extend(ts / 60)

    ax.plot(xs, ys, marker, color=colors[i], label=labels[i])

ax.legend(loc='upper right')

#
# Store
#

name = base
plt.savefig(name + '.png')
plt.savefig(name + '.pdf')

