#!/usr/bin/env python3
#
# Show estimated reversal potentials
#
from __future__ import division
from __future__ import print_function
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import cells


for i in range(9):
    E = cells.reversal_potential(cells.temperature(i + 1))

    print('Cell ' + str(i + 1) + ': ' + str(E))

