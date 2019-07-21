#!/usr/bin/env python3
#
# Animated versions of the protocol plots.
#
from __future__ import division
from __future__ import print_function
import os
import sys
import numpy as np
import myokit
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

# Load project modules
sys.path.append(os.path.abspath(os.path.join('..', 'python')))
import plots
import sumstat


#
# Check input arguments
#
args = sys.argv[1:]
if len(args) != 2:
    print('Syntax:  animate.py <protocol> <live/save>')
    sys.exit(1)
protocol = int(args[0])
save = args[1].lower().strip() == 'save'
print('Selected protocol ' + str(protocol))
if save:
    print('Storing output as movie')
else:
    print('Showing output live on screen')

# Set font
matplotlib.rc('font', family='arial')

# Create empty figure
fig = plt.figure(figsize=(10, 4.8))
fig.subplots_adjust(0.065, 0.08, 0.98, 0.98)
grid = GridSpec(3, 2, hspace=0, wspace=0.2)
vx = fig.add_subplot(grid[0, 0])
cx = fig.add_subplot(grid[1:, 0])
px = fig.add_subplot(grid[:, 1])

# Set labels
cx.set_xlabel('Time (ms)')
cx.set_ylabel('I (nA)', labelpad=9)
vx.set_ylabel('V (mV)')
px.set_xlabel('Deactivated' + ' '*72 + 'Activated')
px.set_ylabel('Inactivated' + ' '*72 + 'Recovered')

# Update ticks
cx.xaxis.set_tick_params()
cx.yaxis.set_tick_params()
vx.set_xticklabels([])
vx.yaxis.set_tick_params()
px.xaxis.set_tick_params()
px.yaxis.set_tick_params()

# Run simulation
m, t, v, c, a, r = plots._phase_simulation(protocol, all_signals=True)

# Draw attractor
plots._phase_attractor(px, m, '--', '#999999')
ainf = m.get('ikr.act.inf').pyfunc()
rinf = m.get('ikr.rec.inf').pyfunc()

# Update axes
vx.set_ylim(-130, 70)
cx.set_ylim(1.1 * np.min(c), 1.1 * np.max(c))
px.set_xlim(-0.01, 1.01)
px.set_ylim(-0.01, 1.01)

# Choose colormap
colormap = 'jet'

# Set speed
fps = 20


if protocol < 6:

    #
    # Periodic protocols
    #

    # Split signal
    split = sumstat.split_points_nocap(protocol)
    norm = matplotlib.colors.Normalize(0, len(split) - 1)
    cmap = matplotlib.cm.get_cmap(colormap)

    # Update x-axes of current/voltage pltos
    vx.set_xlim(0, t[split[0][-1]])
    cx.set_xlim(0, t[split[0][-1]])

    # Work out timing
    stride = 100
    points_inner = split[0][1]
    steps_outer = len(split)
    steps_inner = (points_inner + stride - 1) // stride
    steps_total = steps_outer * steps_inner
    time_text = 'Current time: '

    # Draw 'ghost' of protocol
    for i in range(steps_outer):
        lo = i * points_inner
        hi = lo + points_inner
        vx.plot(t[0:points_inner], v[lo:hi], color='k', alpha=0.1)

    # If saving, show speed
    sim_seconds_per_frame = stride * 0.1 * 1e-3
    speed = fps * sim_seconds_per_frame
    if save:
        time_text = (
            'Displaying at ' + str(np.round(speed, 1)) + 'x real time. '
            + time_text)

    # Add objects to be updated during animation
    objects = [
        vx.plot([], [], color=cmap(norm(i)), animated=True)[0]
        for i in range(steps_outer)]
    objects.extend([
        cx.plot([], [], color=cmap(norm(i)), animated=True)[0]
        for i in range(steps_outer)])
    objects.extend([
        px.plot([], [], color=cmap(norm(i)), animated=True)[0]
        for i in range(steps_outer)])
    objects.extend([
        vx.plot([], [], 'o', color='k', animated=True, fillstyle='none')[0],
        cx.plot([], [], 'o', color='k', animated=True, fillstyle='none')[0],
        px.plot([], [], 'o', color='k', animated=True, fillstyle='none')[0],
        px.plot([], [], 'x', color='k', animated=True)[0],
        cx.text(0.01, 0.016, time_text + '0 s', transform=cx.transAxes),
    ])

    # Provide some feedback while creating the animation
    dots = 20
    print('Animation has ' + str(steps_total) + ' steps.')
    print(
        '(dot per ' + str(dots) + ' steps = '
        + str(steps_total // dots) + ' dots)')
    sys.stdout.write('Animating')

    # Update the graph
    def update(k):
        if k % dots == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        i = k // steps_inner
        j = k % steps_inner + 1
        thi = min(j * stride, points_inner)
        lo = points_inner * i
        hi = lo + thi
        objects[i + 0 * steps_outer].set_data(t[:thi], v[lo:hi])
        objects[i + 1 * steps_outer].set_data(t[:thi], c[lo:hi])
        objects[i + 2 * steps_outer].set_data(a[lo:hi], r[lo:hi])
        vv = v[hi - 1]
        objects[-5].set_data(t[thi - 1], vv)
        objects[-4].set_data(t[thi - 1], c[hi - 1])
        objects[-3].set_data(a[hi - 1], r[hi - 1])
        objects[-2].set_data(ainf(vv), rinf(vv))
        objects[-1].set_text(
            time_text + str(np.round(t[thi - 1] * 1e-3, 1)) + ' s')
        return objects

else:

    #
    # Non-periodic protocols
    #

    # Update x-axes of current/voltage pltos
    vx.set_xlim(0, t[-1])
    cx.set_xlim(0, t[-1])

    # Work out timing
    stride = 100
    n = 1 + (len(t) - 1) // stride
    steps_total = n
    time_text = 'Current time: '

    # If saving, show speed
    sim_seconds_per_frame = stride * 0.1 * 1e-3
    speed = fps * sim_seconds_per_frame
    if save:
        time_text = (
            'Displaying at ' + str(np.round(speed, 1)) + 'x real time. '
            + time_text)

    # Draw 'ghost' of protocol
    vx.plot(t, v, color='k', alpha=0.1)

    # Create colormap
    norm = matplotlib.colors.Normalize(0, 1)
    cmap = matplotlib.cm.get_cmap(colormap)

    # Create line segments, collections, and objects
    v_segments = []
    c_segments = []
    p_segments = []
    v_lines = matplotlib.collections.LineCollection(
        [], cmap=cmap, norm=norm, array=np.linspace(0, 1, n))
    c_lines = matplotlib.collections.LineCollection(
        [], cmap=cmap, norm=norm, array=np.linspace(0, 1, n))
    p_lines = matplotlib.collections.LineCollection(
        [], cmap=cmap, norm=norm, array=np.linspace(0, 1, n))
    vx.add_collection(v_lines)
    cx.add_collection(c_lines)
    px.add_collection(p_lines)
    objects = [
        v_lines,
        c_lines,
        p_lines,
        vx.plot([], [], 'o', color='k', animated=True, fillstyle='none')[0],
        cx.plot([], [], 'o', color='k', animated=True, fillstyle='none')[0],
        px.plot([], [], 'o', color='k', animated=True, fillstyle='none')[0],
        px.plot([], [], 'x', color='k', animated=True)[0],
        cx.text(0.01, 0.016, time_text + '0 s', transform=cx.transAxes),
    ]

    # Provide some feedback while creating the animation
    dots = 20
    print('Animation has ' + str(steps_total) + ' steps.')
    print(
        '(dot per ' + str(dots) + ' steps = '
        + str(steps_total // dots) + ' dots)')
    sys.stdout.write('Animating')

    # Update the graph
    def update(i):
        if i % dots == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        lo = i * stride
        hi = min(lo + stride, len(t) - 1)
        v_segments.append(np.vstack((t[lo:hi + 1], v[lo:hi + 1])).T)
        c_segments.append(np.vstack((t[lo:hi + 1], c[lo:hi + 1])).T)
        p_segments.append(np.vstack((a[lo:hi + 1], r[lo:hi + 1])).T)
        objects[0].set_segments(v_segments)
        objects[1].set_segments(c_segments)
        objects[2].set_segments(p_segments)
        objects[3].set_data(t[hi], v[hi])
        objects[4].set_data(t[hi], c[hi])
        objects[5].set_data(a[hi], r[hi])
        objects[6].set_data(ainf(v[hi]), rinf(v[hi]))
        objects[7].set_text(
            time_text + str(np.round(t[hi] * 1e-3, 1)) + ' s')
        return objects


# Create animation
ani = FuncAnimation(
    fig,
    update,
    steps_total,
    blit=True,
    # Interval is only used for live animation -- and is not accurate
    interval=1/fps,
    repeat=False,
)

# Display or store
if not save:
    # Note: slows down during run, timing is way off
    plt.show()
else:
    ani.save(
        'pr' + str(protocol) + '.mp4',
        writer='ffmpeg',
        #codec='ffv1',
        bitrate=3000,
        fps=fps)

print('\nDone')

