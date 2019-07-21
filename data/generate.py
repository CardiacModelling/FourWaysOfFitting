#!/usr/bin/env python3
#
# Generates synthetic data using the parameters for cell 5 given in Beattie et
# al.
#
from __future__ import division
from __future__ import print_function
import myokit
import numpy as np
import os
import sys

import matplotlib
import matplotlib.pyplot as plt

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import data
import errors
import results

# Get Kylie parameters
cell = 5
parameters = results.load_kylie_parameters(cell)

# Noise to add
cells = {
    10: 0.025,  # Max in data is 0.0247
}

# Get consistent results when regenerating
np.random.seed(1234)

# Create E4 and E3 error, to extract problems
em3 = errors.E3(cell, cap_filter=False)
em4 = errors.E4(cell, cap_filter=False)
em5 = errors.EAP(cell, cap_filter=False)
problems = em3.problems() + em4.problems() + em5.problems()

# Simulate and store
for i, problem in enumerate(problems):
    protocol = 2 + i

    # Maintain order of execution of a previous script, to get the same noise
    if protocol == 6:
        protocol = 7
    elif protocol == 7:
        protocol = 6

    times = problem.times()
    current = problem.evaluate(parameters)
    voltage = problem._model.simulated_v

    # Check if unfiltered
    assert int(round((times[-1] + 0.1) / 0.1)) == len(times)

    d = myokit.DataLog()
    d.set_time_key('time')
    d['time'] = times
    d['voltage'] = voltage

    for cell, sigma in cells.items():
        d['current'] = current + np.random.normal(0, sigma, size=times.shape)
        data.save(cell, protocol, d)

