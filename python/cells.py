#!/usr/bin/env python3
#
# Cell based data and functions
#
from __future__ import division
import numpy as np


def lower_conductance(cell):
    """
    Returns a lower limit for the conductance of the cell with the
    given integer index ``cell``.
    """
    # Map synthetic data to cell 5
    if cell > 9:
        cell = 5

    # Guesses for lower conductance, from Beattie et al.
    lower_conductances = {
        1: 0.0478,  # 16713003
        2: 0.0255,  # 16715049
        3: 0.0417,  # 16708016
        4: 0.0305,  # 16708060
        5: 0.0612,  # 16713110
        6: 0.0170,  # 16708118
        7: 0.0886,  # 16704007
        8: 0.0434,  # 16704047
        9: 0.0203,  # 16707014
    }
    return lower_conductances[cell]


def reversal_potential(temperature):
    """
    Calculates the reversal potential for Potassium ions, using Nernst's
    equation for a given ``temperature`` in degrees celsius and the internal
    and external [K]+ concentrations used in the experiments.
    """
    T = 273.15 + temperature
    F = 96485
    R = 8314
    K_i = 130
    k_o = 4
    return ((R*T)/F) * np.log(k_o/K_i)


def temperature(cell):
    """
    Returns the temperature (in degrees Celsius) for the given integer index
    ``cell``.
    """
    # Map synthetic data to cell 5
    if cell > 9:
        cell = 5

    temperatures = {
        1: 21.3,    # 16713003
        2: 21.4,    # 16715049
        3: 21.8,    # 16708016
        4: 21.7,    # 16708060
        5: 21.4,    # 16713110
        6: 21.7,    # 16708118
        7: 21.2,    # 16704007
        8: 21.6,    # 16704047
        9: 21.4,    # 16707014
    }
    return temperatures[cell]
