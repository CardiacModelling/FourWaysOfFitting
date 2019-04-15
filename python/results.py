#!/usr/bin/env python3
#
# Python module that knows where all the results are, and how to load them.
#
from __future__ import division, print_function
import glob
import inspect
import numpy as np
import os
import re


# Get root of this project
try:
    frame = inspect.currentframe()
    ROOT = os.path.dirname(inspect.getfile(frame))
finally:
    del(frame) # Must be manually deleted
ROOT = os.path.abspath(os.path.join(ROOT, '..'))


# Natural sort
_nat_sort = re.compile('([0-9]+)')
def natural_sort(s):
    return [int(t) if t.isdigit() else t.lower() for t in _nat_sort.split(s)]


def load_parameters(cell, fit, repeats=False, variant=False):
    """
    Returns the parameters obtained from a particular ``fit`` to data from the
    given ``cell``.

    If ``repeats=True``, all obtained parameter sets will be returned.
    """
    cell, fit = int(cell), int(fit)
    assert 1 <= cell <= 9
    assert 1 <= fit <= 5
    if fit == 5:
        d = os.path.join(ROOT, 'surface-ap-fit')
        sfit = 'ap'
    else:
        d = os.path.join(ROOT, 'method-' + str(fit))
        sfit = str(fit)

        if variant:
            if fit not in (1, 2, 3):
                raise NotImplementedError(
                    'No variant known for method ' + str(fit))
            d += 'b'
            sfit += 'b'

    # Handle default case
    if not repeats:
        f = os.path.join(d, 'cell-' + str(cell) + '-fit-' + sfit + '.txt')
        if not os.path.exists(f):
            raise ValueError(
                'No data for fit ' + sfit + ' cell ' + str(cell) + ' yet.')
        with open(f, 'r') as f:
            p = np.array([float(x) for x in f.readlines()])
            assert len(p) == 9
        return p

    # Collect all parameters
    f = 'cell-' + str(cell) + '-fit-' + sfit + '-parameters-*.txt'
    fs = glob.glob(os.path.join(d, f))
    fs.sort(key=natural_sort)
    ps = []
    for f in fs:
        with open(f, 'r') as f:
            ps.append([float(x) for x in f.readlines()])
            assert len(ps[-1]) == 9
    return np.array(ps)


def load_kylie_parameters(cell):
    """
    Returns the parameters Kylie obtained for the given ``cell``.
    """
    if cell == 5:
        return [
            2.26026076650526e-004,
            6.99168845608636e-002,
            3.44809941106440e-005,
            5.46144197845311e-002,
            8.73240559379590e-002,
            8.91302005497140e-003,
            5.15112582976275e-003,
            3.15833911359110e-002,
            1.52395993652348e-001,
        ]

    raise NotImplementedError('Only cell 5')


def load_errors(cell, fit):
    """
    Returns the (sorted) errors for all repeats for the given cell/fit
    combination.
    """
    cell, fit = int(cell), int(fit)
    assert 1 <= cell <= 9
    assert 2 <= fit <= 4

    f = os.path.join(
        ROOT,
        'method-' + str(fit),
        'cell-' + str(cell) + '-fit-' + str(fit) + '-errors.txt'
    )
    with open(f, 'r') as f:
        return np.array([float(x) for x in f.readlines()])


def load_times(cell, fit):
    """
    Returns the (sorted) times for all repeats for the given cell/fit
    combination.
    """
    cell, fit = int(cell), int(fit)
    assert 1 <= cell <= 9
    assert 2 <= fit <= 4

    f = os.path.join(
        ROOT,
        'method-' + str(fit),
        'cell-' + str(cell) + '-fit-' + str(fit) + '-times.txt'
    )
    with open(f, 'r') as f:
        return np.array([float(x) for x in f.readlines()])


def load_evaluations(cell, fit):
    """
    Returns the (unsorted) evaluations for all repeats for the given cell/fit
    combination.
    """
    cell, fit = int(cell), int(fit)
    assert 1 <= cell <= 9
    assert 2 <= fit <= 4

    # Collect evaluations from all logs
    fs = glob.glob(os.path.join(
        ROOT,
        'method-' + str(fit),
        'cell-' + str(cell) + '-fit-' + str(fit) + '-log-*.csv'
    ))
    fs.sort(key=natural_sort)

    evals = []
    for f in fs:

        # Extract number of evaluations
        with open(f, 'r') as f:
            evals.append(float(f.readlines()[-1].strip().split(',')[1]))

    return evals
