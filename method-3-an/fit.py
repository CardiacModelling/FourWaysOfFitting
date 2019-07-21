#!/usr/bin/env python3
#
# Method 3: Simulate the traditional protocols, optimise the model to match
# the recorded currents.
#
# Searching: Use a log-transform on the A-parameters
# Sampling:  Don't use a log-transform
#
import os
import sys

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import fitting


# Run
fitting.cmd(3, 'a', 'n')
