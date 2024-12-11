#!/usr/bin/env python3
#
# Summary statistic calculations for the traditional protocols.
#
from __future__ import division, print_function
import myokit
import numpy as np

# Import local modules
import data
import cells


parameter_names = [
    'ikr.p1',
    'ikr.p2',
    'ikr.p3',
    'ikr.p4',
    'ikr.p5',
    'ikr.p6',
    'ikr.p7',
    'ikr.p8',
    'ikr.p9',
]

pr2_steps = [
    (5712, 24951),
    (57533, 24949),
    (109482, 24950),
    (161932, 24950),
    (215682, 24950),
    (274433, 24950),
]
# Full step durations, in ms (before capacitance filtering)
pr2_durations = [3, 10, 30, 100, 300, 1000]

pr2_steps_variant = [
    (5615, 9950),
    (41943, 9950),
    (78271, 9950),
    (114599, 9950),
    (150927, 9950),
    (187255, 9950),
    (223583, 9950),
    (259911, 9950),
    (296239, 9950),
]
pr2_durations_variant = [20, 80, 140, 200, 260, 320, 380, 440, 500]

pr2_steps_nocap = [
    (5843, 25000),
    (57913, 25000),
    (110113, 25000),
    (162813, 25000),
    (216813, 25000),
    (275813, 25000),
]

pr3_steps = [
    (56141, 9950),
    (138441, 9950),
    (220750, 9950),
    (303030, 9950),
    (385310, 9950),
    (467590, 9950),
    (549871, 9950),
]
pr3_voltages = np.array([-60, -40, -20, 0, 20, 40, 60])

pr3_steps_nocap = [
    (56291, 10000),
    (138871, 10000),
    (221451, 10000),
    (304031, 10000),
    (386611, 10000),
    (469191, 10000),
    (551771, 10000),
]

pr4_steps = [
    (11854, 1450),
    (40560, 1450),
    (69216, 1450),
    (97872, 1450),
    (126527, 1450),
    (155184, 1450),
    (183840, 1450),
    (212495, 1450),
    (241152, 1450),
    (269808, 1450),
    (298464, 1450),
    (327120, 1450),
    (355775, 1450),
    (384431, 1450),
    (413088, 1450),
    (441744, 1450),
]
pr4_voltages = [-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20,
                30, 40, 50]

pr4_steps_nocap = [
    (12054, 1500),
    (41060, 1500),
    (70066, 1500),
    (99072, 1500),
    (128078, 1500),
    (157084, 1500),
    (186090, 1500),
    (215096, 1500),
    (244102, 1500),
    (273108, 1500),
    (302114, 1500),
    (331120, 1500),
    (360126, 1500),
    (389132, 1500),
    (418138, 1500),
    (447144, 1500),
]

pr5_steps = [  # Variable step
    (26463, 59950),
    (129437, 59950),
    (232360, 59950),
    (335285, 59950),   # Very close to Erev
    (438209, 59950),
    (541133, 59950),
    (644056, 59950),
    (746981, 59950),
    (849905, 59950),
]
pr5_voltages = [-120, -110, -100, -90, -80, -70, -60, -50, -40]

pr5_steps_nocap = [
    (26613, 60000),
    (129837, 60000),
    (233061, 60000),
    (336285, 60000),   # Very close to Erev
    (439509, 60000),
    (542733, 60000),
    (645957, 60000),
    (749181, 60000),
    (852405, 60000),
]


def split_points(protocol, variant=False):
    """
    Returns the indices at which to split a traditional protocol signal to
    obtain overlayed traces.
    """
    # Points to split signal at
    splits = {
        1: [
            # Numbers 2, 3, and 4 are a bit off for some reason
            0, 51770, 103519, 155269, 207019, 258770, 310520,
        ],
        2: [
            0, 51770, 103519, 155269, 207019, 258770, 310520,
        ],
        3: [
            0, 82280, 164609, 246889, 329169, 411449, 493729, 576010,
        ],
        4: [
            0, 28657, 57363, 86019, 114674, 143331, 171987, 200642, 229299,
            257955, 286611, 315267, 343922, 372578, 401235, 429891, 458546,
        ],
        5: [
            0, 102974, 205897, 308822, 411746, 514670, 617593, 720518, 823442,
            926366,
        ],
    }
    splits_variants = {
        1: [
            615, 36343, 72071, 107799, 143527, 179255, 214983, 250711, 286439
        ],
        2: [
            615, 36343, 72071, 107799, 143527, 179255, 214983, 250711, 286439
        ],
    }

    # Find split points
    if variant:
        split = splits_variants[protocol]
    else:
        split = splits[protocol]
    return list(zip(split[:-1], split[1:]))


def split_points_nocap(protocol, variant=False):
    """
    Returns the indices at which to split a traditional protocol signal to
    obtain overlayed traces; for signals without capacitance removal.
    """
    # Points to split signal at
    splits = {
        1: np.arange(7) * 52000,
        2: np.arange(7) * 52000,
        3: np.arange(8) * 82580,
        4: np.arange(17) * 29006,
        5: np.arange(10) * 103224,
    }
    splits_variants = {
        1: [
        ],
        2: [
        ],
    }

    # Find split points
    if variant:
        raise NotImplementedError
        split = splits_variants[protocol]
    else:
        split = splits[protocol]
    return list(zip(split[:-1], split[1:]))


def fit_conductance_to_iv_curve(cell, parameters):
    """
    Simulates an IV curve with 8 parameters, and then finds the best fit w.r.t.
    a given cell.
    """
    assert(len(parameters) == 8)

    # Load cell's IV data
    iv1 = iv_curve(cell)[1]

    # Load protocol
    print('Loading protocol file')
    protocol = data.load_myokit_protocol(5)

    # Load model
    model = data.load_myokit_model()

    # Set reversal potential
    model.get('nernst.EK').set_rhs(
        cells.reversal_potential(cells.temperature(cell)))

    # Set 8 parameters
    for i, p in enumerate(parameters):
        model.get(parameter_names[i]).set_rhs(p)

    # Start at steady-state for -80mV
    model.get('membrane.V').promote()
    ai = model.get('ikr.act.inf').pyfunc()(-80)
    ri = model.get('ikr.rec.inf').pyfunc()(-80)
    model.get('membrane.V').demote()
    model.get('ikr.act').set_state_value(ai)
    model.get('ikr.rec').set_state_value(ri)

    # Create simulation
    simulation = myokit.Simulation(model, protocol)

    # Run simulation
    dt = 0.1
    d = simulation.run(
        protocol.characteristic_time(),
        log_interval=dt,
        log=['engine.time', 'ikr.IKr'],
        ).npview()

    # Capacitance filter
    t, c = d['engine.time'], d['ikr.IKr']
    del(d)
    t, c = data.capacitance(protocol, dt, t, c)
    d = myokit.DataLog()
    d['time'] = t
    d['current'] = c

    # Calculate iv from simulation
    vs, iv2 = iv_curve(cell, pr5_log=d)

    # Calculate best scaling
    from scipy.optimize import fmin

    def f(g):
        return np.sum((iv1 - iv2 * g[0])**2)

    # Guess some exponential parameters and fit
    best = float(fmin(f, 1, disp=False)[0])
    g = float(model.get(parameter_names[-1]).rhs()) * best
    return g


def time_constant_of_activation_pr1(cell, pr1_log=None):
    """
    Calculates the time constant of activation for a given cell's Pr1 data.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr1_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, time_constants)`` where ``voltages`` and
    ``time_constants`` are lists of equal lengths.
    """
    # Load data, or use cached
    pr1_log = data.load(cell, 1, pr1_log)
    current = pr1_log['current']

    # Set steps starts and durations
    if cell != 7 and cell != 8:
        steps = pr2_steps
        durations = pr2_durations
    else:
        steps = pr2_steps_variant
        durations = pr2_durations_variant

    # Isolate summary statistics, show in figure which points are used
    summary = []
    for i, j in steps:
        imin = i + np.argmin(current[i:i + 2000])
        x1 = max(i, imin - 10)
        x2 = x1 + 20
        summary.append(np.mean(current[x1:x2]))
    summary = np.array(summary)
    summary /= np.min(summary)

    # Fit time constant with single exponential
    from scipy.optimize import curve_fit

    def f(t, a, b, c):
        return a + b * np.exp(-t / c)

    # Guess some exponential parameters and fit
    popt, pcov = curve_fit(f, durations, summary, [1, -1, 100])
    tau = popt[-1]

    # Return
    return [0], [tau]


def time_constant_of_activation_pr2(cell, pr2_log=None):
    """
    Calculates the time constant of activation for a given cell's Pr2 data.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr2_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, time_constants)`` where ``voltages`` and
    ``time_constants`` are lists of equal lengths.
    """
    # Load data, or use cached
    pr2_log = data.load(cell, 2, pr2_log)
    time = pr2_log.time()
    current = pr2_log['current']

    # Set steps starts and durations
    if cell != 7 and cell != 8:
        steps = pr2_steps
        durations = pr2_durations
    else:
        steps = pr2_steps_variant
        durations = pr2_durations_variant

    debug = False
    if debug:
        import matplotlib.pyplot as plt
        plt.figure()

    # Isolate summary statistics, show in figure which points are used
    summary = []
    for i, j in steps:
        j += i
        imin = i + np.argmin(current[i:j])
        x1 = max(i, imin - 10)
        x2 = x1 + 20
        summary.append(np.mean(current[x1:x2]))

        if debug:
            plt.plot(time[i: j] - time[i], current[i: j])

    summary = np.array(summary)
    summary /= np.min(summary)

    # Fit time constant with single exponential
    from scipy.optimize import curve_fit

    def f(t, a, b, c):
        return a + b * np.exp(-t / c)

    if debug:
        # Show the data
        plt.figure()
        plt.plot(durations, summary, 's')
        plt.show()

    # Guess some exponential parameters and fit
    popt, pcov = curve_fit(f, durations, summary, [1, -1, 100])
    tau = popt[-1]

    # Return
    return [40], [tau]


def time_constants_pr5(cell, pr5_log=None):
    """
    Returns time constants of activation and inactivation, calculated from Pr5.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr5_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, tau_act, tau_inact)`` where ``voltages``,
    ``tau_act``, and ``tau_rec`` are lists of equal lengths.
    """
    # Debug mode
    debug = False
    if debug:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 8))

    # Load data, or use cached
    pr5_log = data.load(cell, 5, pr5_log)
    time = pr5_log['time']
    current = pr5_log['current']

    # Remove step near Erev: As the signal is too flat in some cells to get a
    # good estimate.
    steps = pr5_steps[:3] + pr5_steps[4:]
    voltages = pr5_voltages[:3] + pr5_voltages[4:]
    voltages = np.array(voltages)

    # Single exponential
    def single(t, a, b, c):
        if c < 1:
            return np.ones(len(t)) * float('inf')
        return a + b * np.exp(-t / c)

    # Double exponental
    def f(t, a, b1, c1, b2, c2):
        if c1 < 1 or c2 < c1:
            return np.ones(len(t)) * float('inf')
        if b1 * b2 > 0:
            return np.ones(len(t)) * float('inf')
        return a + b1 * np.exp(-t / c1) + b2 * np.exp(-t / c2)

    # Curve fitting
    from scipy.optimize import curve_fit

    # Determine time constants
    tau_rec = []
    tau_act = []
    for k, step in enumerate(steps):
        i, j = step

        # Fit exponential
        t = time[i:i + j] - time[i - 1]
        c = current[i:i + j]

        # Guess some exponential parameters
        offset = 0
        if cell == 9 and k == len(steps) - 1:
            # Weird artefact in final trace for cell 9
            offset = 100
        peak = offset + np.argmax(np.abs(c[offset:]))

        # Deactivation pre-fit, for guess
        guess = 200 if voltages[k] < -60 else 2000
        a2, b2, c2 = 0, c[peak], guess
        popt, pcov = curve_fit(single, t[peak:], c[peak:], [a2, b2, c2])
        a2, b2, c2 = popt

        # Recovery pre-fit, for guess
        guess = 5
        a1, b1, c1 = c[peak], -c[peak], guess
        if peak < 3:
            # Very fast: Only happens for simulations
            if debug:
                print('Too fast!')
            peak = 3
            a1, b1, c1 = -3, 3, 0.1
        try:
            popt, pcov = curve_fit(single, t[:peak], c[:peak], [a1, b1, c1])
            a1, b1, c1 = popt
        except RuntimeError:
            pass

        # Double exponential
        try:
            popt, pcov = curve_fit(f, t, c, [a1, b1, c1, b2, c2])
            print(popt)
        except RuntimeError:
            popt, pcov = curve_fit(f, t, c, [a1, -1, 10, 0.5, c2])

        tau_rec.append(popt[2])
        tau_act.append(popt[4])
        if debug:
            print('Tau act: ' + str(tau_act[-1]) + ' ms')
            print('Tau rec: ' + str(tau_rec[-1]) + ' ms')
        if debug:
            plt.plot(t, c, alpha=0.7)
            plt.plot(t, f(t, *popt), 'k:', lw=1)

    if debug:
        plt.show()
        import sys
        sys.exit(1)

    return voltages, tau_act, tau_rec


def time_constant_of_activation_pr5(cell, pr5_log=None):
    """
    Returns time constants of activation, calculated from Pr5.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr5_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, time_constants)`` where ``voltages`` and
    ``time_constants`` are lists of equal lengths.
    """
    v, tau_act, tau_rec = time_constants_pr5(cell, pr5_log)
    return v, tau_act


def time_constant_of_inactivation_pr5(cell, pr5_log=None):
    """
    Returns time constants of inactivation, calculated from Pr5.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr5_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, time_constants)`` where ``voltages`` and
    ``time_constants`` are lists of equal lengths.
    """
    v, tau_act, tau_rec = time_constants_pr5(cell, pr5_log=pr5_log)
    return v, tau_rec


def time_constant_of_inactivation_pr4(cell, pr4_log=None):
    """
    Returns time constants of inactivation, calculated from Pr4.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr4_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, time_constants)`` where ``voltages`` and
    ``time_constants`` are lists of equal lengths.
    """
    # Load data, or use cached
    pr4_log = data.load(cell, 4, pr4_log)
    time = pr4_log['time']
    current = pr4_log['current']

    steps = pr4_steps
    voltages = pr4_voltages

    debug = False
    if debug:
        import matplotlib.pyplot as plt
        plt.figure()

    # Curve fitting, single exponential
    from scipy.optimize import curve_fit

    def f(t, a, b, c):
        if c <= 0:
            return np.ones(t.shape) * float('inf')
        return a + b * np.exp(-t / c)

    taus = []
    for k, step in enumerate(steps):
        i, j = step

        t = time[i:i + j] - time[i]
        c = current[i:i + j]

        # Guess some parameters and fit
        p0 = current[i + j - 1], current[i] - current[i + j - 1], 10
        popt, pcov = curve_fit(f, t, c, p0)
        taus.append(popt[2])

        if debug:
            print(voltages[k], popt[2])
            plt.plot(t, c)
            plt.plot(t, f(t, *popt), 'k:')

    if debug:
        plt.show()

    return voltages, taus


def steady_state_activation_pr3(cell, pr3_log=None):
    """
    Returns the steady state of activation, calculated from Pr3.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr3_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, activation)`` where ``voltages`` and
    ``activation`` are lists of equal lengths.
    """
    # Load data, or use cached
    pr3_log = data.load(cell, 3, pr3_log)
    current = pr3_log['current']

    steps = pr3_steps
    voltages = pr3_voltages

    # Find peaks
    cpeaks = []
    for i, j in steps:
        c = current[i:i + j]
        z = np.argmax(c)
        zlo = max(z - 5, 0)
        zhi = zlo + 10
        cpeaks.append(np.mean(c[zlo:zhi]))

    # Normalise
    # Note: Division by (V - E) not needed; all measured at same voltage!
    cpeaks = np.array(cpeaks)
    cpeaks /= np.max(cpeaks[-3:])

    return voltages, cpeaks


def steady_state_inactivation_and_iv_curve_pr5(
        cell, pr5_log=None, include_minus_90=False, estimate_erev=False):
    """
    Returns the steady state of inactivation and an iv-curve, calculated from
    Pr5.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr5_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(v1, inactivation, v2, iv_curve)`` where ``v1`` and
    ``inactivation`` are of equal length, and ``v2`` and ``iv_curve`` are of
    equal length.
    """
    # Load data, or use cached
    pr5_log = data.load(cell, 5, pr5_log)
    current = pr5_log['current']

    steps = pr5_steps
    voltages = np.array(pr5_voltages)

    # Find peaks
    peaks = []
    for k, step in enumerate(steps):
        i, j = step
        if cell == 9 and k == len(steps) - 1:
            # Weird artefact in final trace for cell 9
            i += 100
            j -= 100
        c = current[i:i + j]
        peaks.append(current[i + np.argmax(np.abs(c))])
    peaks = np.array(peaks)

    if estimate_erev:
        # Estimate reversal potential from IV curve
        irev = np.argmax(peaks >= 0)
        x1, x2 = voltages[irev - 1], voltages[irev]
        y1, y2 = peaks[irev - 1], peaks[irev]
        erev = x1 - y1 * (x2 - x1) / (y2 - y1)
    else:
        # Calculate reversal potential
        erev = cells.reversal_potential(cells.temperature(cell))

    # Calculate steady state
    v1 = voltages
    g = peaks / (voltages - erev)
    if not include_minus_90:
        # Remove point at -90, too close to Erev!
        v1 = np.concatenate((voltages[:3], voltages[4:]))
        g = np.concatenate((g[:3], g[4:]))
    g /= np.max(g[:3])

    # Return
    return v1, g, voltages, peaks


def steady_state_inactivation_pr5(
        cell, pr5_log=None, include_minus_90=False, estimate_erev=False):
    """
    Returns the steady state of inactivation, calculated from Pr5.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr5_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, inactivation)`` where ``voltages`` and
    ``inactivation`` are lists of equal lengths.
    """
    v1, s, v2, i = steady_state_inactivation_and_iv_curve_pr5(
        cell, pr5_log, include_minus_90, estimate_erev)
    return v1, s


def iv_curve_pr5(cell, pr5_log=None):
    """
    Returns an IV curve, calculated from Pr5.

    Arguments:

    ``cell``
        Which cell data to use (integer).
    ``pr5_log``
        An optional datalog with the data for the given cell.

    Returns a tuple ``(voltages, peak_currents)`` where ``voltages`` and
    ``peak_currents`` are lists of equal lengths.
    """
    v1, s, v2, i = steady_state_inactivation_and_iv_curve_pr5(cell, pr5_log)
    return v2, i


def time_constant_of_activation(cell, pr2_log=None, pr5_log=None):
    """
    Returns time constants of activation based on Pr2 and Pr5.
    """
    v1, t1 = time_constant_of_activation_pr2(cell, pr2_log=pr2_log)
    v2, t2 = time_constant_of_activation_pr5(cell, pr5_log=pr5_log)
    v = np.concatenate((v1, v2))
    t = np.concatenate((t1, t2))
    i = np.argsort(v)
    return v[i], t[i]


def time_constant_of_inactivation(cell, pr4_log=None, pr5_log=None):
    """
    Returns time constants of inactivation based on Pr4 and Pr5.

    Makes a hardcoded data selection!
    """
    v1, t1 = time_constant_of_inactivation_pr5(cell, pr5_log=pr5_log)
    v2, t2 = time_constant_of_inactivation_pr4(cell, pr4_log=pr4_log)
    return np.concatenate((v1, v2[7:])), np.concatenate((t1, t2[7:]))


def steady_state_activation(cell, pr3_log=None):
    """
    Returns steady-state activation values based on Pr3.
    """
    return steady_state_activation_pr3(cell, pr3_log=pr3_log)


def steady_state_inactivation(cell, pr5_log=None):
    """
    Returns steady-state activation values based on Pr5.

    Makes a hardcoded data selection!
    """
    v, t = steady_state_inactivation_pr5(cell, pr5_log=pr5_log)
    return v, t


def iv_curve(cell, pr5_log=None):
    """
    Returns an IV curve based on Pr5.
    """
    return iv_curve_pr5(cell, pr5_log)


def all_summary_statistics(
        cell, pr2_log=None, pr3_log=None, pr4_log=None, pr5_log=None):
    """
    Returns all 5 summary statistics.

    Makes a hardcoded data selection!

    Returns a tuple::

        ((vta, ta), (vtr, tr), (vai, ai), (vri, ri), (viv, iv))

    with the time constant of activation, the time constant of recovery, the
    steady-state activation, the steady-state recovery, and the iv curve.
    Each is given as a tuple ``(voltage, values)``.
    """
    # Load all data
    pr2_log = data.load(cell, 2, pr2_log)
    pr3_log = data.load(cell, 3, pr3_log)
    pr4_log = data.load(cell, 4, pr4_log)
    pr5_log = data.load(cell, 5, pr5_log)

    # Pr1: Skip

    # Pr2: Get time_constant of activation
    vta2, ta2 = time_constant_of_activation_pr2(cell, pr2_log=pr2_log)

    # Pr3: Steady-state of activation
    vai, ai = steady_state_activation_pr3(cell, pr3_log=pr3_log)

    # Pr4: Time constant of recovery
    vtr2, tr2 = time_constant_of_inactivation_pr4(cell, pr4_log=pr4_log)

    # Pr5: Time constant of activation and recovery
    v, ta1, tr1 = time_constants_pr5(cell, pr5_log=pr5_log)
    vta1 = vtr1 = v

    # Pr5: Steady-state of recovery and IV curve
    vri, ri, viv, iv = steady_state_inactivation_and_iv_curve_pr5(
        cell, pr5_log=pr5_log, include_minus_90=False)

    # Concatenate time constant of activation data
    vta = np.concatenate((vta1, vta2))
    ta = np.concatenate((ta1, ta2))

    # Concatenate time constant of recovery data
    vtr = np.concatenate((vtr1, vtr2[7:]))
    tr = np.concatenate((tr1, tr2[7:]))

    # Return
    return ((vta, ta), (vtr, tr), (vai, ai), (vri, ri), (viv, iv))


def model_steady_state_activation(voltages, parameters):
    """
    Calculates and returns the model variable steady-state activation (not the
    summary statistic!) for the given voltages and parameters.
    """
    p1, p2, p3, p4 = parameters[:4]
    k1 = p1 * np.exp(p2 * voltages)
    k2 = p3 * np.exp(-p4 * voltages)
    return k1 / (k1 + k2)


def model_steady_state_inactivation(voltages, parameters, shift=0, skew=1):
    """
    Calculates and returns the model variable steady-state inactivation (not
    the summary statistic!) for the given voltages and parameters.

    To mess around, you can voltage-shift the curve, or skew it.
    """
    p5, p6, p7, p8 = parameters[4:8]
    # k3 = p5 * np.exp(p6 * voltages)
    # k4 = p7 * np.exp(-p8 * voltages)

    sr = -(p6 + p8) / skew
    hr = np.log(p7 / p5) / (p6 + p8) + shift

    return 1 / (1 + np.exp(sr * (hr - voltages)))


def model_time_constant_of_activation(voltages, parameters):
    """
    Calculates and returns the model variable time constant of activation (not
    the summary statistic!) for the given voltages and parameters.
    """
    p1, p2, p3, p4 = parameters[:4]
    k1 = p1 * np.exp(p2 * voltages)
    k2 = p3 * np.exp(-p4 * voltages)
    return 1 / (k1 + k2)


def model_time_constant_of_inactivation(voltages, parameters):
    """
    Calculates and returns the model variable time constant of inactivation
    (not the summary statistic!) for the given voltages and parameters.
    """
    p5, p6, p7, p8 = parameters[4:8]
    k3 = p5 * np.exp(p6 * voltages)
    k4 = p7 * np.exp(-p8 * voltages)
    return 1 / (k3 + k4)


def direct_fit_linear(ta, tr, ai, ri, iv):
    """
    Performs a direct fit to the given summary statistics, and return the
    obtained kinetic parameters (p1, p2, ..., p8).

    Performs the time-constant fitting part in linear - untransformed - space.
    """
    # Curve fitting
    from scipy.optimize import curve_fit

    def boltzmann(v, h, s):
        return 1 / (1 + np.exp(s * (h - v)))

    def rate_pos(v, a, b):
        return np.exp(a + b * v)

    def rate_neg(v, a, b):
        return np.exp(a - b * v)

    # Fit to ss act
    popt, pcov = curve_fit(boltzmann, ai[0], ai[1], [-20, 0.03])
    ha, sa = popt
    print('Midpoint & slope of activation')
    print(ha, sa)

    # Fit to ss rec
    popt, pcov = curve_fit(boltzmann, ri[0], ri[1], [-60, -0.03])
    hr, sr = popt
    print('Midpoint & slope of inactivation')
    print(hr, sr)

    # Fit to ss act / tau act
    x = ta[0]
    y = boltzmann(x, ha, sa) / ta[1]
    popt, pcov = curve_fit(rate_pos, x, y, [-8, 0.075])
    a1, b1 = popt

    # Fit to ss act / tau act
    x = tr[0]
    y = boltzmann(x, hr, sr) / tr[1]
    popt, pcov = curve_fit(rate_neg, x, y, [-5.0, 0.03])
    a4, b4 = popt

    # Activation parameters
    p1 = np.exp(a1)
    p2 = b1
    p3 = np.exp(sa * ha + a1)
    p4 = sa - b1
    p5 = np.exp(sr * hr + a4)
    p6 = -sr - b4
    p7 = np.exp(a4)
    p8 = b4

    # Full kinetic parameters
    return [p1, p2, p3, p4, p5, p6, p7, p8]


def direct_fit_logarithmic(ta, tr, ai, ri, iv):
    """
    Performs a direct fit to the given summary statistics, and return the
    obtained kinetic parameters (p1, p2, ..., p8).

    Performs the time-constant fitting part in semilog space, which means we
    don't ignore the points where the steady-state is almost zero.
    """
    # Curve fitting
    from scipy.optimize import curve_fit

    def boltzmann(v, h, s):
        return 1 / (1 + np.exp(s * (h - v)))

    def rate_pos(v, a, b):
        return a + b * v

    def rate_neg(v, a, b):
        return a - b * v

    # Fit to ss act
    popt, pcov = curve_fit(boltzmann, ai[0], ai[1], [-20, 0.03])
    ha, sa = popt
    print('Midpoint & slope of activation')
    print(ha, sa)

    # Fit to ss rec
    popt, pcov = curve_fit(boltzmann, ri[0], ri[1], [-60, -0.03])
    hr, sr = popt
    print('Midpoint & slope of inactivation')
    print(hr, sr)

    # Fit to ss act / tau act
    x = ta[0]
    y = np.log(boltzmann(x, ha, sa) / ta[1])
    popt, pcov = curve_fit(rate_pos, x, y, [-8, 0.075])
    a1, b1 = popt

    # Fit to ss act / tau act
    x = tr[0]
    y = np.log(boltzmann(x, hr, sr) / tr[1])
    popt, pcov = curve_fit(rate_neg, x, y, [-5.0, 0.03])
    a4, b4 = popt

    # Activation parameters
    p1 = np.exp(a1)
    p2 = b1
    p3 = np.exp(sa * ha + a1)
    p4 = sa - b1
    p5 = np.exp(sr * hr + a4)
    p6 = -sr - b4
    p7 = np.exp(a4)
    p8 = b4

    # Full kinetic parameters
    return [p1, p2, p3, p4, p5, p6, p7, p8]


def simulate_pr2345(cell, parameters):
    """
    Simulates Pr2-5 and returns a tuple ``pr2_log, pr3_log, pr4_log, pr5_log``.

    For cells 7 and 8 the variant pr2 is simulated.
    """
    import myokit.lib.hh
    assert(len(parameters) == 9)

    # Load model
    model = data.load_myokit_model()
    model.get('membrane.V').set_label('membrane_potential')
    model.get('nernst.EK').set_rhs(
        cells.reversal_potential(cells.temperature(cell)))

    # Set model parameters
    for i, p in enumerate(parameters):
        model.get(parameter_names[i]).set_rhs(p)

    # Start at steady-state for -80mV
    model.get('membrane.V').promote()
    ai = model.get('ikr.act.inf').pyfunc()(-80)
    ri = model.get('ikr.rec.inf').pyfunc()(-80)
    model.get('membrane.V').demote()
    model.get('ikr.act').set_state_value(ai)
    model.get('ikr.rec').set_state_value(ri)

    # Create analytical model
    m = myokit.lib.hh.HHModel.from_component(
        model.get('ikr'), parameters=parameter_names)
    del(model)

    # Run all simulations
    logs = []
    for i in range(4):
        pr = i + 2

        print('Simulating Pr' + str(pr))

        # Load protocol
        variant = (pr == 2 and cell in (7, 8))
        p = data.load_myokit_protocol(pr, variant=variant)

        # Create analytical simulation
        s = myokit.lib.hh.AnalyticalSimulation(m, p)

        # Create times array (with cap filtering, just like real data)
        t = np.arange(0, p.characteristic_time(), 0.1)
        t = data.capacitance(p, 0.1, t)[0]

        # Run simulation
        d = s.run(t[-1] + 0.1, log_times=t).npview()

        # Store in same format as experimental data
        e = myokit.DataLog()
        e.set_time_key('time')
        e['time'] = d['engine.time']
        e['current'] = d['ikr.IKr']
        logs.append(e)

    return logs


def simulate_all_summary_statistics(cell, parameters):
    """
    Simulates and returns all summary statistics.
    """
    # Simulate traditional protocols
    logs = simulate_pr2345(cell, parameters)

    # Calculate summary statistics
    print('Calculating simulated summary statistics')
    return all_summary_statistics(cell, *logs)


def save_all_summary_statistics(basename, ta, tr, ai, ri, iv):
    """
    Saves summary statistics to files.
    Arguments ``ta`` etc. must be tuples (v, stats).
    """
    d = myokit.DataLog()
    d['v'] = ta[0]
    d['ta'] = ta[1]
    d.save_csv(basename + '-ta.csv')

    d = myokit.DataLog()
    d['v'] = tr[0]
    d['tr'] = tr[1]
    d.save_csv(basename + '-tr.csv')

    d = myokit.DataLog()
    d['v'] = ai[0]
    d['ai'] = ai[1]
    d.save_csv(basename + '-ai.csv')

    d = myokit.DataLog()
    d['v'] = ri[0]
    d['ri'] = ri[1]
    d.save_csv(basename + '-ri.csv')

    d = myokit.DataLog()
    d['v'] = iv[0]
    d['iv'] = iv[1]
    d.save_csv(basename + '-iv.csv')


def load_all_summary_statistics(basename):
    """
    Loads files saved by :meth:`save_all_summary_statistics()`.
    """
    d = myokit.DataLog.load_csv(basename + '-ta.csv').npview()
    ta = [d['v'], d['ta']]

    d = myokit.DataLog.load_csv(basename + '-tr.csv').npview()
    tr = [d['v'], d['tr']]

    d = myokit.DataLog.load_csv(basename + '-ai.csv').npview()
    ai = [d['v'], d['ai']]

    d = myokit.DataLog.load_csv(basename + '-ri.csv').npview()
    ri = [d['v'], d['ri']]

    d = myokit.DataLog.load_csv(basename + '-iv.csv').npview()
    iv = [d['v'], d['iv']]

    return ta, tr, ai, ri, iv
