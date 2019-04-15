#!/usr/bin/env python3
#
# Method and protocol performance
#
from __future__ import division, print_function
import os
import sys
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn
import pandas
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

# Tell seaborn to use my colours
palette = dict(zip(labels, colors))

#
# Create figure
#
fig = plt.figure(figsize=mm(170, 120), dpi=200)
fig.subplots_adjust(0.07, 0.05, 0.98, 0.99)
grid = GridSpec(2, 2, hspace=0.2, wspace=0.20)

# Marker size
size = 2


#
# Graph 1: Experimental time per method
#
ax00 = fig.add_subplot(grid[0, 0])
trad = 31.2 + 57.806 + 46.4096 + 92.9016
times = [trad, trad, trad, 8]
ax00.bar([1, 2, 3, 4], times, align='center', color=colors)
ax00.set_xticks([1, 2, 3, 4])
ax00.set_xticklabels(labels)
ax00.set_ylabel('Protocol duration (s)')





#
# Graph 2: Computational time per method
#
ax01 = fig.add_subplot(grid[0, 1])

xs = []
ys = []
for method in [2, 3, 4]:
    for cell in 1 + np.arange(9):
        t = results.load_times(cell, method)
        xs.extend(['Method ' + str(method)] * len(t))
        ys.append(t)
xs = np.array(xs)
ys = np.concatenate(ys) / 60        # Use minutes, not seconds

# Hide extremes
if hide_outliers:
    i = ys < 200
    xs = xs[i]
    ys = ys[i]
    plt.arrow(0.25, 155, 0, 30, width=0.05, head_length=10, color=colors[1])

# Create 'data frame'
df = pandas.DataFrame({
    'method' : xs,
    'time' : ys,
})
df['method'] = df['method'].astype('category')

seaborn.swarmplot(
    ax=ax01,
    data=df,
    x='method',
    y='time',
    hue='method',
    palette=palette,
    size=size,
)

# Set labels
ax01.get_legend().remove()
ax01.set_xlabel('')
ax01.set_ylabel('Time per optimisation (min)')




#
# Graph 3: Evaluation count per method
#
ax10 = fig.add_subplot(grid[1, 0])

xs = []
ys = []
for method in [2, 3, 4]:
    for cell in 1 + np.arange(9):
        f = results.load_evaluations(cell, method)
        xs.extend(['Method ' + str(method)] * len(f))
        ys.append(f)
xs = np.array(xs)
ys = np.concatenate(ys)

# Hide extremes
if hide_outliers:
    i = ys < 30000
    xs = xs[i]
    ys = ys[i]
    plt.arrow(
        0.25, 24000, 0, 4500, width=0.05, head_length=1500, color=colors[1])

# Create 'data frame'
df = pandas.DataFrame({
    'method' : xs,
    'evals' : ys,
})
df['method'] = df['method'].astype('category')

seaborn.swarmplot(
    axes=ax10,
    data=df,
    x='method',
    y='evals',
    hue='method',
    palette=palette,
    size=size,
)

# Set labels
ax10.get_legend().remove()
ax10.set_xlabel('')
ax10.set_ylabel('Evaluations per optimisation')



#
# Graph 4: Time per evaluation, per method
#
ax11 = fig.add_subplot(grid[1, 1])

xs = []
ys = []
for method in [2, 3, 4]:
    for cell in 1 + np.arange(9):
        f = results.load_times(cell, method)
        f /= results.load_evaluations(cell, method)
        xs.extend(['Method ' + str(method)] * len(f))
        ys.append(f)
xs = np.array(xs)
ys = np.concatenate(ys)

# Hide extremes
if hide_outliers:
    i = ys < 1.75
    xs = xs[i]
    ys = ys[i]
    plt.arrow(
        0.25, 1.3, 0, 0.3, width=0.05, head_length=0.1, color=colors[1])


# Create 'data frame'
df = pandas.DataFrame({
    'method' : xs,
    'evals' : ys,
})
df['method'] = df['method'].astype('category')

seaborn.swarmplot(
    axes=ax11,
    data=df,
    x='method',
    y='evals',
    hue='method',
    palette=palette,
    size=size,
)

# Set labels
ax11.get_legend().remove()
ax11.set_xlabel('')
ax11.set_ylabel('Mean time per evaluation (s)')
#'''




#
# Store
#

name = base
plt.savefig(name + '.png')
plt.savefig(name + '.pdf')

