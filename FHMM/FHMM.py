from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
from nilmtk import DataSet, HDFDataStore, MeterGroup, TimeFrame
from nilmtk.legacy.disaggregate.fhmm_exact import FHMM
from nilmtk.legacy.disaggregate.combinatorial_optimisation import CombinatorialOptimisation
from six import iteritems
from nilmtk.metrics import f1_score

# def predict(clf, test_elec, list_of_appliances, sample_period, timezone):
#     pred = {}
#     gt= {}
    
#     # "ac_type" varies according to the dataset used. 
#     # Make sure to use the correct ac_type before using the default parameters in this code.    
#     for i, chunk in enumerate(test_elec.mains().load(physical_quantity = 'power', ac_type = 'apparent', sample_period=sample_period)):
#         chunk_drop_na = chunk.dropna()
#         pred[i] = clf.disaggregate_chunk(chunk_drop_na)
#         gt[i]={}

#         for appliance in list_of_appliances:
#             # Only use the meters that we trained on (this saves time!)
#             # gt[i][meter] = next(test_elec[meter].load(physical_quantity = 'power', ac_type = 'active', sample_period=sample_period))
    
#             gt[i][appliance] = next(test_elec[appliance].load(physical_quantity = 'power', ac_type = 'active', sample_period=sample_period))
#         gt[i] = pd.DataFrame({k:v.squeeze() for k,v in iteritems(gt[i]) if len(v)}, index=next(iter(gt[i].values())).index).dropna()
        

#         #FIX THIS FORMAT
#         # for meter in test_elec.submeters().meters:
#         #     # Only use the meters that we trained on (this saves time!)
#         #     # gt[i][meter] = next(test_elec[meter].load(physical_quantity = 'power', ac_type = 'active', sample_period=sample_period))
    
#         #     gt[i][meter] = next(meter.load(physical_quantity = 'power', ac_type = 'active', sample_period=sample_period))
#         # gt[i] = pd.DataFrame({k:v.squeeze() for k,v in iteritems(gt[i]) if len(v)}, index=next(iter(gt[i].values())).index).dropna()
        
#     # If everything can fit in memory
#     gt_overall = pd.concat(gt)
#     gt_overall.index = gt_overall.index.droplevel()
#     pred_overall = pd.concat(pred)
#     pred_overall.index = pred_overall.index.droplevel()

#     # print(pred_overall.columns)
#     # print(gt_overall.columns)
#     # print(pred_overall)

#     # Having the same order of columns
#     gt_overall = gt_overall[pred_overall.columns]
    
#     #Intersection of index
#     gt_index_utc = gt_overall.index.tz_convert("UTC")
#     pred_index_utc = pred_overall.index.tz_convert("UTC")
#     common_index_utc = gt_index_utc.intersection(pred_index_utc)
    
#     common_index_local = common_index_utc.tz_convert(timezone)
#     gt_overall = gt_overall.loc[common_index_local]
#     pred_overall = pred_overall.loc[common_index_local]
#     # appliance_labels = [m for m in gt_overall.columns.values]

#     return gt_overall, pred_overall

def predict(clf, test_elec, sample_period, timezone):
    pred = {}
    gt= {}
    
    # "ac_type" varies according to the dataset used. 
    # Make sure to use the correct ac_type before using the default parameters in this code.    
    for i, chunk in enumerate(test_elec.mains().load(physical_quantity = 'power', ac_type = 'apparent', sample_period=sample_period)):
        chunk_drop_na = chunk.dropna()
        pred[i] = clf.disaggregate_chunk(chunk_drop_na)
        gt[i]={}

        for meter in test_elec.submeters().meters:
            # Only use the meters that we trained on (this saves time!)    
            gt[i][meter] = next(meter.load(physical_quantity = 'power', ac_type = 'apparent', sample_period=sample_period))
        gt[i] = pd.DataFrame({k:v.squeeze() for k,v in iteritems(gt[i]) if len(v)}, index=next(iter(gt[i].values())).index).dropna()
        
    # If everything can fit in memory
    gt_overall = pd.concat(gt)
    gt_overall.index = gt_overall.index.droplevel()
    pred_overall = pd.concat(pred)
    pred_overall.index = pred_overall.index.droplevel()

    # Having the same order of columns
    gt_overall = gt_overall[pred_overall.columns]
    
    #Intersection of index
    gt_index_utc = gt_overall.index.tz_convert("UTC")
    pred_index_utc = pred_overall.index.tz_convert("UTC")
    common_index_utc = gt_index_utc.intersection(pred_index_utc)
    
    common_index_local = common_index_utc.tz_convert(timezone)
    gt_overall = gt_overall.loc[common_index_local]
    pred_overall = pred_overall.loc[common_index_local]
    appliance_labels = [m for m in gt_overall.columns.values]
    gt_overall.columns = appliance_labels
    pred_overall.columns = appliance_labels
    return gt_overall, pred_overall

rcParams['figure.figsize'] = (13, 6)

train_data = DataSet('SeniorDataset/h5_files/Hart_test_12Hour.h5')
test_data = DataSet('SeniorDataset/h5_files/Hart_test_12Hour.h5')

sample_period = 1
num_states_dict = {'fridge': 2, 'computer': 2, 'hair dryer': 2, 'kettle': 2, 'microwave': 2, 'toaster': 2, 'slow cooker': 2}
fhmm = FHMM()

train_elec = train_data.buildings[1].elec
test_elec = test_data.buildings[1].elec

fhmm.train(train_elec, num_states_dict=num_states_dict, physical_quantity='power', ac_type='apparent')

ground_truth, predictions = predict(fhmm, test_elec, sample_period, train_data.metadata['timezone'])

appliance_labels = [m.label() for m in ground_truth.columns.values]

ground_truth.columns = appliance_labels
predictions.columns = appliance_labels

print(f1_score(predictions, ground_truth))

predictions['Fridge'].plot(label="Pred")
ground_truth['Fridge'].plot(label="GT")
plt.legend()
plt.savefig('Output/fhmm_fridge')
plt.close()

predictions['Kettle'].plot(label="Pred")
ground_truth['Kettle'].plot(label="GT")
plt.legend()
plt.savefig('Output/fhmm_kettle')
plt.close()

predictions['Computer'].plot(label="Pred")
ground_truth['Computer'].plot(label="GT")
plt.legend()
plt.savefig('Output/fhmm_computer')
plt.close()

predictions['Microwave'].plot(label="Pred")
ground_truth['Microwave'].plot(label="GT")
plt.legend()
plt.savefig('Output/fhmm_microwave')
plt.close()

predictions['Toaster'].plot(label="Pred")
ground_truth['Toaster'].plot(label="GT")
plt.legend()
plt.savefig('Output/fhmm_toaster')
plt.close()

predictions['Hair dryer'].plot(label="Pred")
ground_truth['Hair dryer'].plot(label="GT")
plt.legend()
plt.savefig('Output/fhmm_hairdryer')
plt.close()

predictions['Slow cooker'].plot(label="Pred")
ground_truth['Slow cooker'].plot(label="GT")
plt.legend()
plt.savefig('Output/fhmm_slowcooker')
plt.close()