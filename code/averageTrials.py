#this script averages and merges exportingN trials

print 'average and merge trials'
import os
import numpy as np
import scipy.stats
import itertools
import ConfigParser
import random
import getData
import math
Config = ConfigParser.ConfigParser()

#gets current dataset
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'


def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

#CAN USE THE RAW DATA FOR RAW CORRELATION TO DISTANCE IN ANOTHER ANALYSIS
stimuliNames = map(lambda x: x.rpartition('.')[0],listdir_nohidden(rawDataDirectory + 'stimuliData'))
rawData = getData.getRawData(dataset, stimuliNames[0])

#get number of neurons
number_of_neurons = len(rawData)


def getOutputData(location):
	f = open(outputDirectory + 'exportingN/' + location + '.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)

	data = map(lambda x: 
			 map(lambda y: 
				float(y.strip())
			 ,x.strip().split(','))
		,data)

	return data


files = map(lambda x: x.rpartition('.')[0].split('_'), listdir_nohidden(outputDirectory + 'exportingN'))


stimuliData={}
for file in files:
	try:
		stimuliData[file[0]] = stimuliData[file[0]] + [getOutputData(file[0] + '_' + file[1])]
	except KeyError:
		stimuliData[file[0]]=[]
		stimuliData[file[0]] = stimuliData[file[0]] + [getOutputData(file[0] + '_' + file[1])]

#Now take the means of the parts in stimuli data.



def mergeStimulus(trials):
	mergedStimulus = (reduce(lambda x,y: x+y, map(np.array, trials)) / len(trials)).tolist()
	return mergedStimulus


for name in stimuliData:
	stimuliData[name]=mergeStimulus(stimuliData[name])


#write to mergedExportingN

def writeFile(name):
	data = stimuliData[name]
	f=open(outputDirectory + 'mergedExportingN/' + name + '.txt','w')
	for line in data:
		f.write(str(line)[1:-1]+'\n')
	f.close()

for name in stimuliData:
	writeFile(name)









