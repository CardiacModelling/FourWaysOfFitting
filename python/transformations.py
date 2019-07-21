#!/usr/bin/env python3
#
# Parameter transformations
#
from __future__ import division, print_function
import numpy as np


class ATransformation(object):
    """
    Transforms from model to search space (and back), using log transforms on
    all "a" parameters.
    """

    def transform(self, parameters):
        """
        Transform from model into search space.
        """
        transformed_parameters = np.array(parameters, copy=True)
        transformed_parameters[0] = np.log(parameters[0])
        transformed_parameters[2] = np.log(parameters[2])
        transformed_parameters[4] = np.log(parameters[4])
        transformed_parameters[6] = np.log(parameters[6])
        return transformed_parameters

    def detransform(self, transformed_parameters):
        """
        Transform back from search space to model space.
        """
        parameters = np.array(transformed_parameters, copy=True)
        parameters[0] = np.exp(transformed_parameters[0])
        parameters[2] = np.exp(transformed_parameters[2])
        parameters[4] = np.exp(transformed_parameters[4])
        parameters[6] = np.exp(transformed_parameters[6])
        return parameters

    def code(self):
        """ Returns a one-letter code for this transform. """
        return 'a'

    def name(self):
        """ Returns a name for this transform. """
        return 'a-params only'


class KineticTransformation(object):
    """
    Transforms from model to search space (and back), using log transforms on
    all kinetic parameters -- but not on the conductance.
    """

    def transform(self, parameters):
        """
        Transform from model into search space.
        """
        transformed_parameters = np.array(parameters, copy=True)
        for i in range(8):
            transformed_parameters[i] = np.log(parameters[i])
        return transformed_parameters

    def detransform(self, transformed_parameters):
        """
        Transform back from search space to model space.
        """
        parameters = np.array(transformed_parameters, copy=True)
        for i in range(8):
            parameters[i] = np.exp(transformed_parameters[i])
        return parameters

    def code(self):
        """ Returns a one letter code for this transform. """
        return 'k'

    def name(self):
        """ Returns a name for this transform. """
        return 'kinetic'


class FullTransformation(object):
    """
    Transforms from model to search space (and back), using log transforms on
    the full set of parameters.
    """

    def transform(self, parameters):
        """
        Transform from model into search space.
        """
        return np.log(np.array(parameters))

    def detransform(self, transformed_parameters):
        """
        Transform back from search space to model space.
        """
        return np.exp(np.array(transformed_parameters))

    def code(self):
        """ Returns a one letter code for this transform. """
        return 'f'

    def name(self):
        """ Returns a name for this transform. """
        return 'full'


class NullTransformation(object):
    """
    Doesn't transform any parameters.
    """

    def transform(self, parameters):
        """
        Transform from model into search space.
        """
        return parameters

    def detransform(self, transformed_parameters):
        """
        Transform back from search space to model space.
        """
        return transformed_parameters

    def code(self):
        """ Returns a one letter code for this transform. """
        return 'n'

    def name(self):
        """ Returns a name for this transform. """
        return 'untransformed'


codes = {
    'a': ATransformation,
    'f': FullTransformation,
    'k': KineticTransformation,
    'n': NullTransformation,
}


def create(code):
    try:
        meth = codes[code]
    except KeyError:
        raise ValueError('Unknown transformation code ' + str(code))
    return meth()

