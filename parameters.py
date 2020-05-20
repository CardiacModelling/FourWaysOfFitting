#!/usr/bin/env python3
#
# Table: Plot best parameters
#
from __future__ import division
from __future__ import print_function
import os
import sys
import numpy as np

# Load project modules
sys.path.append(os.path.abspath('python'))
import results

fmat1 = ' {:<1.2e}'

for imethod in range(4):
    method = 1 + imethod
    rows = []
    rows.append(['Cell'] + ['p' + str(1 + i) for i in range(9)])
    width = [2] * 10
    width[0] = 4
    for icell in range(9):
        cell = 1 + icell
        row = [str(cell)] + \
              [fmat1.format(x) for x in results.load_parameters(cell, method)]
        w = [max(width[i], len(x)) for i, x in enumerate(row)]
        rows.append(row)

    print('Method ' + str(method))
    for row in rows:
        fields = [field + ' ' * (w[i] - len(field))
                  for i, field in enumerate(row)]
        print(' | '.join(fields))
    print()

