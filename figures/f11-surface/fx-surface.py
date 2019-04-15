#!/usr/bin/env python3
#
# Figure: Plot error surface in prior
#
from __future__ import division, print_function
import myokit
import numpy as np
import os
import sys

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import results


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 3:
    print('Syntax: ' + base + '.py <cell> <error> <n>')
    sys.exit(1)
cell = int(args[0])
method = int(args[1])
n = int(args[2])
filename = 'cell-' + str(cell) + '-surface-' + str(method) + '-' + str(n)



# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)


# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)


lower_alpha = 1e-7              # Kylie: 1e-7
upper_alpha = 1e3               # Kylie: 1e3
lower_beta  = 1e-7              # Kylie: 1e-7
upper_beta  = 0.4               # Kylie: 0.4

rmin = 1.67e-5
rmax = 1000
vmin = -120
vmax = 58.25


def prior12(ax):
    n = 1000
    b = np.linspace(lower_beta, upper_beta, n)
    a = np.linspace(np.log(lower_alpha), np.log(upper_alpha), n)
    bmin = (1 / vmax) * (np.log(rmin) - a)
    bmax = (1 / vmax) * (np.log(rmax) - a)
    bmin = np.maximum(bmin, lower_beta)
    bmax = np.minimum(bmax, upper_beta)

    ax.plot(a, bmin, color='white')
    ax.plot(a, bmax, color='white')

    ax.set_xlim(np.log(lower_alpha * 0.3), np.log(upper_alpha * 3))
    ax.set_ylim(lower_beta - 0.02, upper_beta + 0.02)


def prior34(ax):
    n = 1000
    b = np.linspace(lower_beta, upper_beta, n)
    a = np.linspace(np.log(lower_alpha), np.log(upper_alpha), n)
    bmin = (-1 / vmin) * (np.log(rmin) - a)
    bmax = (-1 / vmin) * (np.log(rmax) - a)
    bmin = np.maximum(bmin, lower_beta)
    bmax = np.minimum(bmax, upper_beta)

    ax.plot(a, bmin, color='white')
    ax.plot(a, bmax, color='white')

    ax.set_xlim(np.log(lower_alpha * 0.3), np.log(upper_alpha * 3))
    ax.set_ylim(lower_beta - 0.01, upper_beta * 0.5 + 0.01)


# Create figure
fig = plt.figure(figsize=mm(170, 47), dpi=200)
fig.subplots_adjust(0.057, 0.18, 0.99, 0.87)
grid = GridSpec(1, 4, wspace=0.33)

# P1/P2
ax0 = fig.add_subplot(grid[0, 0])
ax0.set_xlabel('log p1')
ax0.set_ylabel('p2')
prior12(ax0)

# P3/P4
ax1 = fig.add_subplot(grid[0, 1])
ax1.set_xlabel('log p3')
ax1.set_ylabel('p4')
prior34(ax1)

# P5/P6
ax2 = fig.add_subplot(grid[0, 2])
ax2.set_xlabel('log p5')
ax2.set_ylabel('p6')
prior12(ax2)

# P7/P8
ax3 = fig.add_subplot(grid[0, 3])
ax3.set_xlabel('log p7')
ax3.set_ylabel('p8')
prior34(ax3)

colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

markers = [
    'o',
    's',
    'x',
    '+',
]

popt = results.load_parameters(cell, method)
qopt = np.copy(popt)
qopt[0] = np.log(qopt[0])
qopt[2] = np.log(qopt[2])
qopt[4] = np.log(qopt[4])
qopt[6] = np.log(qopt[6])

if cell == 1:
    if method == 1:
        gmin = -7
        gmax = 1.5
    elif method == 2:
        gmin = -13
        gmax = 2
    elif method == 3:
        gmin = -2
        gmax = 3.5
    elif method == 4:
        gmin = -0.5
        gmax = 5
    elif method == 5:
        gmin = -1
        gmax = 4.5
    else:
        raise NotImplementedError
elif cell == 5:
    if method == 1:
        gmin = -7.5
        gmax = 1.5
    elif method == 2:
        gmin = 0.1
        gmax = 0.1
    elif method == 3:
        gmin = -1.5
        gmax = 3.5
    elif method == 4:
        gmin = -0.5
        gmax = 5
    elif method == 5:
        gmin = -0.1
        gmax = 5
    else:
        raise NotImplementedError
else:
    raise NotImplementedError


axes = [ax0, ax1, ax2, ax3]
for quad in [1, 2, 3, 4]:

    fname = os.path.join('..', '..', 'surface', filename + '-' + str(quad))
    fname = os.path.abspath(fname) + '.csv'
    if not os.path.exists(fname):
        print('File not found: ')
        print('  ' + fname)
        continue

    print('Loading results from ' + fname)
    d = myokit.DataLog.load_csv(fname).npview()

    # Extract ps and qs and fs
    ps = np.array([d['p' + str(1 + i)] for i in range(9)]).T
    qs = np.copy(ps)
    qs[:, 0] = np.log(qs[:, 0])
    qs[:, 2] = np.log(qs[:, 2])
    qs[:, 4] = np.log(qs[:, 4])
    qs[:, 6] = np.log(qs[:, 6])
    fs = d['f']

    # Transform f for plotting
    gs = -np.log(np.abs(fs))

    # Set manual, fixed boundaries for colormap
    print(np.min(gs[np.isfinite(gs)]), np.max(gs[np.isfinite(gs)]))
    assert np.min(gs[np.isfinite(gs)]) > gmin
    assert np.max(gs[np.isfinite(gs)]) < gmax

    # Remove -inf and nan
    gs[np.isinf(gs)] = gmin
    gs[np.isnan(gs)] = gmin

    # Make image
    # Convert to 2d array
    im = gs.reshape((n, n))
    # Transpose, so that rows are p2
    im = im.T
    # Flip y-axis
    im = im[::-1, :]

    # Plot image
    print('Plotting')
    ax = axes[quad - 1]
    i = 2 * (quad - 1)
    j = i + 1

    if False:
        norm = matplotlib.colors.Normalize(np.min(gs), np.max(gs))
        cmap = plt.cm.get_cmap('viridis')
        for k, q in enumerate(qs):
            ax.plot(q[i], q[j], 's', color=cmap(norm(gs[k])))
    else:
        xmin = np.min(qs[:, i])
        xmax = np.max(qs[:, i])
        ymin = np.min(qs[:, j])
        ymax = np.max(qs[:, j])
        dx = (xmax - xmin) / n
        dy = (ymax - ymin) / n
        extent = [
            xmin - 0.5 * dx,
            xmax + 0.5 * dx,
            ymin - 0.5 * dy,
            ymax + 0.5 * dy,
        ]
        ax.imshow(
            im,
            extent=extent,
            aspect='auto',
            vmin=gmin,
            vmax=gmax,
        )

    ax.plot(qopt[i], qopt[j], 'x', color='tab:orange')

# Add colour bar
axbar = plt.axes([0.1, 0.9, 0.8, 0.08])
axbar.set_xticks([])
axbar.set_yticks([])
for sp in axbar.spines:
    axbar.spines[sp].set_visible(False)

im = np.arange(100).reshape((1, 100))
axbar.imshow(im, extent=[-10, 0, 0, 0.2], aspect='auto')


font = {'weight': 'bold', 'fontsize': 14}
ax0.text(0.85, 0.85, 'A', font, transform=ax0.transAxes, color='white')
ax1.text(0.85, 0.85, 'B', font, transform=ax1.transAxes, color='white')
ax2.text(0.85, 0.85, 'C', font, transform=ax2.transAxes, color='white')
ax3.text(0.85, 0.85, 'D', font, transform=ax3.transAxes, color='white')


# Save
fname = base + '-cell-' + str(cell) + '-E' + str(method) + '-' + str(n)
fig.savefig(fname + '.png')
fig.savefig(fname + '.pdf')

#plt.show()
