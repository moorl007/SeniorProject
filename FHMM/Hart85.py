from __future__ import division, print_function
import os
import matplotlib.pyplot as plt
import nilmtk.utils
import numpy as np
import pandas as pd
from matplotlib import rcParams
from nilmtk import DataSet, HDFDataStore, MeterGroup, TimeFrame
from nilmtk.legacy.disaggregate.hart_85 import Hart85
from six import iteritems

rcParams['figure.figsize'] = (13, 6)

train_data = DataSet('SeniorDataset/h5_files/test.h5')
test_data = DataSet('SeniorDataset/h5_files/test.h5')

# train_data.set_window(start='2013-01-05', end='2013-01-06')
train_elec_1 = train_data.buildings[1].elec
# train_data.set_window(start='2013-02-05', end='2013-02-06')
# train_elec_2 = train_data.buildings[1].elec
# test_data.set_window(start='2012-04-27', end='2012-04-28')
# train_elec_3 = train_data.buildings[1].elec
# test_data.set_window(start='2012-05-01', end='2012-05-02')
# train_elec_4 = train_data.buildings[1].elec
# test_data.set_window(start='2012-05-03', end='2012-05-04')
# train_elec_5 = train_data.buildings[1].elec
# test_data.set_window(start='2013-01-06', end='2013-01-07')
test_elec = test_data.buildings[1].elec

hart = Hart85()

train_elec = train_elec_1.submeters()

hart.train(train_elec, columns=[('power', 'apparent')])

# df_mains = next(test_elec.mains().load())
# df_mains.plot()
# plt.legend(["Aggregate"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_aggregate")
# plt.close()

output = HDFDataStore('Output/output.h5', 'w')
df = hart.disaggregate(test_elec.mains(), output, sample_period=1)

submeters = test_elec.submeters()

print(hart.best_matched_appliance(submeters, df))

# df_appliance = next(test_elec['fridge', 1].load())
# merged_df = pd.merge(df[0], df_appliance, left_index=True, right_index=True)

# merged_df[0].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_fridge")
# plt.close()

# df_appliance = next(test_elec['hair dryer', 1].load())
# merged_df = pd.merge(df[0], df_appliance, left_index=True, right_index=True)

# merged_df[0].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_hair_dryer")
# plt.close()

# df_appliance = next(test_elec['microwave', 1].load())
# merged_df = pd.merge(df[0], df_appliance, left_index=True, right_index=True)

# merged_df[0].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_microwave")
# plt.close()

# df_appliance = next(test_elec['hair dryer', 1].load())
# merged_df = pd.merge(df[0], df_appliance, left_index=True, right_index=True)

# merged_df[0].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_hair_dryer")
# plt.close()

# df_appliance = next(test_elec['computer', 1].load())
# merged_df = pd.merge(df[0], df_appliance, left_index=True, right_index=True)

# merged_df[0].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_computer")
# plt.close()

# df_appliance = next(test_elec['kettle', 1].load())
# merged_df = pd.merge(df[0], df_appliance, left_index=True, right_index=True)

# merged_df[0].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_kettle")
# plt.close()

# df_appliance = next(test_elec['toaster', 1].load())
# merged_df = pd.merge(df[0], df_appliance, left_index=True, right_index=True)

# merged_df[0].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_toaster")
# plt.close()