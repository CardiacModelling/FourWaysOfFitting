#!/usr/bin/env python3
#
# Imports (leak-corrected, dofetilide subtracted) data from Kylie's traditional
# protocol experiments, as well as a protocol file (both in MatLab)
#
# Stores a CSV data file and a Myokit protocol file.
#
# Capacitance artefacts are NOT filtered out before storing, although filtered
# data is show for debugging purposes.
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

show_debug = False

#
# Check input arguments
#
args = sys.argv[1:]
if len(args) != 1:
    print('Syntax:  import.py <cell>')
    sys.exit(1)
icell = int(args[0])
print('Selected cell ' + str(icell))


#
# Import
#
cell = 'cell-' + str(icell)
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

protocols = [
    'activation_kinetics_1',
    'activation_kinetics_2',
    'steady_activation',
    'inactivation',
    'deactivation',
]

protocol_fancy_names = [
    'pr1-activation-kinetics-1',
    'pr2-activation-kinetics-2',
    'pr3-steady-activation',
    'pr4-inactivation',
    'pr5-deactivation',
]

repeats = [
    6,
    6,
    7,
    16,
    float('nan'), #9,
]

for ipro in range(5):

    idx = cells[cell]
    pro = protocols[ipro]

    # Load leak-corrected, dofetilide-subtracted IKr data from matlab file
    print('Reading matlab file with current data')
    mat = pro + '_' + idx + '_dofetilide_subtracted_leak_subtracted.mat'
    mat = scipy.io.loadmat(mat)
    current = mat['T']
    current = current[:,0]  # Convert from matrix to array
    del(mat)

    # Create times array, using dt=0.1ms
    dt = 0.1
    time = np.arange(len(current)) * dt

    # Load protocol from protocol file
    variation = ipro < 2 and icell in (7, 8)
    if not variation:

        # Load voltage from protocol.mat file
        print('Reading matlab protocol')
        mat = pro + '_protocol.mat'
        mat = scipy.io.loadmat(mat)
        vm = mat['T']
        vm = vm[:,0]  # Convert from matrix to array
        del(mat)

    else:

        # Exception for Pr1 and Pr2 in cells 7 and 8, which are the oldest two
        # recordings, and use different version of Pr1 and Pr2
        print('Reading myokit protocol')
        p = 'pr1b.mmt' if ipro == 0 else 'pr2b.mmt'
        p = myokit.load_protocol(os.path.join('..', '..', 'myokit', p))
        vm = p.create_log_for_times(time).npview()['pace']

    # Get jump times
    i = np.array([0] + list(np.where(np.abs(vm[1:] - vm[:-1]))[0]))
    start_guess = time[i]

    # Account for tiny shift in stored data
    start_guess[1:] += dt

    # Reduce rid of numerical issues
    start_guess = np.round(start_guess, 1)

    # Store protocol in Myokit file
    if not variation:
        filename = protocol_fancy_names[ipro] + '.mmt'
        print('  Writing protocol to ' + filename)
        level_guess = vm[i + 2]
        length_guess = list(start_guess)
        length_guess.append(time[-1] + (time[-1] - time[-2]))
        length_guess = np.array(length_guess)
        length_guess = length_guess[1:] - length_guess[:-1]

        # Reduce numerical issues
        length_guess = np.round(length_guess, 1)

        with open(filename, 'w') as f:
            f.write('[[protocol]]\n')
            f.write('# ' + protocol_fancy_names[ipro] + '\n')
            f.write('# Level Start   Length  Period  Multiplier\n')
            for k in range(len(start_guess)):
                for x in [level_guess, start_guess, length_guess]:
                    f.write(str(x[k]) + (8 - len(str(x[k]))) * ' ' )
                f.write('0       0\n')
        del(filename, level_guess, length_guess)

    jumps = start_guess[1:]
    del(start_guess, i)

    # Create datalog
    d = myokit.DataLog()
    d.set_time_key('time')
    d['time'] = time
    d['voltage'] = vm
    d['current'] = current

    # Store data in csv
    if True:
        filename = protocol_fancy_names[ipro] + '-' + cell + '.csv'
        print('  Writing data to ' + filename)
        d.save_csv(filename)
    print('Done')

    # Show folded data
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
        plt.ylabel('I (nA)')
        plt.legend()

        # Remove capacitance artefacts
        print('Removing capacitance artefacts for plot only')
        cap_duration = 5 # Same as Kylie (also, see for example step at 500ms)
        for t in jumps:
            # Get indices of capacitance start and end
            i1 = (np.abs(time - t)).argmin()
            i2 = (np.abs(time - t - cap_duration)).argmin()
            # Flatten signal during capacitance artefact
            current[i1:i2] = np.mean(current[i1-(i2-i1): i1])

        # Show data without capacitance artefacts
        plt.subplot(2,1,2)
        plt.plot(
            time, current, color='tab:orange', label='I (exp, cap flattened)')
        plt.legend()

        # Show folded data
        if np.isfinite(repeats[ipro]):
            print('Showing folded current data')
            period = (time[-1] + dt) / repeats[ipro]
            print('period: ' + str(period))
            d = d.fold(period)
            plt.figure()
            plt.subplot(1, 2, 1)
            for key in d.keys_like('voltage'):
                plt.plot(d.time(), d[key])
            plt.xlabel('Time (ms)')
            plt.ylabel('V (mV)')
            plt.subplot(1, 2, 2)
            for key in d.keys_like('current'):
                plt.plot(d.time(), d[key])
            plt.xlabel('Time (ms)')
            plt.ylabel('I (nA)')

        # Show graphs
        plt.show()

