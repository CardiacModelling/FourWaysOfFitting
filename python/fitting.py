#!/usr/bin/env python3
#
# Performs a fit using method 2, 3, or 4
#
from __future__ import division, print_function
import os
import sys
import pints
import numpy as np

# Load project modules
import boundaries
import cells
import errors
import results
import transformations


debug = False


def cmd(method, search_transformation='a', sample_transformation='a',
        start_from_m1=False, method_1b=False, local_optimiser=False):
    """
    Handles command-line arguments to run a fit with one or all cells.
    """
    # Check input arguments
    base = os.path.basename(sys.argv[0])
    args = sys.argv[1:]

    # Get number of repeats
    cap = None
    if start_from_m1:
        repeats = 1
        if len(args) != 1:
            print('Syntax: ' + base + ' <cell|all>')
            return
    else:
        repeats = 5 if method_1b else 50
        if len(args) not in [1, 2, 3]:
            print('Syntax: ' + base + ' <cell|all>'
                  ' (repeats=' + str(repeats) + ')'
                  ' (cap=None)')
            return
        if len(args) > 1:
            repeats = int(args[1])
        if len(args) > 2:
            cap = int(args[2])

    # Get cell list
    if args[0] == 'all':
        # Note: "all" does not include synthetic data.
        cell_list = range(1, 10)
    else:
        cell_list = [int(x) for x in args[0].split(',')]

    # Run
    for cell in cell_list:
        fit(cell, method, search_transformation, sample_transformation,
        start_from_m1, method_1b, repeats, cap, local_optimiser)


def fit(cell, method, search_transformation='a', sample_transformation='a',
        start_from_m1=False, method_1b=False, repeats=1, cap=None,
        local_optimiser=False):
    """
    Performs a fit to data from cell ``cell``, using method ``method`` and the
    given configuration.

    If ``start_from_m1`` is set to ``True``, a single repeat will be run. Else,
    the number of repeats will be set by ``repeats`` and ``cap``.
    """
    # Check cell and method (better checking happens below)
    cell = int(cell)
    method = int(method)

    # Check compatibility of arguments, is handled in detail later via
    # results.reserve_base_name()
    if method == 1 and not method_1b:
        raise ValueError(
            'Only Method 1b is supported by fit(), not method 1.')
    if method != 1 and method_1b:
        raise ValueError('Method 1b can only be used if method 1 is chosen.')

    # Set method name for screen output
    method_name = str(method)
    if start_from_m1:
        method_name += 'b'

    # Create transformation objects
    search_transformation = transformations.create(search_transformation)
    sample_transformation = transformations.create(sample_transformation)

    # Define boundaries
    bounds = boundaries.Boundaries(
        search_transformation,
        sample_transformation,
        None if method == 1 else cells.lower_conductance(cell),
    )

    # Define error function
    if method == 1:
        g_fixed = results.load_parameters(cell, 1)[-1]
        f = errors.E1(cell, search_transformation, fixed_conductance=g_fixed)
    elif method == 2:
        f = errors.E2(cell, search_transformation)
    elif method == 3:
        f = errors.E3(cell, search_transformation)
    elif method == 4:
        f = errors.E4(cell, search_transformation)
    elif method == 5:
        f = errors.EAP(cell, search_transformation)
    else:
        raise ValueError('Method not supported: ' + str(method))

    # Check number of repeats
    if start_from_m1:
        repeats = 1
    else:
        repeats = int(repeats)
        if repeats < 1:
            raise ValueError('Number of repeats must be at least 1.')
        if debug:
            repeats = 3

    # Check cap on total number of runs
    if start_from_m1:
        cap = None
    elif cap is not None:
        cap = int(cap)
        if cap < 1:
            raise ValueError(
                'Cap on total number of runs must be at least 1 (or None).')

    # Run
    scores = []
    for i in range(repeats):

        # Cap max runs
        cap_info = ''
        if cap:
            n = results.count(
                cell, method,
                search_transformation.code(), sample_transformation.code(),
                start_from_m1, method_1b, local_optimiser, parse=False)
            if n >= cap:
                print()
                print('Maximum number of runs reached: terminating.')
                print()
                return
            cap_info = ' (run ' + str(n + 1) + ', capped at ' + str(cap) + ')'

        # Show configuration
        print()
        print('Cell   ' + str(cell))
        print('Method ' + method_name)
        print('Search ' + search_transformation.name())
        print('Sample ' + sample_transformation.name())
        print('Repeat ' + str(1 + i) + ' of ' + str(repeats) + cap_info)
        print()
        if start_from_m1:
            print('Starting from Method 1 result.')
        else:
            print('Starting point sampled from boundaries.')

        # Get base filename to store results in
        with results.reserve_base_name(
                cell, method,
                search_transformation.code(), sample_transformation.code(),
                start_from_m1, method_1b, local_optimiser) as base:
            print('Storing results using base ' + base)

            # Choose starting point
            if start_from_m1:
                # Start from method 1 results
                p0 = results.load_parameters(cell, 1)   # Model space
                q0 = search_transformation.transform(p0)       # Search space
            else:
                # Choose random starting point
                # Allow resampling, in case error calculation fails
                print('Choosing starting point')
                q0 = f0 = float('inf')
                while not np.isfinite(f0):
                    q0 = bounds.sample()    # Search space
                    f0 = f(q0)              # Initial score

            # Create optimiser
            if local_optimiser:
                opt = pints.OptimisationController(
                    f, q0, method=pints.NelderMead)
            else:
                opt = pints.OptimisationController(
                    f, q0, boundaries=bounds, method=pints.CMAES)
            opt.set_log_to_file(base + '.csv', True)
            opt.set_max_iterations(3 if debug else None)
            opt.set_parallel(not local_optimiser)

            # Run optimisation
            with np.errstate(all='ignore'):             # Ignore numpy warnings
                q, s = opt.run()                        # Search space
            p = search_transformation.detransform(q)    # Model space
            if method_1b:
                p = np.concatenate((p, [g_fixed]))

            # Store results for this run
            results.save(base, p, s, opt.time(), opt.evaluations())

        scores.append(s)

    # Order scores
    order = np.argsort(scores)
    scores = np.asarray(scores)[order]

    # Show results
    print('Best scores:')
    for score in scores[:10]:
        print(score)
    print('Mean & std of score:')
    print(np.mean(scores))
    print(np.std(scores))
    print('Worst score:')
    print(scores[-1])
