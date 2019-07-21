#!/usr/bin/env python3
#
# Method 2b: Simulate the traditional protocols, calculate the summary
# statistic, and then optimise the model to match the experimental summary
# statistics.
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
fitting.cmd(2, start_from_m1=True)
