#jon's commnet
import warnings; warnings.filterwarnings('ignore')

from nilmtk import DataSet
train = DataSet('ukdale.h5')
train.set_window(start="13-4-2013", end="14-4-2013")
train_elec = train.buildings[1].elec

from rnndisaggregator import RNNDisaggregator
rnn = RNNDisaggregator()

# train_mains = train_elec.mains().all_meters()[0] # The aggregated meter that provides the input
# train_meter = train_elec.submeters()['microwave'] # The microwave meter that is used as a training target
meter_key = 'kettle'
train_meter = train_elec.submeters()[meter_key]
train_mains = train_elec.mains()

rnn.train(train_mains, train_meter, epochs=1, sample_period=1)
rnn.export_model("model-ukdale.h5")

test = DataSet('ukdale.h5')
test.set_window(start="1-1-2014", end="2-1-2014")
test_elec = test.buildings[1].elec
# test_mains = test_elec.mains().all_meters()[0]
test_mains = test_elec.mains()

disag_filename = 'disag-out.h5' # The filename of the resulting datastore
from nilmtk.datastore import HDFDataStore
output = HDFDataStore(disag_filename, 'w')
# output.close()

# test_mains: The aggregated signal meter
# output: The output datastore
# train_meter: This is used in order to copy the metadata of the train meter into the datastore
rnn.disaggregate(test_mains, output, train_meter, sample_period=1)
output.close()
output = HDFDataStore(disag_filename, 'r')
result = DataSet(disag_filename)
res_elec = result.buildings[1].elec
predicted = res_elec['kettle']
ground_truth = test_elec['kettle']

import matplotlib.pyplot as plt
predicted.plot()
ground_truth.plot()

import metrics
rpaf = metrics.recall_precision_accuracy_f1(predicted, ground_truth)
print("============ Recall: {}".format(rpaf[0]))
print("============ Precision: {}".format(rpaf[1]))
print("============ Accuracy: {}".format(rpaf[2]))
print("============ F1 Score: {}".format(rpaf[3]))

print("============ Relative error in total energy: {}".format(metrics.relative_error_total_energy(predicted, ground_truth)))
print("============ Mean absolute error(in Watts): {}".format(metrics.mean_absolute_error(predicted, ground_truth)))
plt.show()