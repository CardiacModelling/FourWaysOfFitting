#!/usr/bin/env python3
#
# Method 1b: Optimise on the Method 1 error measure.
#
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
fitting.cmd(1, method_1b=True)
