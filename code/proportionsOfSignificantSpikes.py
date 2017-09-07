print 'proportions of significant spikes'
import os
import numpy as np
import scipy.stats
import itertools
import ConfigParser
import random
import math
import getData
Config = ConfigParser.ConfigParser()
Config.read('analysis.config')
number_of_shuffles = int(Config.get("analysis","number_of_shuffles_for_correlation_analysis"))



def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

#get number of neurons
originalFiles=map(lambda x: x.rpartition('.')[0],listdir_nohidden('data/stimuliData'))
originalData=getData.getOriginalData('data/stimuliData/'+originalFiles[0])
number_of_neurons=len(originalData)

files=map(lambda x: x.rpartition('.')[0],listdir_nohidden('exportingN'))


def getData(location):
	f = open(location+'.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)

	data=map(lambda x: 
			map(lambda y: 
				y.strip()
			,x.strip()
			.split(','))
		,data)

	return data
#Include exclusions
def getExclusions():
	f = open('data/exclusions/excludedROI.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)
	
	data = map(int, data[0].split('\t'))
	data = map(lambda x: x-1, data)
	return data


exclusions = getExclusions()
def getProportions(location):
	flatten = lambda l: [item for sublist in l for item in sublist]
	fullData = getData(location)
	newData = []
	for x in range(len(fullData)):
		if x not in exclusions:
			newData.append(fullData[x])
	data = flatten(newData)
	proportions = {-1 : data.count('-1'), 0 : data.count('0'), 1 : data.count('1')}
	proportions['total'] = proportions[-1] + proportions[0] + proportions[1]
	return proportions

def addToDictionary(dicter, newIndex, newElement):
	dicter[newIndex] = newElement
	return dicter

stimuli = {}
for name in files:
	tempNameList = name.split('_')
	tempNameList[1] = int(tempNameList[1])
	try:
		stimuli[tempNameList[0]] = addToDictionary(stimuli[tempNameList[0]], tempNameList[1], getProportions('exportingN/' + name))
	except KeyError:
		stimuli[tempNameList[0]] = {}
		stimuli[tempNameList[0]] = addToDictionary(stimuli[tempNameList[0]], tempNameList[1], getProportions('exportingN/' + name))



def analyzeProportions(stimulus, significanceToBeAnalyzed):
	data = stimuli[stimulus]
	def analyzeTrialProportions(dicter):
		return float(dicter[significanceToBeAnalyzed]) / dicter['total']

	proportions = {}
	for trial in data:
		proportions[trial] = analyzeTrialProportions(data[trial])

	return proportions

proportionsNegative = {}
proportionsPositive = {}
for stimulus in stimuli:
	proportionsNegative[stimulus] = analyzeProportions(stimulus, -1)
	proportionsPositive[stimulus] = analyzeProportions(stimulus, 1)

def mean(l):
	return float(sum(l)) / len(l)

def writePositiveProportions():
	
	f.write('Proportions of Positive Spikes For Different Stimuli\n')
	for stimulus in proportionsPositive:
		f.write(stimulus + '\n')
		tempData = proportionsPositive[stimulus]
		tempTrials = []
		for trial in tempData:
			tempTrials.append(tempData[trial])

		tempMean = mean(tempTrials)
		tempStdev = np.std(np.array(tempTrials))
		f.write('mean: ' + str(tempMean) + '\n')
		f.write('stdev: ' + str(tempStdev) + '\n')
		for trial in tempData:
			f.write('trial ' + str(trial) + ' proportion: ' + str(tempData[trial]) + '\n')
		f.write('\n')

def writeNegativeProportions():
	
	f.write('Proportions of Negative Spikes For Different Stimuli\n')
	for stimulus in proportionsNegative:
		f.write(stimulus + '\n')
		tempData = proportionsNegative[stimulus]
		tempTrials = []
		for trial in tempData:
			tempTrials.append(tempData[trial])

		tempMean = mean(tempTrials)
		tempStdev = np.std(np.array(tempTrials))
		f.write('mean: ' + str(tempMean) + '\n')
		f.write('stdev: ' + str(tempStdev) + '\n')
		for trial in tempData:
			f.write('trial ' + str(trial) + ' proportion: ' + str(tempData[trial]) + '\n')
		f.write('\n')



f = open('proportionsOfSignificantSpikes.txt', 'w')
writePositiveProportions()
f.write('\n \n')
writeNegativeProportions()
f.close()












