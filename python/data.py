#!/usr/bin/env python3
#
# Python module that knows where all the data, models, and protocols are, and
# can load them.
#
from __future__ import division, print_function
import inspect
import myokit
import numpy as np
import os


# Get root of this project
try:
    frame = inspect.currentframe()
    ROOT = os.path.dirname(inspect.getfile(frame))
finally:
    del(frame)  # Must be manually deleted
ROOT = os.path.join(ROOT, '..')


# Data directory
DATA = os.path.join(ROOT, 'data')

# Model directory
MODEL = os.path.join(ROOT, 'model-and-protocols')

# Protocol directory
PROTO = os.path.join(ROOT, 'model-and-protocols')


def load(cell, protocol, cached=None, cap_filter=True):
    """
    Returns data for the given cell and protocol, with capacitance filtering
    applied.

    Arguments:

    ``cell``
        The cell to use (integer).
    ``protocol``
        The protocol to use (integer)
    ``cached``
        Optional cached data. If given, this will be returned directly.
    ``cap_filter``
        Enable capacitance filtering (default: True)

    Returns a myokit DataLog.
    """
    if cached is not None:
        return cached

    # Get path to data file
    trad = os.path.join(DATA, 'traditional-data')
    data_files = {
        1: os.path.join(trad, 'pr1-activation-kinetics-1-cell-' + str(cell)),
        2: os.path.join(trad, 'pr2-activation-kinetics-2-cell-' + str(cell)),
        3: os.path.join(trad, 'pr3-steady-activation-cell-' + str(cell)),
        4: os.path.join(trad, 'pr4-inactivation-cell-' + str(cell)),
        5: os.path.join(trad, 'pr5-deactivation-cell-' + str(cell)),
        6: os.path.join(DATA, 'validation-data', 'ap-cell-' + str(cell)),
        7: os.path.join(DATA, 'sine-wave-data', 'cell-' + str(cell)),
    }
    data_file = data_files[protocol]

    # Load protocol for capacitance filtering.
    variant = protocol < 3 and (cell == 7 or cell == 8)
    if variant:
        print('Loading variant protocol for capacitance filtering')
    else:
        print('Loading protocol for capacitance filtering')
    protocol = load_myokit_protocol(protocol, variant)

    # Load data from zip or csv
    if os.path.exists(data_file + '.zip'):
        print('Loading ' + data_file + '.zip')
        log = myokit.DataLog.load(data_file + '.zip').npview()
    else:
        print('Loading ' + data_file + '.csv')
        log = myokit.DataLog.load_csv(data_file + '.csv').npview()
        log.save(data_file + '.zip')

    # Apply capacitance filtering
    voltage = 'voltage' in log
    if cap_filter:
        dt = 0.1
        signals = [log.time(), log['current']]
        if voltage:
            signals.append(log['voltage'])
        signals = capacitance(protocol, dt, *signals)
    else:
        signals = [log.time(), log['current']]
        if voltage:
            signals.append(log['voltage'])

    log = myokit.DataLog()
    log.set_time_key('time')
    log['time'] = signals[0]
    log['current'] = signals[1]
    if voltage:
        log['voltage'] = signals[2]

    # Return
    return log


def save(cell, protocol, log):
    """
    Stores synthetic data for the given cell and protocol.

    Arguments:

    ``cell``
        The cell to use (integer).
    ``protocol``
        The protocol to use (integer)
    ``log``
        The log to store

    """
    # Test cell index
    if cell < 10:
        raise ValueError('Artificial cell index must be 10 or greater.')

    # Test log
    for key in ['time', 'current', 'voltage']:
        if key not in log:
            raise ValueError('Missing log entry: ' + key)

    # Get path to data file
    trad = os.path.join(DATA, 'traditional-data')
    data_files = {
        1: os.path.join(trad, 'pr1-activation-kinetics-1-cell-' + str(cell)),
        2: os.path.join(trad, 'pr2-activation-kinetics-2-cell-' + str(cell)),
        3: os.path.join(trad, 'pr3-steady-activation-cell-' + str(cell)),
        4: os.path.join(trad, 'pr4-inactivation-cell-' + str(cell)),
        5: os.path.join(trad, 'pr5-deactivation-cell-' + str(cell)),
        6: os.path.join(DATA, 'validation-data', 'ap-cell-' + str(cell)),
        7: os.path.join(DATA, 'sine-wave-data', 'cell-' + str(cell)),
    }
    data_file = os.path.abspath(data_files[protocol])

    # Store
    print('Storing cell ' + str(cell) + ' data for protocol ' + str(protocol)
          + ' to ' + data_file)
    log.save(data_file + '.zip')
    log.save_csv(data_file + '.csv')


def load_myokit_model():
    """
    Loads the HH version of the Beattie (Myokit) model.
    """
    return myokit.load_model(os.path.join(MODEL, 'beattie-2017-ikr-hh.mmt'))


def load_myokit_protocol(protocol, variant=False):
    """
    Loads the Myokit protocol with the given index (1-7). For Pr6 and Pr7, the
    protocol only has the steps for capacitance filtering.
    """
    protocol_files = {
        1: os.path.join(PROTO, 'pr1-activation-kinetics-1.mmt'),
        2: os.path.join(PROTO, 'pr2-activation-kinetics-2.mmt'),
        3: os.path.join(PROTO, 'pr3-steady-activation.mmt'),
        4: os.path.join(PROTO, 'pr4-inactivation.mmt'),
        5: os.path.join(PROTO, 'pr5-deactivation.mmt'),
        6: os.path.join(PROTO, 'pr6-ap-steps.mmt'),
        7: os.path.join(PROTO, 'pr7-sine-wave-steps.mmt'),
    }

    # Load variants for Pr1 and Pr2 for cells 7 and 8
    if variant:
        if protocol == 1:
            protocol = os.path.join(PROTO, 'pr1b.mmt')
        elif protocol == 2:
            protocol = os.path.join(PROTO, 'pr2b.mmt')
        else:
            raise ValueError('Variants only exist for Pr1 and Pr2')
    else:
        protocol = protocol_files[protocol]

    # Load Myokit protocol
    return myokit.load_protocol(protocol)


def load_ap_protocol():
    """
    Returns a tuple ``(times, values)`` representing Pr6.
    """
    data_file = os.path.join(DATA, 'validation-data', 'ap')

    # Load data from zip or csv
    if os.path.exists(data_file + '.zip'):
        print('Loading ' + data_file + '.zip')
        log = myokit.DataLog.load(data_file + '.zip').npview()
    else:
        print('Loading ' + data_file + '.csv')
        log = myokit.DataLog.load_csv(data_file + '.csv').npview()
        log.save(data_file + '.zip')

    return log


def load_protocol_values(protocol, variant=False):
    """
    Returns a (capacitance filtered) tuple ``(times, voltages)`` for the
    selected ``protocol``.
    """
    p = load_myokit_protocol(protocol, variant)

    if protocol == 6:
        log = load_ap_protocol().npview()
        t, v = log['time'], log['voltage']
    elif protocol == 7:
        m = load_myokit_model()
        m.get('membrane.V').set_rhs(
            'if(engine.time >= 3000.1 and engine.time < 6500.1,'
            + ' - 30'
            + ' + 54 * sin(0.007 * (engine.time - 2500.1))'
            + ' + 26 * sin(0.037 * (engine.time - 2500.1))'
            + ' + 10 * sin(0.190 * (engine.time - 2500.1))'
            + ', engine.pace)')
        p = load_myokit_protocol(protocol)
        s = myokit.Simulation(m, p)
        tmax = p.characteristic_time()
        t = np.arange(0, tmax, 0.1)
        v = s.run(tmax + 0.1, log=['membrane.V'], log_times=t)
        v = np.array(v['membrane.V'])
    else:
        t = np.arange(0, p.characteristic_time(), 0.1)
        v = np.array(p.value_at_times(t))

    return capacitance(p, 0.1, t, v)


def capacitance(protocol, dt, *signals):
    """
    Creates and applies a capacitance filter, based on a Myokit protocol.

    Arguments:

    ``protocol``
        A Myokit protocol.
    ``dt``
        The sampling interval of the given signals.
    ``signals``
        One or more signal files to filter.

    Returns a filtered version of the given signals.
    """
    cap_duration = 5    # Same as Kylie
    fcap = np.ones(len(signals[0]), dtype=int)
    steps = [step for step in protocol]
    for step in steps[1:]:
        i1 = int(step.start() / dt)
        i2 = i1 + int(cap_duration / dt)
        fcap[i1:i2] = 0
    fcap = fcap > 0

    if False:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(signals[0], signals[1])
        for step in steps[1:]:
            plt.axvline(step.start(), color='k', alpha=0.25)
        plt.show()

    # Apply filter
    return [x[fcap] for x in signals]


def model_path(model_file):
    """
    Returns the path to the given Myokit model file.
    """
    return os.path.join(MODEL, model_file)


def protocol_path(protocol_file):
    """
    Returns the path to the given Myokit protocol file.
    """
    return os.path.join(PROTO, protocol_file)
