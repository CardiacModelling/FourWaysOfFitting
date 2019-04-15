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
    #
    # Guesses for lower conductance
    #
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


def access_resistance(cell):
    """
    Returns the
    """
    # Cell 1
    # Access resistance    (Ra) = 4.7 MOhms
    # Cell 2
    # Access resistance    (Ra) = 4.0 MOhms
    # Cell 3
    # Access resistance    (Ra) = 6.9 MOhms
    # Cell 4
    # 220 megaohms series resistance compensation
    # Cell 5
    # Access resistance    (Ra) = 33.1 MOhms
    # Cell 6
    # Access resistance    (Ra) = 4.2 MOhms
    # Cell 7
    # Access resistance    (Ra) = 38.2 MOhms
    # Cell 8
    # Access resistance    (Ra) = 56.2 MOhms
    # Cell 9
    # Access resistance    (Ra) = 53.8 MOhms

