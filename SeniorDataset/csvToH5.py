import numpy as np
import pandas as pd
from nilm_metadata import convert_yaml_to_hdf5
from nilmtk import DataSet
from nilmtk.measurement import LEVEL_NAMES
import matplotlib.pyplot as plt

keys = ['/building1/elec/meter1', '/building1/elec/converted_fridge(11-16)', '/building1/elec/converted_hairDryer(11-15)', '/building1/elec/converted_kettle(11-16)', '/building1/elec/converted_laptop(11-15)', '/building1/elec/converted_microwave(11-15)', '/building1/elec/converted_toaster(11-16)']
pathBeg = 'SeniorDataset'

powerdata_filename = 'SeniorDataset/h5_files/Zeb_test.h5'
metadata_dir = 'SeniorDataset/metadata'

for key in keys:
    df = pd.read_csv(pathBeg+key+'.csv', low_memory=False, dtype=np.float32, header=[0,1])
    df.to_hdf(powerdata_filename, key=key, mode='a', format='table')
    del df

convert_yaml_to_hdf5(metadata_dir, powerdata_filename) #will append metadata to hdf5 file

data = DataSet(powerdata_filename)
# print(data.buildings[1].elec.mains())
# print(data.buildings[1].elec.submeters()['toaster'])

# # Save to HDF5
# df.to_hdf(filename, 'data', mode='w', format='table')
# del df    # allow df to be garbage collected

# # Append more data
# df2 = pd.DataFrame(np.arange(10).reshape((5,2))*10, columns=['A', 'B'])
# df2.to_hdf(filename, 'data', append=True)