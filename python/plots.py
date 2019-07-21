#!/usr/bin/env python3
#
# Standard plots for all protocols
#
from __future__ import division, print_function
import myokit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Import local modules
import data
import results
import sumstat


# Colour map for traditional protocol plots
colormap = 'jet'
cmap_fix = 1
# colormap = 'nipy_spectral'
# cmap_fix = 1.1

# Colours and markers for summary_statistics
marker_act = 'g^'

# Colours and markers for cells
cell_markers = ['o', 's', 'p', 'D', 'X', '*', '+', 'x', 'v']


def fold(protocol, time, voltage, currents, labels=None, markers=None):
    """
    Create a folded plot of a given protocol, using the data given.
    """
    # Get split points
    split = sumstat.split_points(protocol)

    # Define zoom points
    zoom = {
        3: ((500, 6500), (-0.1, 1.75)),
        4: ((1180, 1500), (-3.2, 6.5)),
        5: ((2300, 8000), (-4, 2)),
    }

    # Create colormap
    cmap = matplotlib.cm.get_cmap(colormap)
    norm = matplotlib.colors.Normalize(0, (len(split) - 1) * cmap_fix)

    # Create plot
    plt.figure()
    matplotlib.gridspec.GridSpec(4, 1)

    plt.subplot2grid((4, 1), (0, 0))
    plt.xlabel('Time (ms)')
    plt.ylabel('V (mV)')
    for i, bounds in enumerate(split):
        lower, upper = bounds
        plt.plot(time[lower:upper] - time[lower], voltage[lower:upper],
                 color=cmap(norm(i)))

    plt.subplot2grid((4, 1), (1, 0), rowspan=3)
    plt.xlabel('Time (ms)')
    plt.ylabel('I (nA)')
    for i, bounds in enumerate(split):
        lower, upper = bounds
        for j, current in enumerate(currents):
            label = labels[j] if labels and i == 0 else None
            marker = markers[j] if markers else None
            plt.plot(
                time[lower:upper] - time[lower], current[lower:upper],
                marker, color=cmap(norm(i)), label=label)

    if labels:
        plt.legend()

    try:
        xlim, ylim = zoom[protocol]
        plt.xlim(*xlim)
        plt.ylim(*ylim)
    except KeyError:
        pass


def current(
        ax, cell, protocol, lw=1, technicolor=False, log=None, alpha=None,
        cap_filter=True, label=None):
    """
    Creates a (possibly folded) plot on axes ``ax`` of the currents measured in
    the given ``cell`` during the given ``protocol``.
    """
    # Load signal
    if log is None:
        log = data.load(cell, protocol)
    t = log['time']
    c = log['current']

    # Plot
    if protocol < 6:
        # Fold steps
        variant = protocol in (1, 2) and cell in (7, 8)
        if cap_filter:
            split = sumstat.split_points(protocol, variant)
        else:
            split = sumstat.split_points_nocap(protocol, variant)
        cmap = matplotlib.cm.get_cmap(colormap)
        norm = matplotlib.colors.Normalize(0, (len(split) - 1) * cmap_fix)
        for i, bounds in enumerate(split):
            if technicolor:
                color = cmap(norm(i))
            else:
                color = 'k'
            lo, hi = bounds
            ax.plot(
                t[lo:hi] - t[lo], c[lo:hi], color=color, lw=lw, alpha=alpha,
                label=(label if i == 0 else None))

    else:
        # Normal plot
        if technicolor:
            _technicolor_dreamline(ax, t, c)
        else:
            ax.plot(t, c, color='tab:blue', alpha=alpha)


def voltage(
        ax, cell, protocol, lw=1, technicolor=False, values=None,
        cap_filter=True):
    """
    Creates a (possibly folded) plot on axes ``ax`` of the voltage for a given
    ``protocol``.
    """
    # Get voltage signal
    variant = protocol in (1, 2) and cell in (7, 8)
    if values is None:
        t, v = data.load_protocol_values(protocol, variant)
    else:
        t, v = values

    # Plot
    if protocol < 6:
        # Fold steps
        if cap_filter:
            split = sumstat.split_points(protocol, variant)
        else:
            split = sumstat.split_points_nocap(protocol, variant)
        cmap = matplotlib.cm.get_cmap(colormap)
        norm = matplotlib.colors.Normalize(0, (len(split) - 1) * cmap_fix)
        for i, bounds in enumerate(split):
            lo, hi = bounds
            ax.plot(t[lo:hi] - t[lo], v[lo:hi], color=cmap(norm(i)), lw=lw)
    else:
        # Normal plot
        if technicolor:
            _technicolor_dreamline(ax, t, v)
        else:
            ax.plot(t, v, color='tab:green')


def _technicolor_dreamline(ax, x, y, z=None, lw=1):
    """
    Draws a multi-coloured line.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    if z is not None:
        z = np.asarray(z)

    # Invisible plot for automatic x & y limits
    if z is None:
        ax.plot(x, y, alpha=0)
    else:
        ax.plot(x, y, z, alpha=0)

    # Create collection of line segments
    stride = int(len(x) / 1000)
    n = 1 + (len(x) - 1) // stride
    segments = []
    for i in range(n):
        lo = i * stride
        hi = lo + stride + 1
        xs = x[lo:hi]
        ys = y[lo:hi]
        if z is None:
            segments.append(np.vstack((xs, ys)).T)
        else:
            zs = z[lo:hi]
            segments.append(np.vstack((xs, ys, zs)).T)
    n = len(segments)

    if z is None:
        Collection = matplotlib.collections.LineCollection
    else:
        Collection = Line3DCollection

    ax.add_collection(Collection(
        segments,
        cmap=plt.cm.get_cmap(colormap),
        norm=matplotlib.colors.Normalize(0, cmap_fix),
        array=np.linspace(0, 1, n),
        lw=lw,
    ))


def _phase_model():
    """
    Returns a model for phase plane simulations, using Kylie's parameters for
    cell 9.
    """
    # Load model, set Kylie's sine wave parameters for Cell 5
    m = data.load_myokit_model()
    for i, p in enumerate(results.load_kylie_parameters(5)):
        m.get('ikr.p' + str(1 + i)).set_rhs(p)
    return m


def _phase_attractor(ax, model=None, lt='-', color=None, lw=None,
                     numbers=None):
    """
    Plots the attractor / stable point for the states as a function of V.
    """
    if model is None:
        model = _phase_model()

    ainf = model.get('ikr.act.inf').pyfunc()
    rinf = model.get('ikr.rec.inf').pyfunc()
    v = np.linspace(-250, 50, 400)
    x = ainf(v)
    y = rinf(v)
    ax.plot(x, y, lt, color=color, lw=lw)

    if numbers is not None:
        xof = 0.06
        yof = 0

        try:
            vs = list(numbers)
        except Exception:
            vs = [-120, ] + list(range(-100, 20, 10))

        for v in vs:
            if v > -40:
                yof = 0.04
                xof = 0.025
            ax.plot(ainf(v), rinf(v), 'x')
            ax.text(
                ainf(v) + xof, rinf(v) + yof, str(v) + ' mV', fontsize=7,
                verticalalignment='center')


def _phase_arrows(ax, x, y, color=None, p=100, alpha=None):
    """
    Plots some arrows on a line.

    Arguments: ``p`` is for spacing.
    """
    w, h = x[1::p] - x[:-1:p], y[1::p] - y[:-1:p]
    x, y = x[::p], y[::p]
    n = min(len(w), len(h), len(x), len(y))
    w, h, x, y = w[:n], h[:n], x[:n], y[:n]
    ax.quiver(
        x, y, w, h, scale_units='xy', angles='xy', scale=1, color=color,
        width=0.009, minshaft=0.001, minlength=0.001, alpha=alpha,
    )


def _phase_simulation(protocol, all_signals=False):
    """
    Runs a simulation to create a phase plot for the given protocol, using the
    parameters found by Kylie for Cell 5.

    Returns a tuple ``(model, activation, recovery)`` if ``all_signals=False``,
    else a tuple ``(model, time, voltage, current, activation, recover)``.
    """
    m = _phase_model()

    # Move to stable state at -80mV
    m.get('ikr.act').set_state_value(m.get('ikr.act.inf').pyfunc()(-80))
    m.get('ikr.rec').set_state_value(m.get('ikr.rec.inf').pyfunc()(-80))

    # Load protocol, run simulation
    p = data.load_myokit_protocol(protocol)
    if protocol == 7:
        r = m.get('membrane.V').rhs()
        m.get('membrane.V').set_rhs(
            'if(engine.time >= 3000.1 and engine.time < 6500.1,'
            + ' - 30'
            + ' + 54 * sin(0.007 * (engine.time - 2500.1))'
            + ' + 26 * sin(0.037 * (engine.time - 2500.1))'
            + ' + 10 * sin(0.190 * (engine.time - 2500.1))'
            + ', engine.pace)')
    s = myokit.Simulation(m, p)
    if protocol == 7:
        m.get('membrane.V').set_rhs(r)
    if protocol == 6:
        times, values = data.load_protocol_values(protocol)
        s.set_fixed_form_protocol(times, values)
        d = s.run(times[-1] + 0.2, log_times=times).npview()
    else:
        d = s.run(p.characteristic_time(), log_interval=0.1).npview()

    if all_signals:
        return (m, d.time(), d['membrane.V'], d['ikr.IKr'],
                d['ikr.act'], d['ikr.rec'])
    return m, d['ikr.act'], d['ikr.rec']


def phase(ax, protocol, sim=None, limits=None, alpha=None):
    """
    Creates a 2d phase portrait for the given protocol, using the parameters
    found by Kylie for Cell 5.
    """
    if sim is None:
        m, act, rec = _phase_simulation(protocol)
    else:
        m, act, rec = sim

    # Allow partial drawing
    if limits is not None:
        lo, hi = limits
        act = act[lo:hi]
        rec = rec[lo:hi]

    # Update axis limits
    ax.set_xlim(-0.05, 1)
    ax.set_ylim(-0.05, 1)

    # Draw grid
    color = '#cccccc'
    lw = 0.5
    ax.axvline(0, color=color, lw=lw)
    ax.axhline(0, color=color, lw=lw)
    ax.axvline(0.5, color=color, lw=lw)
    ax.axhline(0.5, color=color, lw=lw)
    # plt.axvline(1, color=color, lw=lw)
    # plt.axhline(1, color=color, lw=lw)

    # Plot attractor
    _phase_attractor(ax, m, color='#999999', lw=0.5)

    # Estimate spacing for arrows
    arrow_spacing = {
        1: 50,
        2: 50,
        3: 100,
        4: 800,
        5: 800,
    }
    arrow_spacing = arrow_spacing.get(protocol, 100)
    if protocol < 6:
        split = sumstat.split_points(protocol)
        cmap = matplotlib.cm.get_cmap(colormap)
        norm = matplotlib.colors.Normalize(0, (len(split) - 1) * cmap_fix)
        for i, bounds in enumerate(split):
            lo, hi = bounds
            x = act[lo:hi]
            y = rec[lo:hi]
            ax.plot(x, y, color=cmap(norm(i)), lw=1, alpha=alpha)
            _phase_arrows(
                ax, x, y, color=cmap(norm(i)), p=arrow_spacing, alpha=alpha)
    else:
        _technicolor_dreamline(ax, act, rec, lw=1)


def phase3d(ax, protocol):
    """
    Creates a phase plane plot on a 3d set of axes.
    """
    m, t, v, i, act, rec = _phase_simulation(protocol, True)

    ax.set_xlim(-0.05, 1)
    ax.set_ylim(-0.05, 1)

    # Plot attractor
    ainf = m.get('ikr.act.inf').pyfunc()
    rinf = m.get('ikr.rec.inf').pyfunc()
    vat = np.linspace(-140, 50, 140)
    ax.plot(ainf(vat), rinf(vat), vat, color='#999999')

    if protocol < 6:
        split = sumstat.split_points(protocol)
        cmap = matplotlib.cm.get_cmap(colormap)
        norm = matplotlib.colors.Normalize(0, (len(split) - 1) * cmap_fix)
        for i, bounds in enumerate(split):
            lo, hi = bounds
            x = act[lo:hi]
            y = rec[lo:hi]
            z = v[lo:hi]
            ax.plot(x, y, z, color=cmap(norm(i)))
            # _phase_arrows(ax, x, y, color=cmap(norm(i)), p=arrow_spacing)
    else:
        _technicolor_dreamline(ax, act, rec, v)


def prior12(ax, logx, logy=False, labels=True):
    """
    Draw the prior for p1 and p2.
    """
    ga1 = 0.3
    ga2 = 0.2

    lower_alpha = 1e-7              # Kylie: 1e-7
    upper_alpha = 1e3               # Kylie: 1e3
    lower_beta = 1e-7               # Kylie: 1e-7
    upper_beta = 0.4                # Kylie: 0.4

    ax.axvline(lower_alpha, color='k', alpha=ga1)
    ax.axvline(upper_alpha, color='k', alpha=ga1)
    ax.axhline(lower_beta, color='k', alpha=ga1)
    ax.axhline(upper_beta, color='k', alpha=ga1)

    rmin = 1.67e-5
    rmax = 1000
    # vmin = -120
    vmax = 58.25

    n = 1000

    if logx:
        a = np.exp(np.linspace(np.log(lower_alpha), np.log(upper_alpha), n))
        ax.set_xscale('log')
        ax.set_xlim(lower_alpha * 0.3, upper_alpha * 3)
    else:
        a = np.linspace(lower_alpha, upper_alpha, n)
        ax.set_xlim(lower_alpha - 50, upper_alpha + 50)

    if logy:
        ax.set_yscale('log')
        ax.set_ylim(lower_beta * 0.3, upper_beta * 3)
    else:
        ax.set_ylim(lower_beta - 0.02, upper_beta + 0.02)


    bmin = (1 / vmax) * (np.log(rmin) - np.log(a))
    bmax = (1 / vmax) * (np.log(rmax) - np.log(a))
    bmin = np.maximum(bmin, lower_beta)
    bmax = np.minimum(bmax, upper_beta)
    bmax = np.maximum(bmax, lower_beta)
    ax.fill_between(
        a, bmin, bmax, color='k', alpha=ga2,
        label='Bounded area' if labels else None
    )

    ax.plot(a, bmin, label='Lower bound' if labels else None)
    ax.plot(a, bmax, label='Upper bound' if labels else None)


def prior34(ax, logx, logy=False, labels=True):
    """
    Draw the prior for p3 and p4.
    """
    ga1 = 0.3
    ga2 = 0.2

    lower_alpha = 1e-7              # Kylie: 1e-7
    upper_alpha = 1e3               # Kylie: 1e3
    lower_beta = 1e-7               # Kylie: 1e-7
    upper_beta = 0.4                # Kylie: 0.4

    ax.axvline(lower_alpha, color='k', alpha=ga1)
    ax.axvline(upper_alpha, color='k', alpha=ga1)
    ax.axhline(lower_beta, color='k', alpha=ga1)
    ax.axhline(upper_beta, color='k', alpha=ga1)

    rmin = 1.67e-5
    rmax = 1000
    vmin = -120
    # vmax = 58.25

    n = 1000

    if logx:
        a = np.exp(np.linspace(np.log(lower_alpha), np.log(upper_alpha), n))
        ax.set_xscale('log')
        ax.set_xlim(lower_alpha * 0.3, upper_alpha * 3)
    else:
        a = np.linspace(lower_alpha, upper_alpha, n)
        ax.set_xlim(lower_alpha - 50, upper_alpha + 50)

    if logy:
        ax.set_yscale('log')
        ax.set_ylim(lower_beta * 0.3, upper_beta * 3)
    else:
        ax.set_ylim(lower_beta - 0.02, upper_beta + 0.02)

    bmin = (-1 / vmin) * (np.log(rmin) - np.log(a))
    bmax = (-1 / vmin) * (np.log(rmax) - np.log(a))
    bmin = np.maximum(bmin, lower_beta)
    bmax = np.minimum(bmax, upper_beta)
    bmax = np.maximum(bmax, lower_beta)
    ax.fill_between(
        a, bmin, bmax, color='k', alpha=ga2,
        label='Bounded area' if labels else None
    )
    ax.plot(a, bmin, label='Lower bound' if labels else None)
    ax.plot(a, bmax, label='Upper bound' if labels else None)

