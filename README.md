# brain-regions-analysis

Possible new name for tool: Brain Wave
*** means it needs edits.


This is a software package meant for analyzing data collected from processing the brain. It allows researchers to look into the effects of stimuli on different regions of the brain and allows researchers to find spatial relationships between the ROIs. Finish explanation.*********

The data needs to incorporate events from multiple ROIs. It also needs the coordinates of the ROIs. The final type of data needed is a list of excluded ROIs. This is necessary for every dataset.

Here is how to run the code:
**********
Go into the code directory.

The code is written in python 2.7.11 and Mathematica.

Mathematica should be added to your bash profile with this line:

alias wolfram='/Applications/Mathematica.app/Contents/MacOS/MathKernel'

Mathematica scripts will then be run with:
wolfram -script filename.wl

Python should have necessary dependences installed with pip.

Python scripts should be run with:
python filename.py

To run all of the python scripts, run:
python fullPythonAnalysis.py

To run all of the Mathematica scripts, run:
wolfram -script fullMathematicaAnalysis.wl

To run everything:
bash fullAnalysis.sh

To control which dataset you're running the analysis on, change the filename in currentDataset.txt.

The first script that must be run is:
python createExperimentAnalysis.py

***********
Here is an explanation of the uses of each script. Sometimes you may want to run them indvidually. If you do, they should typically be run in order.

createExperimentAnalysis.py
Generates the output directories for each dataset.

getData.py:
This file contains two useful functions. They are used by other scripts to get raw data and to check what the current dataset in currentdataset.txt is.

makeMathematicaConfig.py
This file converts the analysis.config file to a txt file that can be read by Mathematica.

These files implement a difference of means shuffle test to find the significance of activity after the stimulus.

analyzeNormal.py
This file uses shuffle test to binarize the raw data. If after the stimulus is applied, the ROI sees statistically signficant increases or decreases in ***change in flourescence over baseline flourescence***, it is assigned either a 1 or -1 respectively. If there is no signficant change in flourescence, the ROI is assigned a 0.  

analyzeN.py
This file is similar to analyzeNormal.py. The difference is it maintains the temporal aspect of the data. Rather than simply assigning a 1, 0, or -1 to indicate the significance overall, it assigns those values to small groups of n frames. It then shows if small groups of frames have a mean value significantly different from the mean before. 

mergeNormalToOneFile.py
This file merges the significance results of analyzeNormal.py to one file.

mergePValsToOneFile.py
This file merges the p-value results of analyzeNormal.py to one file.

averageTrials.py
It provides proportions of trials signficantly active.

proportion_of_trials_spiking_in.py
Prepares the data to generate pie charts in the place of each neuron. It will show which trials each neuron was signficantly active in.

machineLearningParser.py
parses the data for machine learning (classification of what stimulus causes activity).

trainModel.py
trains and evaluates machine learning model on machine learning data

makeHistogramData.py
generates the proportion of neurons signficantly active over time for histograms for each trial

neuronCorrelationAnalysis.py
generates the correlation values between every neuron combination

neuronSimilarityAnalysis.py
the same as correlation analysis, but with different definition of similarity. It's defined by the number of times the value is the same in the same time frame in each neuron

correlationToDistance.py
generates plots of correlation values to distances

similarityToDistance.py
generates plots of similarity values to distances

neuronCorrelationRanker.py
ranks the correlations

intersectionAnalysis.py
identifies intersections of neurons through trials

makeSungearData.py
parses data for sungear

********
Mathematica codes

histograms.wl
generates histograms that correspond to histograms.py output

makeMovies.wl
makes movies of signficant changes in fluorscence over time

pieNeurons.wl
makes visualizations of signficant changes in fluorscence over time by representing neurons with pie charts

proportion_of_trials_spiking.wl
makes visualizations of which trials neurons were significantly changing in. The plots look exactly like pieNeurons plots. NOTICE THE DIFFERENCE







