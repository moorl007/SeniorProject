import numpy as np
import pandas as pd
from nilm_metadata import convert_yaml_to_hdf5
from nilmtk import DataSet
from nilmtk.measurement import LEVEL_NAMES
import matplotlib.pyplot as plt

number = 60
keys = ['/building1/elec/meter1', '/building1/elec/meter2', '/building1/elec/meter3', '/building1/elec/meter4', '/building1/elec/meter5', '/building1/elec/meter6', '/building1/elec/meter7']
# keys = ['/96Hour_' + str(number) + 'Second/meter1', '/96Hour_' + str(number) + 'Second/meter2', '/96Hour_' + str(number) + 'Second/meter3', '/96Hour_' + str(number) + 'Second/meter4', '/96Hour_' + str(number) + 'Second/meter5', '/96Hour_' + str(number) + 'Second/meter6', '/96Hour_' + str(number) + 'Second/meter7']
pathBeg = 'SeniorDataset'

powerdata_filename = 'SeniorDataset/h5_files/96Hour_' + str(number) + 'Second.h5'
metadata_dir = 'SeniorDataset/metadata'

for count, key in enumerate(keys):
    df = pd.read_csv(pathBeg+key+'.csv', low_memory=False, dtype={'a': np.float32}, header=[0, 1], index_col=0)
    df.index = pd.to_datetime(df.index, unit='s', utc=True)
    df.columns.names = LEVEL_NAMES

    if(count == 0):
        # delete the existing h5 file before adding new appliances
        df.to_hdf(powerdata_filename, key=key, mode='w', format='table')
    else:
        df.to_hdf(powerdata_filename, key=key, mode='a', format='table')
    del df

convert_yaml_to_hdf5(metadata_dir, powerdata_filename) #will append metadata to hdf5 file

# data = DataSet(powerdata_filename)
# print(data.buildings[1].elec.mains())
# print(data.buildings[1].elec.submeters()['toaster'])

# test_elec = data.buildings[1].elec

# df_fridge = next(test_elec['toaster'].load())
# df_fridge.plot()
# plt.savefig('test')

# next(data.buildings[1].elec.mains().load()).plot()
# plt.savefig('test')
# plt.close()

# next(data.buildings[1].elec['toaster'].load()).plot()
# plt.savefig('test')
# plt.close()

# # Save to HDF5
# df.to_hdf(filename, 'data', mode='w', format='table')
# del df    # allow df to be garbage collected

# # Append more data
# df2 = pd.DataFrame(np.arange(10).reshape((5,2))*10, columns=['A', 'B'])
# df2.to_hdf(filename, 'data', append=True)