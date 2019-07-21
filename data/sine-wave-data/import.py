#!/usr/bin/env python
#
# Imports Kylie's (leak-corrected, dofetilide subtracted) sine-wave data,
# stores it as CSV.
#
# Leak capacitance artefacts are NOT removed in the stored data, but data is
# shown without them for debugging purposes.
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

show_debug = True

cell = 9
print('Selected cell ' + str(cell))

cell = 'cell-' + str(cell)
cells = {
    'cell-1': '16713003',
    'cell-2': '16715049',
    'cell-3': '16708016',
    'cell-4': '16708060',
    'cell-5': '16713110',
    'cell-6': '16708118',
    'cell-7': '16704007',
    'cell-8': '16704047',
    'cell-9': '16707014',
}

idx = cells[cell]

# Load protocol from protocol file
print('Reading matlab protocol')
mat = 'sine_wave_protocol.mat'
mat = scipy.io.loadmat(mat)
vm = mat['T']
vm = vm[:,0]  # Convert from matrix to array
del(mat)

# Load leak-corrected, dofetilide-subtracted IKr data from matlab file
print('Reading matlab data')
mat = 'sine_wave_' + idx + '_dofetilide_subtracted_leak_subtracted.mat'
mat = scipy.io.loadmat(mat)
current = mat['T']
current = current[:,0]  # Convert from matrix to array
del(mat)

# Create times array, using dt=0.1ms
time = np.arange(len(current)) * 0.1

# Correct tiny shift in stored data (doubling final point)
#vm[:-1] = vm[1:]
#current[:-1] = current[1:]

# Store data as csv/zip
d = myokit.DataLog()
d.set_time_key('time')
d['time'] = time
d['voltage'] = vm
d['current'] = current

filename = cell + '.zip'
print('  Writing data to ' + filename)
d.save(filename)
filename = cell + '.csv'
print('  Writing data to ' + filename)
d.save_csv(filename)

print('Done!')

# Store protocol as csv/zip
del(d['current'])
filename = 'sine-wave.zip'
print('  Writing protocol to ' + filename)
d.save(filename)
filename = 'sine-wave.csv'
print('  Writing protocol to ' + filename)
d.save_csv(filename)

# Show debug data
if show_debug:
    # Show data with capacitance artefacts
    print('Plotting data with artefacts')
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(time, vm, color='darkgreen', label='V (exp)')
    plt.xlabel('Time (ms)')
    plt.ylabel('V (mV)')
    plt.legend()
    plt.subplot(2,1,2)
    plt.plot(time, current, color='darkblue', label='I (exp)')
    plt.xlabel('Time (ms)')
    plt.ylabel('Current (nA)')
    plt.legend()

    # Remove capacitance artefacts
    print('Flattening capacitance for plotting only')
    cap_duration = 5  # Same as Kylie
    jumps = [
        250,
        300,
        500,
        1500,
        2000,
        3000,
        6500,
        7000,
        ]
    for t in jumps:
        # Get indices of capacitance start and end
        i1 = (np.abs(time-t)).argmin()
        i2 = (np.abs(time-t-cap_duration)).argmin()
        # Remove data points during capacitance artefact
        current[i1:i2] = np.mean(current[i1-(i2-i1): i1])

    # Show data without capacitance artefacts
    plt.subplot(2,1,2)
    plt.plot(time, current, color='tab:orange', label='I (exp, cap flattened)')
    plt.legend()
    plt.show()
