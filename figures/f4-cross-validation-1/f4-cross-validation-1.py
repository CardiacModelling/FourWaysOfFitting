#!/usr/bin/env python3
#
# Figure: Cross validation on model variables & experimental summary statistics
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
import plots
import results
import sumstat


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) not in (1, 2):
    print('Syntax: ' + base + '.py <cell|all> <variant>')
    sys.exit(1)

if args[0] == 'all':
    cell_list = range(1, 10)
else:
    cell_list = [int(args[0])]

variant = False
if len(args) == 2:
    variant = args[1] == 'variant'
if variant:
    print('Creating method 1b variant figure')


# Set font
font = {'family': 'arial', 'size': 10}
matplotlib.rc('font', **font)

# Matplotlib figure sizes are in inches
def mm(*size):
    return tuple(x / 25.4 * 1.5 for x in size)

labels = [
    'Fit 1',
    'Prediction 2',
    'Prediction 3',
    'Prediction 4',
]

colorv = 'k'
color0 = '#333333'
colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
]

marker0 = 's'
markers = [
    '-',
    '-',
    '-',
    '-',
]

if variant:
    labels.insert(1, 'Fit 1b')
    colors.insert(1, 'tab:cyan')
    markers.insert(1, '-')

vai = np.linspace(-100, 80, 180)
vri = np.linspace(-150, 80, 230)
vta = np.linspace(-140, 50, 190)
vtr = np.linspace(-130, 60, 180)

for cell in cell_list:
    print('Selected cell ' + str(cell))
    label0 = 'Cell' + str(cell)

    # Create figure
    fig = plt.figure(figsize=mm(82, 78), dpi=200)
    fig.subplots_adjust(0.15, 0.092, 0.99, 0.88)

    grid = GridSpec(2, 2, wspace=0.4, hspace=0.2)
    ax0 = fig.add_subplot(grid[0, 0])
    #ax0.set_xlabel('V (mV)')
    ax0.set_ylabel('Steady state of activation')
    ax1 = fig.add_subplot(grid[0, 1])
    #ax1.set_xlabel('V (mV)')
    ax1.set_ylabel('Steady state of inact.')
    ax2 = fig.add_subplot(grid[1, 0])
    ax2.set_xlabel('V (mV)')
    ax2.set_ylabel('Time constant of act. (ms)')
    ax3 = fig.add_subplot(grid[1, 1])
    ax3.set_xlabel('V (mV)')
    ax3.set_ylabel('Time constant of inact. (ms)')

    # Show x and y axes
    #ax0.axvline(0, color='gray', lw=0.5)
    #ax3.axvline(0, color='gray', lw=0.5)
    #ax4.axvline(0, color='gray', lw=0.5)

    # Plot
    ta, tr, ai, ri, iv = sumstat.all_summary_statistics(cell)
    args = {
        'color': color0,
        'label': label0,
    }

    ax0.plot(ai[0], ai[1], marker0, **args)
    ax1.plot(ri[0], ri[1], marker0, **args)
    ax2.plot(ta[0], ta[1], marker0, **args)
    ax3.plot(tr[0], tr[1], marker0, **args)

    if variant:
        todo = [
            {
                'cell': cell,
                'method': 1,
                'method_1b': False,
            },
            {
                'cell': cell,
                'method': 1,
                'method_1b': True,
            },
        ]
    else:
        todo = [
            {'cell': cell, 'method': 1},
            {'cell': cell, 'method': 2},
            {'cell': cell, 'method': 3},
            {'cell': cell, 'method': 4},
        ]

    for j, args in enumerate(todo):
        try:
            p = results.load_parameters(**args)
        except ValueError as e:
            print('Skipping option: ' + str(args))
            print('  ' + str(e))
            continue

        mai = sumstat.model_steady_state_activation(vai, p)
        mri = sumstat.model_steady_state_inactivation(vri, p)
        mta = sumstat.model_time_constant_of_activation(vta, p)
        mtr = sumstat.model_time_constant_of_inactivation(vtr, p)

        args = {
            'color': colors[j],
            'label': labels[j],
            'lw': 1 if j > 0 else 2,
        }
        ax0.plot(vai, mai, markers[j], **args)
        ax1.plot(vri, mri, markers[j], **args)
        ax2.plot(vta, mta, markers[j], **args)
        ax3.plot(vtr, mtr, markers[j], **args)



    # Add labels to panels
    #font = {'weight': 'bold', 'fontsize': 14}
    #ax0.text(0.05, 0.90, 'A', font, transform=ax0.transAxes)
    #ax1.text(0.87, 0.90, 'B', font, transform=ax1.transAxes)
    #ax2.text(0.05, 0.90, 'C', font, transform=ax2.transAxes)
    #ax3.text(0.05, 0.90, 'D', font, transform=ax3.transAxes)

    # Legend on top of figure
    ax0.legend(ncol=3, loc=(0, 1.05))

    # X-axes limits
    ax0.set_xlim(-89, 75)
    ax1.set_xlim(-135, 15)
    ax2.set_xlim(-135, 45)
    ax3.set_xlim(-125, 55)

    # Y-axes limits
    ax0.set_ylim(-0.05, 1.05)
    #ax1.set_ylim(-0.05, 1.27)
    ax1.set_ylim(-0.05, 1.05)

    # Store
    name = base + '-cell-' + str(cell)
    if variant:
        name += '-with-1b'
    fig.savefig(name + '.png')
    fig.savefig(name + '.pdf')
    plt.close(fig)

#plt.show()
