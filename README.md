# Electric Load Disaggregation at Varying Timescales
A Senior Project by Ben Moorlach, Brandon Gorter, Jon Skarda, Zach Xiong, and Zeb Zimmer

This project and the code described below requires a NILMTK environment which can be difficult to setup if unfamiliar with Anaconda Envrionments.
[NILMTK installation guide ](https://klemenjak.medium.com/a-step-by-step-manual-for-installing-nilmtk-bff86e3aa418) is a great resource that we used to set up our own envrioments.
The process, even with the guide, can be frustrating but the fuctions and premade algorithms that come from NILMTK are essential and are worth the effort.

.h5 files are used to save ML models, datasets, and prediction waveforms.  The ones present in the folders are not necessary for use and are products of the engineering process.
Their only use is to serve as an example if a user wants to run the code immediately. 

Each algorithm's implementation is reliant on the formation of the data.  A CSV of the form 
```csv
,power
,apparent
1640995201,2.0
1640995202,2.0
etc.
```
which is timestamp then energy value(we used apparent power:watts) can be converted with the csvToH5.py script found iin the SeniorDataset folder.  The naming conventions
for NILMTK is meter1.csv should be the aggregate waveform. meter2.csv, meter3.csv, etc. should be the individual waveforms and the metadata in SeniorDataset/metadata/building1.yaml
needs to be how it is shown in our file.  The applicances can change but need to match the data (meter3.csv for example) as this yaml file determines the labels.

A few csv to csv conversion scripts exist within the code to get a csv file ready for integration into an .h5 file.  Senior/Dataset/allCSV/updateCSV will take a single csv
file and convert it to the form shown above.  The timestamp should be consistent across all of the meter#.csv files.  Hence we used 1640995201 as our starting point which
is Jan 1, 2022.  

A better understanding of the Disaggregation problem and our proposed solution can be understood by reading (or skimming it's your life) the Final Report document.
There are a few decent graphs that should the desired output and one model of project's setup from an abstracted viewpoint.

## Folder Breakdown
### Combinatorial Optimization
This folder contains CO_Performance_Analysis.ipynb, which is a notebook file that was used to test another benchmark supervised algorithm called Combinatorial Optimization. This algorithm did not end up being used for our final product, but was part of our initial testing which helped us decide which algorithms to use.
### FHMM
FHMM_Performance_Analysis.ipynb is the only file of note here. It was used to test the FHMM method from NILMTK.  
### Hart Unsupervised
This folder contains all of the files used for testing the Hart Unsupervised algorithm. Hart_Performance_Analysis.ipynb was the main file used for performance analysis, while Hart85.py was used for testing purposes. The various output files are datastore files containing outputs from the performance testing.
### Output
A bunch of disaggregated waveforms.  The title of the photos shows where it came from except the labels in the photos are wrong. All pictures were at 1 second sampling frequency.
### SeniorDataset
The multitude of CSV files used for training and testing are stored here as well as the metadata and a few earlier-mentioned python scripts.  The original data collected 
is found in SeniorDataset/allCSV each in their own folder.  

NOTE: The following 96 hour files are not necessary as NILMTK has a scaling variable in the train function called sample_period which can be set to change the sampling frequency. 
These were used just to check and ensure that that feature worked as intended.
We used our data sampled at 1 second and then used this variable to test at other sampling rates to collect our data.

The original waveforms were used to synthetically create the 96HourCSV files.  96Hour_15Second is the original 
96HourCSV_Converted which is data taken at 1 second frequencies that has been transformed into 15 second frequencies by the SeniorDataset/allCSV/timeshift.py script
### neural-disaggregator
A failed attempt to get a properly-working recurrent neural network lies buried here.  In the RNN subfolder the RNN-test-notebook.ipynb was used to try and evalute the RNN.
This entire folder comes from [Gabriel Freeze's Neural Disaggregator github repo](https://github.com/GabrielFreeze/neural-disaggregator) and likely would work better than 
our other models if given more training data.

[Product Launch Video](https://youtu.be/h3MfLHuDVjE)

A final report summarizing and concluding the project is included in the repository.
