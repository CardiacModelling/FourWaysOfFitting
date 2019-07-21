#!/usr/bin/env python3
#
# Error functions for optimisation and validation
#
from __future__ import division, print_function
import myokit
import myokit.lib.hh
import numpy as np
import pints

# Load project modules
import cells
import data
import model
import sumstat
import transformations


class E1(pints.ErrorMeasure):
    """
    Pints error measure used only in validation, that compares model variables
    to simulated summary statistics (method 1).

    Arguments:

    ``cell``
        The cell index (1-9) to define the error on.
    ``transformation``
        An optional parameter transformation.
    ``fixed_conductance``
        If given, this conductance will be used, and conductance will be
        removed from the list of parameters.

    """
    def __init__(self, cell, transformation=None, fixed_conductance=None):

        # Store cell
        self.cell = cell

        # Store transformation object
        if transformation is None:
            transformation = transformations.NullTransformation()
        self.transformation = transformation

        # Calculate experimental summary statistics
        print('Calculating summary statistics for cell ' + str(cell))
        stats = sumstat.all_summary_statistics(cell)

        # Unpack
        self.vta, self.ta1 = stats[0]
        self.vtr, self.tr1 = stats[1]
        self.vai, self.ai1 = stats[2]
        self.vri, self.ri1 = stats[3]

        # Scale factors for error
        self.nta = 1 / len(self.ta1)
        self.ntr = 1 / len(self.tr1)
        self.nai = 1 / len(self.ai1)
        self.nri = 1 / len(self.ri1)
        self.zta = 1 / np.max(self.ta1)
        self.ztr = 1 / np.max(self.tr1)
        self.zai = 1
        self.zri = 1
        assert(self.zta > 0)
        assert(self.ztr > 0)

        # Store fix_conductance
        self._fixg = False
        self._g = None
        if fixed_conductance:
            self._fixg = True
            self._g = float(fixed_conductance)

    def n_parameters(self):
        return 8 if self._fixg else 9

    def __call__(self, parameters):

        # Transform parameters back to model space
        parameters = self.transformation.detransform(parameters)

        # Add fixed conductance
        if self._fixg:
            parameters = list(parameters) + [self._g]

        # Calculate model variables
        ta2 = sumstat.model_time_constant_of_activation(self.vta, parameters)
        tr2 = sumstat.model_time_constant_of_inactivation(self.vtr, parameters)
        ai2 = sumstat.model_steady_state_activation(self.vai, parameters)
        ri2 = sumstat.model_steady_state_inactivation(self.vri, parameters)

        # Calculate combined RMSE
        return (
            self.zta * np.sqrt(self.nta * np.sum((ta2 - self.ta1)**2)) +
            self.ztr * np.sqrt(self.ntr * np.sum((tr2 - self.tr1)**2)) +
            self.zai * np.sqrt(self.nai * np.sum((ai2 - self.ai1)**2)) +
            self.zri * np.sqrt(self.nri * np.sum((ri2 - self.ri1)**2))
        )


class E2(pints.ErrorMeasure):
    """
    Pints error measure that compares simulated to experimentally derived
    summarys statistics (method 2).

    Arguments:

    ``cell``
        The cell index (1-9) to define the error on.
    ``transformation``
        An optional parameter transformation.

    """
    def __init__(self, cell, transformation=None):

        # Store cell
        self.cell = cell

        # Store transformation object
        if transformation is None:
            transformation = transformations.NullTransformation()
        self.transformation = transformation

        # Calculate experimental summary statistics
        print('Calculating summary statistics for cell ' + str(cell))
        stats = sumstat.all_summary_statistics(cell)

        # Unpack
        self.ta1 = stats[0][1]
        self.tr1 = stats[1][1]
        self.ai1 = stats[2][1]
        self.ri1 = stats[3][1]
        self.iv1 = stats[4][1]

        # Scale factors for error
        self.nta = 1 / len(self.ta1)
        self.ntr = 1 / len(self.tr1)
        self.nai = 1 / len(self.ai1)
        self.niv = 1 / len(self.iv1)
        self.zta = 1 / np.max(self.ta1)
        self.ztr = 1 / np.max(self.tr1)
        self.zai = 1
        self.ziv = 1 / (np.max(self.iv1) - np.min(self.iv1))
        assert(self.zta > 0)
        assert(self.ztr > 0)
        assert(self.ziv > 0)

        # Load Myokit model
        model = data.load_myokit_model()
        model.get('membrane.V').set_label('membrane_potential')
        model.get('nernst.EK').set_rhs(
            cells.reversal_potential(cells.temperature(cell)))

        # Start at steady-state for -80mV
        print('Updating model to steady-state.')
        model.get('membrane.V').promote()
        ai = model.get('ikr.act.inf').pyfunc()(-80)
        ri = model.get('ikr.rec.inf').pyfunc()(-80)
        model.get('membrane.V').demote()
        model.get('ikr.act').set_state_value(ai)
        model.get('ikr.rec').set_state_value(ri)

        # Create analytical model
        m = myokit.lib.hh.HHModel.from_component(
            model.get('ikr'),
            parameters=[
                'ikr.p1',
                'ikr.p2',
                'ikr.p3',
                'ikr.p4',
                'ikr.p5',
                'ikr.p6',
                'ikr.p7',
                'ikr.p8',
                'ikr.p9',
            ],
        )

        # Load protocols, create simulations and times arrays
        self.simulations = []
        self.times = []
        for i in (2, 3, 4, 5):
            variant = (i == 2 and cell in (7, 8))
            p = data.load_myokit_protocol(i, variant=variant)
            self.simulations.append(myokit.lib.hh.AnalyticalSimulation(m, p))
            self.times.append(data.capacitance(
                p, 0.1, np.arange(0, p.characteristic_time(), 0.1))[0])

    def n_parameters(self):
        return 9

    def simulate(self, parameters):

        # Transform parameters back to model space
        parameters = self.transformation.detransform(parameters)

        # Run all simulations
        logs = [0] * 4
        for i, s in enumerate(self.simulations):

            # Reset simulation
            s.reset()

            # Update simulation parameters
            s.set_parameters(parameters)

            # Run simulation
            t = self.times[i]
            try:
                d = s.run(t[-1] + 0.1, log_times=t).npview()
            except myokit.SimulationError:
                return float('inf')

            # Store in same format as experimental data
            e = myokit.DataLog()
            e.set_time_key('time')
            e['time'] = d['engine.time']
            e['current'] = d['ikr.IKr']
            logs[i] = e

        # Calculate summary statistics
        try:
            stats = sumstat.all_summary_statistics(
                self.cell,
                pr2_log=logs[0],
                pr3_log=logs[1],
                pr4_log=logs[2],
                pr5_log=logs[3]
            )
        except Exception:
            import traceback
            e = traceback.format_exc()
            if 'Optimal parameters not found' not in e:
                print(e)
            return None

        return stats[0][1], stats[1][1], stats[2][1], stats[3][1], stats[4][1]

    def __call__(self, parameters):

        stats = self.simulate(parameters)
        if stats is None:
            return float('inf')

        ta2, tr2, ai2, ri2, iv2 = stats
        return (
            self.zta * np.sqrt(self.nta * np.sum((ta2 - self.ta1)**2)) +
            self.ztr * np.sqrt(self.ntr * np.sum((tr2 - self.tr1)**2)) +
            self.zai * np.sqrt(self.nai * np.sum((ai2 - self.ai1)**2)) +
            self.ziv * np.sqrt(self.niv * np.sum((iv2 - self.iv1)**2))
        )


class WholeTraceError(pints.ErrorMeasure):
    """
    Pints error measure that compares the whole traces of protocols.

    Arguments:

    ``cell``
        The cell index (1-9) to define the error on.
    ``protocols``
        The protocols (1-7) to define the error on.
    ``transformation``
        An optional transformation.
    ``cap_filter``
        Enable capacitance filtering (default: True)

    """
    def __init__(self, cell, protocols, transformation=None, cap_filter=True):

        # Store transformation object
        if transformation is None:
            transformation = transformations.NullTransformation()
        self._transformation = transformation

        # Store problems
        self._problems = []

        # Set individual errors and weights
        weights = []
        errors = []
        for protocol in protocols:

            # Create protocol
            if protocol == 6:
                p = data.load_protocol_values(protocol)
            else:
                p = data.load_myokit_protocol(protocol)

            # Create forward model
            m = model.Model(
                p,
                cells.reversal_potential(cells.temperature(cell)),
                sine_wave=(protocol == 7),
                analytical=(protocol < 6),
                start_steady=True
            )

            # Load data, create single output problem
            log = data.load(cell, protocol, cap_filter=cap_filter)
            time = log.time()
            current = log['current']

            # Create single output problem
            problem = pints.SingleOutputProblem(m, time, current)
            self._problems.append(problem)

            # Define error function
            errors.append(pints.RootMeanSquaredError(problem))

            # Add weighting based on range
            weights.append(1 / (np.max(current) - np.min(current)))

        # Create weighted sum of errors
        self._f = pints.SumOfErrors(errors, weights)

    def n_parameters(self):
        return 9

    def problems(self):
        """ Return the problems, e.g. for synthetic data generation. """
        return self._problems

    def __call__(self, parameters):

        # Transform parameters back to model space
        parameters = self._transformation.detransform(parameters)

        return self._f(parameters)


class E3(WholeTraceError):
    """
    Error measure on Pr2--5, for method 3.

    Arguments:

    ``cell``
        The cell index (1-9) to define the error on.
    ``transformation``
        An optional transformation.
    ``cap_filter``
        Enable capacitance filtering (default: True)

    """
    def __init__(self, cell, transformation=None, cap_filter=True):
        super(E3, self).__init__(
            cell, [2, 3, 4, 5], transformation, cap_filter)


class E4(WholeTraceError):
    """
    Error measure on Pr7, for method 4.

    Arguments:

    ``cell``
        The cell index (1-9) to define the error on.
    ``transformation``
        An optional transformation.
    ``cap_filter``
        Enable capacitance filtering (default: True)

    """
    def __init__(self, cell, transformation=None, cap_filter=True):
        super(E4, self).__init__(cell, [7], transformation, cap_filter)


class EAP(WholeTraceError):
    """
    Error measure on the AP signal, for independent validation.

    Arguments:

    ``cell``
        The cell index (1-9) to define the error on.
    ``transformation``
        An optional transformation.
    ``cap_filter``
        Enable capacitance filtering (default: True)

    """
    def __init__(self, cell, transformation=None, cap_filter=True):
        super(EAP, self).__init__(cell, [6], transformation, cap_filter)
