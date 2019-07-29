#!/usr/bin/env python3
#
# Figure: Plot starting points on Method 2 surface
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
import boundaries
import results
import transformations


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 0:
    print('Syntax: ' + base + '.py')
    sys.exit(1)


cell = 5
method = 2
print('Selected cell: ' + str(cell))
print('Selected method: ' + str(method))



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
    a = np.linspace(np.log(lower_alpha), np.log(upper_alpha), n)
    b = np.linspace(lower_beta, upper_beta, n)

    bmin = (1 / vmax) * (np.log(rmin) - a)
    bmax = (1 / vmax) * (np.log(rmax) - a)
    bmin = np.maximum(bmin, lower_beta)
    bmax = np.minimum(bmax, upper_beta)
    ax.plot(a, bmin, color='white')
    ax.plot(a, bmax, color='white')

    x = [np.log(lower_alpha)] * 2
    y = [np.max(bmin), np.max(bmax)]
    ax.plot(x, y, color='white')

    ax.set_xlim(np.log(lower_alpha * 0.3), np.log(upper_alpha * 3))
    ax.set_ylim(lower_beta - 0.02, upper_beta + 0.02)


def prior34(ax):
    n = 1000
    a = np.linspace(np.log(lower_alpha), np.log(upper_alpha), n)
    b = np.linspace(lower_beta, upper_beta, n)

    bmin = (-1 / vmin) * (np.log(rmin) - a)
    bmax = (-1 / vmin) * (np.log(rmax) - a)
    bmin = np.maximum(bmin, lower_beta)
    bmax = np.minimum(bmax, upper_beta)
    ax.plot(a, bmin, color='white')
    ax.plot(a, bmax, color='white')

    x = [np.log(lower_alpha)] * 2
    y = [np.max(bmin), np.max(bmax)]
    ax.plot(x, y, color='white')

    ax.set_xlim(np.log(lower_alpha * 0.3), np.log(upper_alpha * 3))
    ax.set_ylim(lower_beta - 0.01, upper_beta * 0.5 + 0.01)


# Set min and max g
if cell == 5:
    if method == 1:
        gmin = -7.5
        gmax = 1.5
    elif method == 2:
        gmin = -13
        gmax = 2
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


# Load data for quads
quads = []
filename1 = 'cell-' + str(cell) + '-surface-' + str(method) + '-256-'
filename2 = 'cell-' + str(cell) + '-surface-' + str(method) + '-16-'
filename1 = os.path.abspath(os.path.join('..', '..', 'surface', filename1))
filename2 = os.path.abspath(os.path.join('..', '..', 'surface', filename2))
for quad in [1, 2, 3, 4]:
    n = 256
    fname = filename1 + str(quad) + '.csv'
    if not os.path.exists(fname):
        fname = filename2 + str(quad) + '.csv'
        if not os.path.exists(fname):
            print('File not found: ')
            print('  ' + fname)
            continue
        n = 16

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
    #print(np.min(gs[np.isfinite(gs)]), np.max(gs[np.isfinite(gs)]))
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

    # Get extent
    i = 2 * (quad - 1)
    j = i + 1

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

    quads.append((im, extent))


# Create figure
fig = plt.figure(figsize=mm(170, 120), dpi=200)
fig.subplots_adjust(0.056, 0.065, 0.99, 0.95)
grid = GridSpec(3, 4, wspace=0.33, hspace=0.08)

t0 = transformations.NullTransformation()
for row, tcode in enumerate('naf'):

    # Create axes
    ax0 = fig.add_subplot(grid[row, 0])
    ax1 = fig.add_subplot(grid[row, 1])
    ax2 = fig.add_subplot(grid[row, 2])
    ax3 = fig.add_subplot(grid[row, 3])

    # Draw prior
    prior12(ax0)
    prior34(ax1)
    prior12(ax2)
    prior34(ax3)

    # Add labels
    ax0.set_ylabel('p2')
    ax1.set_ylabel('p4')
    ax2.set_ylabel('p6')
    ax3.set_ylabel('p8')
    if row == 2:
        ax0.set_xlabel('log p1')
        ax1.set_xlabel('log p3')
        ax2.set_xlabel('log p5')
        ax3.set_xlabel('log p7')
    else:
        ax0.tick_params(axis='x', labelbottom=False)
        ax1.tick_params(axis='x', labelbottom=False)
        ax2.tick_params(axis='x', labelbottom=False)
        ax3.tick_params(axis='x', labelbottom=False)

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

    axes = [ax0, ax1, ax2, ax3]
    for quad, qdata in enumerate(quads):
        im, extent = qdata

        # Plot image
        ax = axes[quad]
        ax.imshow(
            im,
            extent=extent,
            aspect='auto',
            vmin=gmin,
            vmax=gmax,
        )

        ax.plot(np.log(popt[2*quad]), popt[2*quad+1], 'x', color='tab:orange')

    # Sample and plot
    trans = transformations.create(tcode)
    b = boundaries.Boundaries(t0, trans)
    ps = np.array([b.sample() for i in range(100)])
    for p in ps:
        assert(b.check(p))
    kw = {
        'color': 'white',
        'alpha': 1,
        'marker': 'o',
        'fillstyle': 'none',
        'linestyle': '',
    }
    ax0.plot(np.log(ps[:, 0]), ps[:, 1], **kw)
    ax1.plot(np.log(ps[:, 2]), ps[:, 3], **kw)
    ax2.plot(np.log(ps[:, 4]), ps[:, 5], **kw)
    ax3.plot(np.log(ps[:, 6]), ps[:, 7], **kw)

    # Add labels
    font = {'weight': 'bold', 'fontsize': 14}
    ax0.text(
        0.92, 0.85, tcode, font, transform=ax0.transAxes, color='white',
        horizontalalignment='right')


# Add colour bar
axbar = plt.axes([0.16, 0.97, 0.73, 0.02])
axbar.text(
    -0.01, 0.5, 'High RMSE',
    transform=axbar.transAxes,
    horizontalalignment='right', verticalalignment='center')
axbar.text(
    1.01, 0.5, 'Low RMSE', transform=axbar.transAxes,
    horizontalalignment='left', verticalalignment='center')

axbar.set_xticks([])
axbar.set_yticks([])
for sp in axbar.spines:
    axbar.spines[sp].set_visible(False)

im = np.arange(100).reshape((1, 100))
axbar.imshow(im, extent=[-10, 0, 0, 0.2], aspect='auto')


# Save
fname = base + '-cell-' + str(cell)
fig.savefig(fname + '.png')
fig.savefig(fname + '.pdf')

#plt.show()
