#!/usr/bin/env python3
#
# Imports (leak-corrected, dofetilide subtracted) data from Kylie's AP
# protocol experiments, as well as a (CSV, fixed-form) protocol file.
#
# Stores a CSV data file and a CSV protocol file.
#
# No filtering is performed.
#
from __future__ import print_function
import os
import sys
import numpy as np
import scipy
import scipy.io
import matplotlib.pyplot as plt
import myokit
import myokit.formats.axon

#
# Check input arguments
#
args = sys.argv[1:]
if len(args) != 1:
    print('Syntax:  import.py <cell>')
    sys.exit(1)
cell = int(args[0])
print('Selected cell ' + str(cell))


show_debug = True

cells = {
    1: '16713003',
    2: '16715049',
    3: '16708016',
    4: '16708060',
    5: '16713110',
    6: '16708118',
    7: '16704007',
    8: '16704047',
    9: '16707014',
}

protocol = 'ap'

idx = cells[cell]
pro = protocol

# Load protocol from protocol file
print('Reading matlab protocol')
mat = pro + '_protocol.mat'
mat = scipy.io.loadmat(mat)
vm = mat['T']
vm = vm[:,0]  # Convert from matrix to array
del(mat)

# Load leak-corrected, dofetilide-subtracted IKr data from matlab file
print('Reading matlab data')
mat = pro + '_' + idx + '_dofetilide_subtracted_leak_subtracted.mat'
mat = scipy.io.loadmat(mat)
current = mat['T']
current = current[:,0]  # Convert from matrix to array
del(mat)

# Create times array, using dt=0.1ms
dt = 0.1
time = np.arange(len(current)) * dt

# Store data in csv & binary
d = myokit.DataLog()
d.set_time_key('time')
d['time'] = time
d['voltage'] = vm
d['current'] = current

filename = protocol + '-cell-' + str(cell) + '.zip'
print('  Writing data to ' + filename)
d.save(filename)

filename = protocol + '-cell-' + str(cell) + '.csv'
print('  Writing data to ' + filename)
d.save_csv(filename)

# Store protocol in csv & binary
del(d['current'])
filename = protocol + '.zip'
print('  Writing data to ' + filename)
d.save(filename)

filename = protocol + '.csv'
print('  Writing data to ' + filename)
d.save_csv(filename)

print('Done')
