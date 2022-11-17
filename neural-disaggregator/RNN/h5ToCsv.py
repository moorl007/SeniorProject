#!/usr/bin/env python3

# to run
# python3 h5ToCsv.py ukdale.h5 > ukdale.csv
import pandas as pd
import sys
print('hello world')
fpath = sys.argv[1]
print(fpath)

print('printing hdf keys')


outpath = 'CSVFiles/UKDALE'
with pd.HDFStore(fpath, 'r') as hdf:
    # This prints a list of all group names:
    print(hdf.keys())
    print(len(hdf.keys()))
    count = 0
    for key in hdf.keys():  
        if(count == 1):
            break
        print(count) 
        df = pd.read_hdf(fpath, key=key)
        print(df.head)
        # df.astype({'physical_quantity'})
        # print(df.dtypes)
        df.to_csv(outpath+key+'.csv', index=True)
        count += 1