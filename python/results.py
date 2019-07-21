#!/usr/bin/env python3
#
# Python module that knows where all the results are, and how to load them.
#
import glob
import fnmatch
import inspect
import numpy as np
import os
import pints
import re

# Load project modules
import transformations


# Get root of this project
try:
    frame = inspect.currentframe()
    ROOT = os.path.dirname(inspect.getfile(frame))
finally:
    del(frame)  # Must be manually deleted
ROOT = os.path.abspath(os.path.join(ROOT, '..'))


def natural_sort(s):
    """
    Key function for natural sorting.
    """
    pat = re.compile('([0-9]+)')
    return [int(t) if t.isdigit() else t.lower() for t in pat.split(s)]


def _root_name(cell, method,
               search_transformation='a', sample_transformation='a',
               start_from_m1=False, method_1b=False):
    """
    Returns a dirname and base filename for the given info: To create a full
    filename, add a repeat number and a file extension.
    """
    cell = int(cell)
    method = int(method)
    if cell < 1 or cell > 10:
        raise ValueError('Unknown cell: ' + str(cell))
    if method < 1 or method > 5:
        raise ValueError('Unknown method: ' + str(method))

    # Transformation codes must exist
    if search_transformation not in transformations.codes:
        raise ValueError(
            'Unknown transformation code: ' + str(search_transformation))
    if sample_transformation not in transformations.codes:
        raise ValueError(
            'Unknown transformation code: ' + str(search_transformation))

    # Method 1 cannot use transformations
    if method == 1 and not method_1b:
        if search_transformation != 'a' or sample_transformation != 'a':
            raise ValueError(
                'Method 1 results cannot be requested for specific parameter'
                ' transformations.')

    # Method 1 cannot use start_from_m1
    if method == 1 and start_from_m1:
            raise ValueError('Start-from-m1 cannot be used with method 1.')

    # Method 1b cannot be used with methods other than method 1
    if method != 1 and method_1b:
        raise ValueError('Method-1b can only be used with method 1.')

    # Get directory name
    dirname = 'method-' + str(method) if method < 5 else 'surface-ap-fit'
    if start_from_m1 or method_1b:
        dirname += 'b'
    if search_transformation != 'a' or sample_transformation != 'a':
        dirname += '-' + search_transformation + sample_transformation
    dirname = os.path.join(ROOT, dirname)

    # Get root of file name
    root = 'cell-' + str(cell) + '-fit-' + str(method)
    if start_from_m1 or method_1b:
        root += 'b'
    # TODO Add transformation name too?
    if method_1b or method > 1:
        root += '-run-'

    return (dirname, root)


class reserve_base_name(object):
    """
    Context manager that reserves and returns a base filename (i.e. without an
    extension) for the next repeat of the fit indicated by the parameters.

    If an exception occurs within the manager's context, any files matching the
    patterns ``basename.*`` and ``basename-*`` are deleted.
    """
    def __init__(self, cell, method, search_transformation='a',
                 sample_transformation='a', start_from_m1=False,
                 method_1b=False):

        # Method 1 is only supported for method 1b
        if method == 1 and not method_1b:
            raise ValueError('Only method 1b is supported, not method 1.')

        # Get directory and root of filename (without indice)
        dirname, root = _root_name(
            cell, method, search_transformation, sample_transformation,
            start_from_m1, method_1b)
        self._dirname = dirname
        self._root = root

        # Indice, as integer
        self._indice = None

        # Filename including indice and padding
        self._base = None

        # Indice formatting
        self._format = '{:03d}'

    def __enter__(self):

        # Find potential indice
        fs = glob.glob(os.path.join(self._dirname, self._root + '*'))
        if fs:
            fs = [os.path.splitext(f)[0] for f in fs]
            fs = [int(f.rsplit('-', 1)[1]) for f in fs]
            indice = max(fs)
        else:
            indice = 0

        # Reserve
        running = True
        while running:
            indice += 1
            filename = self._root + self._format.format(indice) + '.txt'
            path = os.path.join(self._dirname, filename)
            f = None
            try:
                f = open(path, 'x')     # Note: Python 3.3 only
                f.write('Reserved\n')
                running = False
            except FileExistsError:
                # File already exists, try next indice
                pass
            finally:
                if f is not None:
                    f.close()

        # Store
        self._indice = indice
        self._base = self._root + self._format.format(indice)

        # Return path (dirname and base filename)
        return os.path.join(self._dirname, self._base)

    def __exit__(self, exc_type, exc_val, exc_tb):

        # No exception? Then exit
        if exc_type is None:
            return

        # Delete files matching patterns
        patterns = [
            self._base + '.*',
            self._base + '-*',
        ]
        for filename in os.listdir(self._dirname):
            for pattern in patterns:
                if fnmatch.fnmatch(filename, pattern):
                    path = os.path.join(self._dirname, filename)
                    print('Removing unfinished result file: ' + path)
                    os.remove(path)

        # Don't suppress the exception
        return False


def save(base, parameters, error, time, evaluations):
    """
    Stores a set of ``parameters``, an RMSE ``error``, and the ``time`` and
    number of ``evaluations`` it took to obtain the result in a file based on
    the given ``base`` name.
    """
    path = base + '.txt'
    assert(len(parameters) == 9)
    error = float(error)
    time = float(time)
    evaluations = int(evaluations)

    print('Writing results to ' + str(path))
    with open(path, 'w') as f:
        f.write('error: ' + pints.strfloat(error) + '\n')
        f.write('time: ' + pints.strfloat(time) + '\n')
        f.write('evaluations: ' + str(evaluations) + '\n')
        f.write('parameters:\n')
        for p in parameters:
            f.write('    ' + pints.strfloat(p) + '\n')
    print('Done')


def count(cell, method, search_transformation='a', sample_transformation='a',
          start_from_m1=False, method_1b=False, parse=True):
    """
    Counts the number of results available for the given configuration.

    If ``parse`` is set to ``False``, unfinished and corrupt result files are
    also included in the count.
    """
    if parse:
        # Count parsed results
        parts = load(
            cell, method, search_transformation, sample_transformation,
            start_from_m1, method_1b)
        return len(parts[0])
    else:
        dirname, root = _root_name(
            cell, method, search_transformation, sample_transformation,
            start_from_m1, method_1b)
        return len(list(glob.glob(os.path.join(dirname, root + '*.txt'))))


def load(cell, method, search_transformation='a', sample_transformation='a',
         start_from_m1=False, method_1b=False):
    """
    Returns all results for the given configuration.

    Returns a tuple ``(run, parameters, error, time, evaluations)``, containing
    a list of run indices, a list of parameter vectors, a list of errors, and
    lists of evaluation times and evaluation counts.

    Each list is ordered by error (lowest first).
    """
    dirname, root = _root_name(
        cell, method, search_transformation, sample_transformation,
        start_from_m1, method_1b)

    # Create empty lists
    rs, ps, es, ts, ns = [], [], [], [], []

    # Find matching files
    fs = glob.glob(os.path.join(dirname, root + '*.txt'))
    for path in fs:
        filename = os.path.split(path)[1]
        i = int(os.path.splitext(filename)[0].rsplit('-', 1)[1])

        # Naively parse file, warn and skip unparseable files
        p = e = t = n = None
        try:
            todo = 4
            with open(path, 'r') as f:
                for i in range(100):    # Give up after 100 lines
                    line = f.readline().strip()
                    if line.startswith('error:'):
                        e = float(line[6:])
                        todo -= 1
                    elif line.startswith('time:'):
                        t = float(line[5:])
                        todo -= 1
                    elif line.startswith('evaluations:'):
                        n = int(line[12:])
                        todo -= 1
                    elif line == 'parameters:':
                        p = [float(f.readline()) for j in range(9)]
                        todo -= 1
                    if todo == 0:
                        break
                if todo:
                    print('Unable to find all information, skipping '
                          + filename)
                    continue
        except Exception as e:
            print('Error when parsing file, skipping ' + filename)
            print(e)
            continue

        # Store
        rs.append(i)
        ps.append(p)
        es.append(e)
        ts.append(t)
        ns.append(n)

    # Convert to arrays and sort
    es = np.array(es)
    order = np.argsort(es)
    rs = np.array(rs)[order]
    ps = np.array(ps)[order]
    es = es[order]
    ts = np.array(ts)[order]
    ns = np.array(ns)[order]

    return (rs, ps, es, ts, ns)


def load_parameters(
        cell, method, search_transformation='a', sample_transformation='a',
        start_from_m1=False, method_1b=False, repeats=False):
    """
    Returns the parameters obtained from a fit with a given ``method`` to data
    from the specified ``cell`` with the given configuration.

    If ``repeats=True``, all obtained parameter sets will be returned.
    """
    if method == 1 and not method_1b:
        path = _root_name(
            cell, method, search_transformation, sample_transformation,
            start_from_m1, method_1b)
        path = os.path.join(*path) + '.txt'
        with open(path, 'r') as f:
            p = np.array([float(x) for x in f.readlines()])
            assert len(p) == 9
        return p

    rs, ps, es, ts, ns = load(
        cell, method, search_transformation, sample_transformation,
        start_from_m1, method_1b)
    if repeats:
        return ps
    else:
        return ps[0] if len(ps) else None


def load_errors(
        cell, method, search_transformation='a', sample_transformation='a',
        start_from_m1=False, method_1b=False):
    """
    Returns the (sorted) errors for all repeats for the given fit.
    """
    rs, ps, es, ts, ns = load(
        cell, method, search_transformation, sample_transformation,
        start_from_m1, method_1b)
    return es


def load_times(
        cell, method, search_transformation='a', sample_transformation='a',
        start_from_m1=False, method_1b=False):
    """
    Returns the (sorted) times for all repeats for the given fit.
    """
    rs, ps, es, ts, ns = load(
        cell, method, search_transformation, sample_transformation,
        start_from_m1, method_1b)
    return ts


def load_evaluations(
        cell, method, search_transformation='a', sample_transformation='a',
        start_from_m1=False, method_1b=False):
    """
    Returns the (sorted) evaluations for all repeats for the given fit.
    """
    rs, ps, es, ts, ns = load(
        cell, method, search_transformation, sample_transformation,
        start_from_m1, method_1b)
    return ns


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
