import numpy as np
import pandas as pd
from nilm_metadata import convert_yaml_to_hdf5
from nilmtk import DataSet
from nilmtk.measurement import LEVEL_NAMES
import matplotlib.pyplot as plt

# keys = ['/building5/elec/meter1', '/building5/elec/meter10', '/building5/elec/meter11', '/building5/elec/meter12', '/building5/elec/meter13', '/building5/elec/meter14', '/building5/elec/meter15', '/building5/elec/meter16', '/building5/elec/meter17', '/building5/elec/meter18', '/building5/elec/meter19', '/building5/elec/meter2', '/building5/elec/meter20', '/building5/elec/meter21', '/building5/elec/meter22', '/building5/elec/meter23', '/building5/elec/meter24', '/building5/elec/meter25', '/building5/elec/meter26', '/building5/elec/meter3', '/building5/elec/meter4', '/building5/elec/meter5', '/building5/elec/meter6', '/building5/elec/meter7', '/building5/elec/meter8', '/building5/elec/meter9', '/building4/elec/meter1', '/building4/elec/meter2', '/building4/elec/meter3', '/building4/elec/meter4', '/building4/elec/meter5', '/building4/elec/meter6', '/building3/elec/meter1', '/building3/elec/meter2', '/building3/elec/meter3', '/building3/elec/meter4', '/building3/elec/meter5', '/building2/elec/meter1', '/building2/elec/meter10', '/building2/elec/meter11', '/building2/elec/meter12', '/building2/elec/meter13', '/building2/elec/meter14', '/building2/elec/meter15', '/building2/elec/meter16', '/building2/elec/meter17', '/building2/elec/meter18', '/building2/elec/meter19', '/building2/elec/meter2', '/building2/elec/meter20', '/building2/elec/meter3', '/building2/elec/meter4', '/building2/elec/meter5', '/building2/elec/meter6', '/building2/elec/meter7', '/building2/elec/meter8', '/building2/elec/meter9', '/building1/elec/meter1', '/building1/elec/meter10', '/building1/elec/meter11', '/building1/elec/meter12', '/building1/elec/meter13', '/building1/elec/meter14', '/building1/elec/meter15', '/building1/elec/meter16', '/building1/elec/meter17', '/building1/elec/meter18', '/building1/elec/meter19', '/building1/elec/meter2', '/building1/elec/meter20', '/building1/elec/meter21', '/building1/elec/meter22', '/building1/elec/meter23', '/building1/elec/meter24', '/building1/elec/meter25', '/building1/elec/meter26', '/building1/elec/meter27', '/building1/elec/meter28', '/building1/elec/meter29', '/building1/elec/meter3', '/building1/elec/meter30', '/building1/elec/meter31', '/building1/elec/meter32', '/building1/elec/meter33', '/building1/elec/meter34', '/building1/elec/meter35', '/building1/elec/meter36', '/building1/elec/meter37', '/building1/elec/meter38', '/building1/elec/meter39', '/building1/elec/meter4', '/building1/elec/meter40', '/building1/elec/meter41', '/building1/elec/meter42', '/building1/elec/meter43', '/building1/elec/meter44', '/building1/elec/meter45', '/building1/elec/meter46', '/building1/elec/meter47', '/building1/elec/meter48', '/building1/elec/meter49', '/building1/elec/meter5', '/building1/elec/meter50', '/building1/elec/meter51', '/building1/elec/meter52', '/building1/elec/meter53', '/building1/elec/meter54', '/building1/elec/meter6', '/building1/elec/meter7', '/building1/elec/meter8', '/building1/elec/meter9']
keys = ['/building1/elec/meter1', '/building1/elec/meter2', '/building1/elec/meter3', '/building1/elec/meter4', '/building1/elec/meter5', '/building1/elec/meter6', '/building1/elec/meter7']
pathBeg = 'SeniorDataset'

powerdata_filename = 'SeniorDataset/h5_files/test.h5'
metadata_dir = 'SeniorDataset/metadata'

#IMPORTANT!!! NEED TO CONVERT DATA INTO WATTS FROM KILOWATTS
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