#!/usr/bin/env python3
#
# Method 3b: Simulate the traditional protocols, optimise the model to match
# the recorded currents.
#
# Start from the best point returned by Method 1, and only perform 1 repeat.
#
# Searching: Use a log-transform on the A-parameters
# Sampling:  Use a log-transform on the A-parameters
#
import os
import sys

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import fitting


# Run
fitting.cmd(3, start_from_m1=True)
