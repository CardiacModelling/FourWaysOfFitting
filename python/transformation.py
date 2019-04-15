#!/usr/bin/env python3
#
# Parameter transformations
#
from __future__ import division, print_function
import numpy as np


class Transformation(object):
    """
    Transforms from model to search space (and back).
    """

    def transform(self, parameters):
        """
        Transform from model into search space.
        """
        return np.array([
            np.log(parameters[0]),
            parameters[1],
            np.log(parameters[2]),
            parameters[3],
            np.log(parameters[4]),
            parameters[5],
            np.log(parameters[6]),
            parameters[7],
            # Conductance
            parameters[8],
        ])

    def detransform(self, transformed_parameters):
        """
        Transform back from search space to model space.
        """
        return np.array([
            np.exp(transformed_parameters[0]),
            transformed_parameters[1],
            np.exp(transformed_parameters[2]),
            transformed_parameters[3],
            np.exp(transformed_parameters[4]),
            transformed_parameters[5],
            np.exp(transformed_parameters[6]),
            transformed_parameters[7],
            # Conductance
            transformed_parameters[8],
        ])


class TransformationNoConductance(object):
    """
    Transforms from model to search space (and back).
    """

    def transform(self, parameters):
        """
        Transform from model into search space.
        """
        return np.array([
            np.log(parameters[0]),
            parameters[1],
            np.log(parameters[2]),
            parameters[3],
            np.log(parameters[4]),
            parameters[5],
            np.log(parameters[6]),
            parameters[7],
        ])

    def detransform(self, transformed_parameters):
        """
        Transform back from search space to model space.
        """
        return np.array([
            np.exp(transformed_parameters[0]),
            transformed_parameters[1],
            np.exp(transformed_parameters[2]),
            transformed_parameters[3],
            np.exp(transformed_parameters[4]),
            transformed_parameters[5],
            np.exp(transformed_parameters[6]),
            transformed_parameters[7],
        ])

