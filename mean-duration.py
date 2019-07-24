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
    ['M3', 3, 'a', 'a', False, False],
    ['M4', 4, 'a', 'a', False, False],
    ['AP', 5, 'a', 'a', False, False],
    ['M1b', 1, 'a', 'a', False, True],
    ['M2b', 2, 'a', 'a', True, False],
    ['M3b', 3, 'a', 'a', True, False],
    ['M2-na', 2, 'n', 'a', False, False],
    ['M2-fa', 2, 'f', 'a', False, False],
    ['M2-an', 2, 'a', 'n', False, False],
    ['M2-af', 2, 'a', 'f', False, False],
    ['M2-nn', 2, 'n', 'n', False, False],
    ['M2-ff', 2, 'f', 'f', False, False],
    ['M3-na', 3, 'n', 'a', False, False],
    ['M3-fa', 3, 'f', 'a', False, False],
    ['M3-an', 3, 'a', 'n', False, False],
    ['M3-af', 3, 'a', 'f', False, False],
    ['M3-nn', 3, 'n', 'n', False, False],
    ['M3-ff', 3, 'f', 'f', False, False],
    ['M4-na', 4, 'n', 'a', False, False],
    ['M4-fa', 4, 'f', 'a', False, False],
    ['M4-an', 4, 'a', 'n', False, False],
    ['M4-af', 4, 'a', 'f', False, False],
    ['M4-nn', 4, 'n', 'n', False, False],
    ['M4-ff', 4, 'f', 'f', False, False],
]
rules = [0, 7, 13, 19]

header = [
    'Option',
    'Mean',
    'Mean*50',
    'Mean*80',
    'Min',
    '10%',
    '90%',
    'Max',
]

cells = range(1, 11)

def format_time(seconds=None):
    if seconds < 60:
        return str(round(seconds, 1)) + ' sec'
    minutes = seconds / 60
    if minutes < 60:
        return str(round(minutes, 1)) + ' min'
    hours = minutes / 60
    if hours < 24:
        return str(round(hours, 1)) + ' hrs'
    days = hours / 24
    return str(round(days, 1)) + ' days'


rows = [header]
for i, ropt in enumerate(row_opts):
    name, method, search, sample, start_from_m1, method_1b = ropt

    times = []
    for cell in cells:
        times.extend(
            results.load_times(
                cell, method, search, sample, start_from_m1, method_1b))

    row = [name]
    if times:
        row.append(format_time(np.mean(times)))
        row.append(format_time(np.mean(times) * 50))
        row.append(format_time(np.mean(times) * 80))
        row.append(format_time(np.min(times)))
        row.append(format_time(np.percentile(times, 10)))
        row.append(format_time(np.percentile(times, 90)))
        row.append(format_time(np.max(times)))
    else:
        row.extend([''] * 7)
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
    print(' | '.join(row))
    if i in rules:
        print('-+-'.join(['-' * len(x) for x in row]))

