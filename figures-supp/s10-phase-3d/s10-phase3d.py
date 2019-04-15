#!/usr/bin/env python3
#
# Three-dimension versions of the protocol phase plane plots.
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
from matplotlib.animation import FuncAnimation

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import plots
import sumstat


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 1:
    print('Syntax: ' + base + '.py <protocol>')
    sys.exit(1)
protocol = int(args[0])
print('Selected protocol ' + str(protocol))

# Set font
matplotlib.rc('font', family='arial', size=12)


#
# Create figure
#
fig = plt.figure(figsize=(9, 6))
plt.subplots_adjust(-0.01, 0.01, 1.05, 1.1)
ax = fig.gca(projection='3d')
ax.view_init(elev=20, azim=35)
plots.phase3d(ax, protocol)

s = 18
ax.set_xlabel(
    'Activated' + ' '*9 + 'Deactivated', fontsize=s, labelpad=10)
ax.set_ylabel(
    'Inactivated' + ' '*22 + 'Recovered', fontsize=s, labelpad=12)
ax.set_zlabel(
    'Voltage (mV)', fontsize=s, labelpad=10)



# Store
plt.savefig(base + '-pr' + (str(protocol)))
print('Done')

