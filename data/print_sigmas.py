#!/usr/bin/env python3
#
# Estimate and show the sigma levels in all cells, all training data.
#
from __future__ import division
from __future__ import print_function
import numpy as np
import os
import sys

import matplotlib
import matplotlib.pyplot as plt

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import errors
import results

debug = False

# Get Kylie parameters
cell = 5
parameters = results.load_kylie_parameters(cell)

all_sigmas = []
for cell in range(1, 10):

    # Create E4 and E3 error, to extract problems
    em3 = errors.E3(cell)
    em4 = errors.E4(cell)

    problems = em3.problems() + em4.problems()

    sigmas = []
    for problem in problems:

        times = problem.times()
        values = problem.evaluate(parameters)

        # Estimate sigma
        sigma = np.std(problem.values()[:2500])
        print(sigma)

        if debug:
            plt.figure()
            plt.plot(times[:2500], problem.values()[:2500])

        sigmas.append(sigma)
    all_sigmas.append(sigmas)

all_sigmas = np.array(all_sigmas)
print(all_sigmas)
print(np.min(all_sigmas))
print(np.max(all_sigmas))
print(np.mean(all_sigmas))

if debug:
    plt.show()

