#machineLearningParser
#separate into test and training data

print 'parse for machine learning'
import os
import re
import numpy as np
import getData
import random


#get name of dataset to work with
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read(rawDataDirectory + 'analysis.config')
stimuliNames = getData.getStimuliNames()

f = open(outputDirectory + 'compressedNormalData.txt', 'r')
data=[]
for line in f:
    data.append(line)
f.close()

data = map(lambda x: map(lambda y:y.strip().replace("'","").replace("_","") ,x.strip().split(',')), data)

number_of_stimuli = len(data)
stimuli={}

for name in stimuliNames:
	stimuli[name] =[]

for x in range(len(data)):
	temp = stimuli[data[x][0]]
	temp.append(data[x][2:])
	stimuli[data[x][0]] = temp[:]

for stimulus in stimuli:
	stimuli[stimulus] = map(lambda x: map(int,x), np.array(stimuli[stimulus]).transpose().tolist())

for stimulus in stimuli:
	f = open(outputDirectory + 'proportion_of_trials_spiking/' + stimulus + '.txt', 'w')
	for line in stimuli[stimulus]:
		f.write(str(line)[1:-1] + '\n')
	f.close()