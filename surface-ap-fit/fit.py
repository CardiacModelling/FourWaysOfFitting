#!/usr/bin/env python3
#
# Fit to AP signal: Find optimal value of EAP for each cell, used only to draw
# a surface for EAP.
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
fitting.cmd(5)
