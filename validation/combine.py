#!/usr/bin/env python3
#
# Create combined (multi-cell) error measures for all 4 methods, and all 5
# criteria
#
from __future__ import division, print_function
import os
import sys
import myokit
import numpy as np

#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) > 1:
    print('Syntax: ' + base + '.py <variant>')
    sys.exit(1)

variant = False
if len(args) == 1:
    variant = args[0] == 'variant'
if variant:
    print('Running for method 1b variant')



r = []
for i in range(9):
    log = myokit.DataLog.load_csv('rms-errors-cell-' + str(1 + i) + '.csv')
    r.append([log['rms' + str(1 + j)] for j in range(5)])
r = np.array(r)

print(r.shape)

# Get mean and std
rm = np.mean(r, axis=0)
rs = np.std(r, axis=0)

print(rm.shape)
print(rs.shape)
print(rm)
print(rs)

# Get minimum of each row (as a column vector)
norm = np.min(rm, axis=1).reshape((5, 1))
print(norm)

# Normalise both the mean and the stddev (linear transformation, so OK!)
rm /= norm
rs /= norm
print(rm)
print(rs)

# Store
filename = 'rms-errors'
if variant:
    filename += '-with-1b'
filename += '.csv'
print('Saving to ' + filename)

log = myokit.DataLog()
for j, r in enumerate(rm):
    log['rms' + str(1 + j) + '_rel'] = r
for j, r in enumerate(rs):
    log['rms' + str(1 + j) + '_rel_std'] = r
log.save_csv(filename)

