#!/usr/bin/env python3
#
# Pints ForwardModel that runs simulations with Kylie's model.
# Sine waves optional
#
from __future__ import division, print_function
import myokit
import myokit.lib.hh
import numpy as np
import pints

from data import model_path


class Model(pints.ForwardModel):
    """
    Pints ForwardModel that runs simulations with Kylie's model.
    Sine waves or data protocol optional.

    Arguments:

        ``protocol``
            A myokit.Protocol or a tuple (times, voltage)
        ``reversal_potential``
            The reversal potential
        ``sine_wave``
            Set to True if sine-wave protocol is being used.
        ``start_steady``
            Start at steady state for -80mV. Note that this should be disabled
            to get Kylie's original results.
        ``analytical``
            Use an analytical simulation.

    """
    parameters = [
        'ikr.p1',
        'ikr.p2',
        'ikr.p3',
        'ikr.p4',
        'ikr.p5',
        'ikr.p6',
        'ikr.p7',
        'ikr.p8',
        'ikr.p9',
    ]

    def __init__(
        self, protocol, reversal_potential, sine_wave=False,
        start_steady=False, analytical=False):

        # Load model
        model = myokit.load_model(model_path('beattie-2017-ikr-hh.mmt'))

        # Start at steady-state for -80mV
        if start_steady:
            print('Updating model to steady-state for -80mV.')
            model.get('membrane.V').promote()
            ai = model.get('ikr.act.inf').pyfunc()(-80)
            ri = model.get('ikr.rec.inf').pyfunc()(-80)
            model.get('membrane.V').demote()
            model.get('ikr.act').set_state_value(ai)
            model.get('ikr.rec').set_state_value(ri)

        # Set reversal potential
        assert reversal_potential < 0 #TODO: Remove this
        model.get('nernst.EK').set_rhs(reversal_potential)

        # Add sine-wave equation to model
        if sine_wave:
            model.get('membrane.V').set_rhs(
                'if(engine.time >= 3000.1 and engine.time < 6500.1,'
                + ' - 30'
                + ' + 54 * sin(0.007 * (engine.time - 2500.1))'
                + ' + 26 * sin(0.037 * (engine.time - 2500.1))'
                + ' + 10 * sin(0.190 * (engine.time - 2500.1))'
                + ', engine.pace)')

        # Create simulation
        self._analytical = analytical
        if not self._analytical:
            self.simulation = myokit.Simulation(model)

            # Add protocol
            if isinstance(protocol, myokit.Protocol):
                self.simulation.set_protocol(protocol)
            else:
                # Apply data-clamp
                times, voltage = protocol
                self.simulation.set_fixed_form_protocol(times, voltage)

                # Set max step size
                self.simulation.set_max_step_size(0.1)

            # Set solver tolerances
            self.simulation.set_tolerance(1e-8, 1e-8)

        else:
            if sine_wave:
                raise ValueError(
                    'Analytical simulation cannot be used with sine wave.')
            elif not isinstance(protocol, myokit.Protocol):
                raise ValueError(
                    'Analytical simulation cannote be used with data clamp.')
            model.get('membrane.V').set_label('membrane_potential')
            m = myokit.lib.hh.HHModel.from_component(
                model.get('ikr'), parameters=self.parameters)

            self.simulation = myokit.lib.hh.AnalyticalSimulation(m, protocol)

        # Set a maximum duration for each simulation.
        self._timeout = myokit.Timeout(60)

    def n_parameters(self):
        return len(self.parameters)

    def set_tolerances(self, tol):
        self.simulation.set_tolerance(tol, tol)

    def simulate(self, parameters, times):

        # Update model parameters
        for i, name in enumerate(self.parameters):
            self.simulation.set_constant(name, parameters[i])

        # Run
        self.simulation.reset()
        try:
            if self._analytical:
                d = self.simulation.run(
                    times[-1] + 0.5 * times[1],
                    log_times=times,
                    ).npview()
            else:
                d = self.simulation.run(
                    times[-1] + 0.5 * times[1],
                    log_times=times,
                    #log=['ikr.IKr', 'membrane.V'],
                    log=['ikr.IKr', 'membrane.V'],
                    progress=self._timeout,
                    ).npview()
        except myokit.SimulationError:
            return times * float('inf')
        except myokit.SimulationCancelledError:
            return times * float('inf')

        # Store membrane potential for debugging
        #self.simulated_v = d['membrane.V']

        # Return
        return d['ikr.IKr']

