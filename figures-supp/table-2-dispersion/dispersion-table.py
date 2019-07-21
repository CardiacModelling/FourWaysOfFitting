#!/usr/bin/env python3
#
# Dispersion of good results, per method, per cell
#
from __future__ import division, print_function
import os
import sys
import myokit
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpecFromSubplotSpec as SubGridSpec

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', '..', 'python')))
import results


#
# Check input arguments
#
base = os.path.splitext(os.path.basename(__file__))[0]
args = sys.argv[1:]
if len(args) != 0:
    print('Syntax: ' + base + '.py')
    sys.exit(1)

# Analyse obtained parameters
data = []
for cell in range(1, 11):
    row = [cell]
    for method in [2, 3, 4]:
        imethod = method - 1

        # Get scores, parameters
        rs, ps, es, ts, ns = results.load(cell, method)
        if len(rs) == 0:
            row.append(0)
            row.append(0)
            row.append(0)
            continue

        # Get maximum error in parameters of best fits
        i = es / es[0] - 1 < 0.01
        es = es[i]
        ps = ps[i]
        spread = 100 * np.max(np.abs(ps / ps[0] - 1))

        # Count how many results were also close in parameter space
        ds = np.max(np.abs(ps / ps[0] - 1), axis=1)
        ds = ds[ds < 0.01]

        row.append(spread)
        row.append(len(ps))
        row.append(len(ds))

    data.append(row)


# Pad table and print
rows = [['Cell', 'M2', 'n', '', 'M3', 'n', '', 'M4', 'n', '']]
rows += [[str(x) for x in row] for row in data]

widths = [0] * len(rows[0])
for row in rows:
    for i, x in enumerate(row):
        widths[i] = max(len(x), widths[i])

for row in rows:
    for i, w in enumerate(widths):
        row[i] += ' ' * (w - len(row[i]))
    print(' | '.join(row))


# Write latex versions to file
def table1(data):

    # Put Cell S in front
    data = [data[-1]] + data[:-1]

    data = np.array([[x[1], x[4], x[7]] for x in data]).T
    rows = []

    row = ['Method']
    row.append('Cell S')
    row.extend(['Cell ' + str(i) for i in range(1, 10)])
    rows.append(row)

    for imethod, dat in enumerate(data):
        row = [str(2 + imethod) + ' ' * 5]
        for x in dat:
            if type(x) != str:
                if x == 0:
                    x = '0'
                elif x < 0.01:
                    x = '{:<1.0e}'.format(x)
                    # Remove extra zero
                    assert(x[3] == '0')
                    x = x[:3] + x[4:]
                elif x < 1:
                    x = '{:<1.2f}'.format(x)
                else:
                    x = '{:<2.3f}'.format(x)
            row.append(x + ' ' * (6 - len(x)))
        rows.append(row)

    with open('table1.tex', 'w') as f:
        f.write('\\begin{tabular}{' + 'l ' * 11 + '}\n')
        f.write('\\hline\n')
        f.write(' & '.join(rows[0]) + '\\\\\n')
        f.write('\\hline\n')
        f.write(' & '.join(rows[1]) + '\\\\\n')
        f.write(' & '.join(rows[2]) + '\\\\\n')
        f.write(' & '.join(rows[3]) + '\\\\\n')
        f.write('\\hline\n')
        f.write('\\end{tabular}\n')


def table2(data):
    rows = []

    row = ['Method']
    row.append('Cell S')
    row.extend(['Cell ' + str(i) for i in range(1, 10)])
    rows.append(row)

    # Put Cell S at start
    data = [data[-1]] + data[:-1]

    # Extract numbers
    data1 = np.array([[x[2], x[5], x[8]] for x in data]).T
    data2 = np.array([[x[3], x[6], x[9]] for x in data]).T

    for imethod, dat1 in enumerate(data1):
        dat2 = data2[imethod]
        row = [str(2 + imethod) + ' ' * 5]

        for j in range(10):
            x = str(dat2[j]) + ' / ' + str(dat1[j])
            x += ' ' * (7 - len(x))
            row.append(x)

        rows.append(row)

    with open('table2.tex', 'w') as f:
        f.write('\\begin{tabular}{' + 'l ' * 11 + '}\n')
        f.write('\\hline\n')
        f.write(' & '.join(rows[0]) + '\\\\\n')
        f.write('\\hline\n')
        for row in rows[1:]:
            f.write(' & '.join(row) + '\\\\\n')
        f.write('\\hline\n')
        f.write('\\end{tabular}\n')


table1(data)
table2(data)

