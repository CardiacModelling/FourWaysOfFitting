#!/usr/bin/env python3
#
# Count the number of fitting results available.
#
#
import os
import sys

# Load project modules
sys.path.append(os.path.abspath('python'))
import results


row_opts = [
    [1, 'a', 'a'],
    [2, 'a', 'a'],
    [3, 'a', 'a'],
    [4, 'a', 'a'],
    [5, 'a', 'a'],
    [6, 'a', 'a'],
    [7, 'a', 'a'],
    [8, 'a', 'a'],
    [9, 'a', 'a'],
    [10, 'a', 'a'],

    [5, 'n', 'a'],
    [5, 'f', 'a'],
    [5, 'a', 'n'],
    [5, 'a', 'f'],
    [5, 'n', 'n'],
    [5, 'f', 'f'],

    [10, 'n', 'a'],
    [10, 'f', 'a'],
    [10, 'a', 'n'],
    [10, 'a', 'f'],
    [10, 'n', 'n'],
    [10, 'f', 'f'],

    [10, 'a', 'k'],
    [10, 'k', 'a'],
    [10, 'k', 'k'],
]

col_opts = [
    [1, False, False],
    [2, False, False],
    [3, False, False],
    [4, False, False],
    [1, False, True],
    [2, True, False],
    [3, True, False],
    [5, False, False],
]

header = [
    'Cell',
    'Variant',
    'M1',
    'M2',
    'M3',
    'M4',
    'M1b',
    'M2b',
    'M3b',
    'AP',
]
assert(len(header) - 2 == len(col_opts))


rows = [header]
for ropt in row_opts:
    cell, search_transformation, sample_transformation = ropt

    tname = search_transformation + ', ' + sample_transformation
    tname = '' if tname == 'a, a' else tname

    row = [str(cell), tname]
    for copt in col_opts:
        method, start_from_m1, method_1b = copt

        skip = False
        if method == 1:
            if tname != '':
                skip = True
            elif cell > 9 and method_1b:
                skip = True
            else:
                trans = None
        elif method == 5 or start_from_m1:
            if cell > 9 or tname != '':
                skip = True
        if skip:
            row.append('XX')
            continue

        try:
            parameters = results.load_parameters(
                cell, method, search_transformation, sample_transformation,
                start_from_m1, method_1b, True)
        except FileNotFoundError:
            row.append('0')
            continue
        if method == 1 and not method_1b:
            row.append('1')
        else:
            row.append(str(len(parameters)))
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
        pad = ' ' * (widths[j] - len(row[j]))
        row[j] = row[j] + pad if j == 1 else pad + row[j]

# Print table
for i, row in enumerate(rows):
    print(' | '.join(row))
    if i in [0, 10, 16, 22]:
        print('-+-'.join(['-' * len(x) for x in row]))

