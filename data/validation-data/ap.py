#!/usr/bin/env python
import myokit
import myokit.formats.axon as axon

# log = myokit.DataLog.load('ap.zip')  # Load myokit DataLog
log = myokit.DataLog.load_csv('ap.csv')  # Import CSV as datalog

import numpy as np
log['time'] = np.round(log['time'], 10)

axon.save_atf(log, 'ap.atf')

