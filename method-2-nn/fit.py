#!/usr/bin/env python3
#
# Method 2: Simulate the traditional protocols, calculate the summary
# statistic, and then optimise the model to match the experimental summary
# statistics.
#
# Searching: Don't use a log-transform
# Sampling:  Don't use a log-transform
#
import os
import sys

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import fitting


# Run
fitting.cmd(2, 'n', 'n')
