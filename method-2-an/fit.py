#!/usr/bin/env python3
#
# Method 2: Simulate the traditional protocols, calculate the summary
# statistic, and then optimise the model to match the experimental summary
# statistics.
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
fitting.cmd(2, 'a', 'n')
