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
fig1 = plt.figure(figsize=mm(80, 50), dpi=200)
fig2 = plt.figure(figsize=mm(80, 50), dpi=200)
fig3 = plt.figure(figsize=mm(80, 50), dpi=200)
fig4 = plt.figure(figsize=mm(80, 50), dpi=200)
fig1.subplots_adjust(0.12, 0.08, 0.98, 0.99)
fig2.subplots_adjust(0.12, 0.08, 0.98, 0.99)
fig3.subplots_adjust(0.15, 0.08, 0.98, 0.99)
fig4.subplots_adjust(0.13, 0.08, 0.98, 0.99)

ax00 = fig1.add_subplot(111)
ax01 = fig2.add_subplot(111)
ax10 = fig3.add_subplot(111)
ax11 = fig4.add_subplot(111)


# Marker size
size = 2


#
# Graph 1: Experimental time per method
#
print('Creating fig 1')

trad = 31.2 + 57.806 + 46.4096 + 92.9016
times = [trad, trad, trad, 8]
ax00.bar([1, 2, 3, 4], times, align='center', color=colors)
ax00.set_xticks([1, 2, 3, 4])
ax00.set_xticklabels(labels)
ax00.set_ylabel('Protocol duration (s)')

# Store
print('Storing fig 1')
name = base + '-1'
fig1.savefig(name + '.png')
fig1.savefig(name + '.pdf')
plt.close(fig1)



#
# Graph 2: Computational time per method
#
print('Creating fig 2')

xs = []
ys = []
for method in [2, 3, 4]:
    for cell in 1 + np.arange(9):
        t = results.load_times(cell, method)
        xs.extend(['Method ' + str(method)] * len(t))
        ys.append(t)
xs = np.array(xs)
ys = np.concatenate(ys) / 60        # Use minutes, not seconds

# Create 'data frame'
df1 = pandas.DataFrame({'method': xs, 'time': ys})
df1['method'] = df1['method'].astype('category')

# Hide extremes
if hide_outliers:
    ax01.set_ylim(-5, 202)
    i = ys < 200
    xs = xs[i]
    ys = ys[i]
    ax01.arrow(0.25, 155, 0, 30, width=0.05, head_length=10, color=colors[1])

    df2 = pandas.DataFrame({'method': xs, 'time': ys})
    df2['method'] = df2['method'].astype('category')
else:
    df2 = df1

args = {
    'ax': ax01,
    'x': 'method',
    'y': 'time',
    'hue': 'method',
    'palette': palette,
}
boxargs = {
    'dodge': False,
    'whis': np.inf,
    'boxprops': {
        'alpha': 0.15,
    },
    'whiskerprops': {
        'alpha': 0.15,
    },
    'capprops': {
        'alpha': 0.15,
    },
    'width': 0.9,
}

args['data'] = df1
seaborn.boxplot(**args, **boxargs)
args['data'] = df2
seaborn.swarmplot(size=size, **args)

# Set labels
ax01.get_legend().remove()
ax01.set_xlabel('')
ax01.set_ylabel('Time per optimisation (min)')

# Store
print('Storing fig 2')
name = base + '-2'
fig2.savefig(name + '.png')
fig2.savefig(name + '.pdf')
plt.close(fig2)



#
# Graph 3: Evaluation count per method
#
print('Creating fig 3')

xs = []
ys = []
for method in [2, 3, 4]:
    for cell in 1 + np.arange(9):
        f = results.load_evaluations(cell, method)
        xs.extend(['Method ' + str(method)] * len(f))
        ys.append(f)
xs = np.array(xs)
ys = np.concatenate(ys)

# Create 'data frame'
df1 = pandas.DataFrame({'method': xs, 'evals': ys})
df1['method'] = df1['method'].astype('category')


# Hide extremes
if hide_outliers:
    ax10.set_ylim(-800, 30500)
    i = ys < 30000
    xs = xs[i]
    ys = ys[i]
    ax10.arrow(
        0.25, 24000, 0, 4500, width=0.05, head_length=1500, color=colors[1])

    df2 = pandas.DataFrame({'method': xs, 'evals': ys})
    df2['method'] = df2['method'].astype('category')
else:
    df2 = df1

args['ax'] = ax10
args['y'] = 'evals'
args['data'] = df1
seaborn.boxplot(**args, **boxargs)
args['data'] = df2
seaborn.swarmplot(size=size, **args)


# Set labels
ax10.get_legend().remove()
ax10.set_xlabel('')
ax10.set_ylabel('Evaluations per optimisation')

# Store
print('Storing fig 3')
name = base + '-3'
fig3.savefig(name + '.png')
fig3.savefig(name + '.pdf')
plt.close(fig3)




#
# Graph 4: Time per evaluation, per method
#
print('Creating fig 4')

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

# Create 'data frame'
df1 = pandas.DataFrame({'method': xs, 'evals': ys})
df1['method'] = df1['method'].astype('category')

# Hide extremes
if hide_outliers:
    ax11.set_ylim(-0.07, 1.8)
    i = ys < 1.75
    xs = xs[i]
    ys = ys[i]
    ax11.arrow(
        0.25, 1.3, 0, 0.3, width=0.05, head_length=0.1, color=colors[1])

    df2 = pandas.DataFrame({'method': xs, 'evals': ys})
    df2['method'] = df2['method'].astype('category')
else:
    df2 = df1

args['ax'] = ax11
args['y'] = 'evals'
args['data'] = df1
seaborn.boxplot(**args, **boxargs)
args['data'] = df2
seaborn.swarmplot(size=size, **args)


# Set labels
ax11.get_legend().remove()
ax11.set_xlabel('')
ax11.set_ylabel('Mean time per evaluation (s)')

# Store
print('Storing fig 4')
name = base + '-4'
fig4.savefig(name + '.png')
fig4.savefig(name + '.pdf')
plt.close(fig4)

