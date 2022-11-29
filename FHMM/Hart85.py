from __future__ import division, print_function
import os
import matplotlib.pyplot as plt
from nilmtk.metrics import f1_score
import numpy as np
import pandas as pd
from matplotlib import rcParams
from nilmtk import DataSet, HDFDataStore, MeterGroup, TimeFrame
from nilmtk.legacy.disaggregate.hart_85 import Hart85
from six import iteritems

rcParams['figure.figsize'] = (13, 6)

train_data = DataSet('SeniorDataset/h5_files/Hart_test_12Hour.h5')

#set the training data to a 4-hour window
# train_data.set_window(start='1970-01-01T01', end='1970-01-01T05')
train_elec = train_data.buildings[1].elec

test_data = DataSet('SeniorDataset/h5_files/Hart_test_12Hour.h5')

#set the test data to a different 4-hour window
# test_data.set_window(start='1970-01-01T05', end='1970-01-01T09')
test_elec = test_data.buildings[1].elec

hart = Hart85()

hart.train(train_elec.submeters(), columns=[('power', 'apparent')])

df_mains = next(test_elec.mains().load())
df_mains.plot()
plt.legend(["Aggregate"]);
plt.ylabel("Power (W)")
plt.xlabel("Time")
plt.savefig("Output/hart_aggregate")
plt.close()

output = HDFDataStore('Output/output.h5', 'w')
df = hart.disaggregate(test_elec.mains(), output, sample_period=1)
output.close()
# print(test_elec.submeters())
# print(hart.best_matched_appliance(test_elec.submeters(), df))

df_appliance = next(test_elec['fridge', 1].load())
merged_df = pd.merge(df[0], df_appliance, left_index=True, right_index=True)

predictions_data = DataSet('Output/output.h5')
predictions_metergroup = predictions_data.buildings[1].elec

print(f1_score(predictions_metergroup, test_elec))
#fridge highest at 0.878, everything else below 0.2

# merged_df[0].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_fridge")
# plt.close()

# df_appliance = next(test_elec['kettle', 1].load())
# merged_df = pd.merge(df[1], df_appliance, left_index=True, right_index=True)

# merged_df[1].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_kettle")
# plt.close()

# df_appliance = next(test_elec['computer', 1].load())
# merged_df = pd.merge(df[2], df_appliance, left_index=True, right_index=True)

# merged_df[2].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_computer")
# plt.close()

# df_appliance = next(test_elec['microwave', 1].load())
# merged_df = pd.merge(df[3], df_appliance, left_index=True, right_index=True)

# merged_df[3].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_microwave")
# plt.close()

# df_appliance = next(test_elec['toaster', 1].load())
# merged_df = pd.merge(df[4], df_appliance, left_index=True, right_index=True)

# merged_df[4].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_toaster")
# plt.close()

# df_appliance = next(test_elec['hair dryer', 1].load())
# merged_df = pd.merge(df[5], df_appliance, left_index=True, right_index=True)

# merged_df[5].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_hair_dryer")
# plt.close()

# df_appliance = next(test_elec['slow cooker', 1].load())
# merged_df = pd.merge(df[6], df_appliance, left_index=True, right_index=True)

# merged_df[6].plot(c='r')
# merged_df['power', 'apparent'].plot()
# plt.legend(["Predicted", "Ground truth"]);
# plt.ylabel("Power (W)")
# plt.xlabel("Time")
# plt.savefig("Output/hart_slow_cooker")
# plt.close()