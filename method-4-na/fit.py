#!/usr/bin/env python3
#
# Method 4: Simulate the sine wave protocol, optimise the model to match
# the recorded currents.
#
# Searching: Don't use a log-transform
# Sampling:  Use a log-transform on the A-parameters
#
import os
import sys

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import fitting


# Run
fitting.cmd(4, 'n', 'a')
