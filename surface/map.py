#!/usr/bin/env python3
#
# Map (part of) the surface defined by an error measure.
#
from __future__ import division, print_function
import os
import sys
import pints
import numpy as np
import myokit

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import boundaries
import cells
import errors
import results
import transformation


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) not in (4, 5):
    print('Syntax: ' + base + '.py <cell> <error> <n> <quad> <nc>')
    sys.exit(1)
cell = int(args[0])
method = int(args[1])
n = int(args[2])
assert n > 0
filename = 'cell-' + str(cell) + '-surface-' + str(method) + '-' + str(n)
print('Selected cell ' + str(cell))
print('Selected error ' + str(method))
print('Selected n ' + str(n))
if args[3] == 'all':
    print('Selected all quadrants')
    quads = [1, 2, 3, 4]
else:
    quads = [int(args[3])]
    assert 0 < quads[0] < 5
    print('Selected quadrant ' + str(quads[0]))
if len(args) == 5:
    nc = int(args[4])
    assert(nc > 0)
else:
    nc = pints.ParallelEvaluator.cpu_count()
print('Running with ' + str(nc) + ' worker processes')


#
# Define boundaries and parameter transformation
#
trans = transformation.Transformation()
boundaries = boundaries.Boundaries(cells.lower_conductance(cell), trans)


#
# Get best parameters
#
#pf5 = results.load_parameters(cell, 5)
pfm = results.load_parameters(cell, method)

# CHOOSE: EXPLORE OWN BEST OR AP BEST?
popt = pfm
qopt = trans.transform(popt)                    # Search space

lower_alpha = 1e-7
upper_alpha = 1e3
lower_beta  = 1e-7
upper_beta  = 0.4

# Set boundaries in search space
qalo = np.log(1e-7)
qahi = np.log(1e3)
qblo = 0

# Define method
if method == 1:
    f = errors.E1(cell, trans)
elif method == 2:
    f = errors.E2(cell, trans)
elif method == 3:
    f = errors.E3(cell, trans)
elif method == 4:
    f = errors.E4(cell, trans)
elif method == 5:
    f = errors.EAP(cell, trans)
else:
    print('Unknown method or not implemented')
    sys.exit(1)

# Show value at optimum
print(f(qopt))

for quad in quads:
    fname = filename + '-' + str(quad) + '.csv'
    print('Storing results to ' + fname)

    # Define grid in search space
    qbhi = 0.4 if (quad == 1 or quad == 3) else 0.2
    a = (quad - 1) * 2
    b = a + 1
    qs = []
    for qa in np.linspace(qalo, qahi, n):
        for qb in np.linspace(qblo, qbhi, n):
            q = np.copy(qopt)
            q[a] = qa
            q[b] = qb
            qs.append(q)
    qs = np.array(qs)
    ps = np.array([trans.detransform(q) for q in qs])

    # Evaluate
    e = pints.ParallelEvaluator(f, n_workers=nc)
    z = nc * 4
    imax = (len(qs) + z - 1) // z
    fs = np.ones(len(qs)) * 100
    print('Evaluating...')
    for i in range(imax):
        lo = i * z
        hi = lo + z
        fs[lo:hi] = e.evaluate(qs[lo:hi])
        print(str(1 + i) + ' out of ' + str(imax) + ', quad ' + str(quad))

    # Store results
    print('Storing results')
    d = myokit.DataLog()
    d['f'] = fs
    for i in range(9):
        d['p' + str(1 + i)] = ps[:, i]
    d.save_csv(fname)

print('Done')
