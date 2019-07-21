#!/usr/bin/env python3
#
# Count the number of fitting results available.
#
#
import numpy as np
import os
import sys

# Load project modules
sys.path.append(os.path.abspath('python'))
import results
import transformations


row_opts = [
    ['M2', 2, 'a', 'a', False, False],
    ['M2b', 2, 'a', 'a', True, False],
    ['M2-na', 2, 'n', 'a', False, False],
    ['M2-fa', 2, 'f', 'a', False, False],

    ['M3', 3, 'a', 'a', False, False],
    ['M3b', 3, 'a', 'a', True, False],
    ['M3-na', 3, 'n', 'a', False, False],
    ['M3-fa', 3, 'f', 'a', False, False],
    ['M3-an', 3, 'a', 'n', False, False],
    ['M3-af', 3, 'a', 'f', False, False],
    ['M3-nn', 3, 'n', 'n', False, False],
    ['M3-ff', 3, 'f', 'f', False, False],

    ['M4', 4, 'a', 'a', False, False],
    ['M4-na', 4, 'n', 'a', False, False],
    ['M4-fa', 4, 'f', 'a', False, False],
    ['M4-an', 4, 'a', 'n', False, False],
    ['M4-af', 4, 'a', 'f', False, False],
    ['M4-nn', 4, 'n', 'n', False, False],
    ['M4-ff', 4, 'f', 'f', False, False],

    ['M4-ak', 4, 'a', 'k', False, False],
    ['M4-ka', 4, 'k', 'a', False, False],
    ['M4-kk', 4, 'k', 'k', False, False],

    ['AP', 5, 'a', 'a', False, False],
]
rules = [0, 4, 12, 19, 22]

header = ['Option'] + [str(1 + i) for i in range(10)]

fmat = '{:<1.3f}'

cells = range(1, 11)

rows = [header]
for i, ropt in enumerate(row_opts):
    name, method, search, sample, start_from_m1, method_1b = ropt

    row = [name]
    for cell in cells:
        fs = results.load_errors(cell, *ropt[1:])
        if len(fs):
            f0 = fmat.format(fs[0])
            # Remove extra 0
            #assert(f0[6] == '0')
            #f0 = f0[:6] + f0[7:]

            row.append(f0)
        else:
            row.append('')
    rows.append(row)


# Set column widths
widths = [0] * len(rows[0])
for row in rows:
    assert(len(row) == len(widths))
    for j, x in enumerate(row):
        if len(x) > widths[j]:
            widths[j] = len(x)

# Pad cells
for i in range(len(rows)):
    row = rows[i]
    for j in range(len(row)):
        row[j] = ' ' * (widths[j] - len(row[j])) + row[j]

# Print table
for i, row in enumerate(rows):
    print(row[0] + ' | ' + ' '.join(row[1:]))
    if i in rules:
        bits = ['-' * len(x) for x in row]
        print(bits[0] + '-+-' + '-'.join(bits[1:]))

