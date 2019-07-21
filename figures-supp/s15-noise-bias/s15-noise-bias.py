#!/usr/bin/env python3
#
# Error function plotted between true and best point
#
from __future__ import division, print_function
import os
import sys
import myokit
import numpy as np
import pints
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import errors
import results


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 1:
    print('Syntax: ' + base + '.py <method>')
    sys.exit(1)

methods = [int(x) for x in args[0].split(',')]

for method in methods:
    assert method in [2, 3, 4]

for method in methods:

    cell = 10

    # Set font
    font = {'family': 'arial', 'size': 10}
    matplotlib.rc('font', **font)

    # Matplotlib figure sizes are in inches
    def mm(*size):
        return tuple(x / 25.4 * 1.5 for x in size)


    # Create figure
    fig = plt.figure(figsize=mm(82, 35), dpi=200)
    fig.subplots_adjust(0.22, 0.21, 0.985, 0.92)

    ax = fig.add_subplot(1, 1, 1)

    # Get real parameters
    assert cell == 10
    ks = results.load_kylie_parameters(5)

    # Get obtained best parameters
    ps = results.load_parameters(cell, method)

    if ps is None:
        print('No data for cell ' + str(cell) + ' method ' + str(method))
        continue

    if method == 2:
        error = errors.E2(cell)
        error_name = '$E_{M2}$'
    elif method == 3:
        error = errors.E3(cell)
        error_name = '$E_{M3}$'
    elif method == 4:
        error = errors.E4(cell)
        error_name = '$E_{M4}$'
    else:
        raise NotImplementedError()

    padding = 0.45
    evaluations = 20


    # Generate some x-values near the given parameters
    s = np.linspace(-padding, 1 + padding, evaluations)

    # Direction
    r = ps - ks

    # Calculate function with other parameters fixed
    x = [ks + sj * r for sj in s]
    y = pints.evaluate(error, x, parallel=True)

    print('Error at kylie params   : ' + str(error(ks)))
    print('Error at obtained params: ' + str(error(ps)))

    # Plot
    ax.axvline(0, color='tab:blue', label='True parameters')
    ax.axvline(1, color='tab:orange', label='Best obtained')
    ax.plot(s, y, color='tab:green', label='Error function')
    ax.legend()
    ax.ticklabel_format(axis='y', useOffset=False, style='plain')

    ax.set_xlabel('Cross-section from $x_{true}$ to $x_{best}$')
    ax.set_ylabel(error_name)


    # Store
    name = base + '-method-' + str(method)
    fig.savefig(name + '.png')
    fig.savefig(name + '.pdf')

