from __future__ import print_function
import numpy as np
import pandas as pd
from pylab import rcParams
import matplotlib.pyplot as plt

rcParams['figure.figsize'] = (13, 6)

import nilmtk
from nilmtk import DataSet, TimeFrame, MeterGroup, HDFDataStore
from nilmtk.legacy.disaggregate import CombinatorialOptimisation
from nilmtk.utils import print_dict
from nilmtk.metrics import f1_score

data = DataSet('data/AMPds2.h5')
print('Loaded', len(data.buildings), 'buildings')

elec = data.buildings[1].elec
elec.get_timeframe()

data.set_window(start='2012-04-23', end='2012-04-24')
elec_1 = data.buildings[1].elec

mains=elec_1.mains()
submeters=elec_1.submeters()
mains.available_ac_types('power')

from nilmtk.legacy.disaggregate.fhmm_exact import FHMM
from nilmtk.disaggregate.combinatorial_optimisation import CO
#need params for "non-legacy" algorithms - needs further investigation
from nilmtk.legacy.disaggregate.hart_85 import Hart85

h = FHMM()

h.train(submeters)

output = HDFDataStore('output.h5', 'w')
df = h.disaggregate(submeters, output)

df.tail()
h.best_matched_appliance(submeters, df)