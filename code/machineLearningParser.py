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


trainingData = []
testData = []
#75% for training, 25% for testing
trainingAmount = .75
testingAmount = .25
random.seed(101)
def separateData(stimulusName):
	stimulusData = stimuli[stimulusName]
	#random.shuffle(stimulusData)
	for trial in stimulusData[:int(trainingAmount*len(stimulusData))]:
		trainingData.append([stimulusName] + map(float,trial))
	
	for trial in stimulusData[int(trainingAmount*len(stimulusData)):]:
		testData.append([stimulusName] + map(float,trial))



for stimulus in stimuli:
	separateData(stimulus)
random.seed(29292)
random.shuffle(trainingData)
random.shuffle(testData)



f = open(outputDirectory + 'trainingData.txt' , 'w')
for line in trainingData:
	f.write(str(line)[1:-1] + '\n')
f.close()

f = open(outputDirectory + 'testData.txt', 'w')
for line in testData:
	f.write(str(line)[1:-1] + '\n')
f.close()



