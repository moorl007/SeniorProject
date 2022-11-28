import os
import numpy as np
import pandas as pd

# keys = ['/building1/elec/meter1', '/building1/elec/meter2', '/building1/elec/meter3', '/building1/elec/meter4', '/building1/elec/meter5']
keys = ['/building1/elec/meter1',
        '/building1/elec/meter2']
pathBeg = 'SeniorDataset'
pathEnd = '.csv'

# filename = 'SeniorDesign.h5'

count = 0
for key in keys:
    # if(count==1):
    #     break
    print(count)
    count += 1
    # df = pd.read_csv(pathBeg+key+pathEnd, low_memory=True, skiprows=1, dtype = {'timestamp': int, 'active': float})
    df = pd.read_csv(pathBeg+key+pathEnd, low_memory=True, skiprows=1)
    # df['timestamp'] = df['timestamp'].astype('datetime64[s]')
    # df.set_index('timestamp')
    # df = df.iloc[1: , :]
    # print(df.dtypes)
    print(df.head)
    # print()
    # print()
    # print(df.iloc[0])
    # print(df.iloc[0].timestamp)
    # print(df['timestamp'].dtype)
    np.datetime64(int(df.iloc[0].timestamp), 's')
    # print(np.datetime64(int(df.iloc[0].timestamp), 's'))
    newList = []
    newPower = []
    for i in range(len(df)):
        addition = np.datetime64(int(df.iloc[i].timestamp), 's')
        power = df.iloc[i].active * 1000
        # print(addition)
        newList.append(addition)
        newPower.append(power)
    df['newDates'] = newList
    df['newPower'] = newPower
    df.set_index('newDates', inplace=True, drop=True)
    # df.drop(columns=['timestamp','active'])
    # df.drop('active')
    del df['timestamp']
    del df['active']
    # df = df[['newDates', 'active']]
    # print(df)
    df.to_csv('outputTest.csv')
    # print(os.getcwd())
print('done')