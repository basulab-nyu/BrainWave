print 'neuron correlation ranker'
import os
import numpy as np
import scipy.stats
import itertools
import ConfigParser
import random
import math
import getData
#get name of dataset to work with
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'



Config = ConfigParser.ConfigParser()
Config.read(rawDataDirectory + 'analysis.config')
number_of_shuffles = int(Config.get("analysis", "number_of_shuffles_for_correlation_analysis"))



def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

#get number of neurons
originalFiles = map(lambda x: x.rpartition('.')[0],listdir_nohidden(rawDataDirectory + 'stimuliData'))
originalData = getData.getRawData(dataset, originalFiles[0])
number_of_neurons = len(originalData)


files=map(lambda x: x.rpartition('.')[0],listdir_nohidden(outputDirectory + 'exportingN'))


neuronCombinations=list(itertools.combinations(range(number_of_neurons),2))


def getData(location):
	f = open(location+'.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)

	data=map(lambda x: 
			map(lambda y: 
				float(y.strip())
			,x.strip().split(','))
		,data)

	return data

def analyzeStimulus(location):
	stimulusData = getData(location)
	def analyzeNeurons(data,neuronNum1,neuronNum2,delay):
		neuron1=data[neuronNum1]
		neuron2=data[neuronNum2]

		if delay>0:
			neuron1=neuron1[delay:]
			neuron2=neuron2[:-delay]
		elif delay<0:
			neuron1=neuron1[:delay]
			neuron2=neuron2[-delay:]

		neuron1 = map(float, neuron1)
		neuron2 = map(float, neuron2)

		correlationVal=scipy.stats.pearsonr(neuron1,neuron2)[0]
		tempCorVals=0
		tempNeuron2=neuron2[:]
		lessThanCounter=0.0
		

		
		return [neuronNum1+1,neuronNum2+1,delay,correlationVal]



	analyzedNeurons=[]
	for combo in neuronCombinations:
		for delay in range(-3,4):
			analyzedNeurons.append(analyzeNeurons(stimulusData,combo[0],combo[1],delay))
	
	for x in range(len(analyzedNeurons)):
		if math.isnan(analyzedNeurons[x][-1]):
			analyzedNeurons[x][-1]=0

	 
	analyzedNeuronsSorted = sorted(analyzedNeurons, key = lambda cor: cor[3])
	highPositiveCorrelations = analyzedNeuronsSorted[len(analyzedNeuronsSorted)*95/100:]
	highNegativeCorrelations = analyzedNeuronsSorted[0:len(analyzedNeuronsSorted)*5/100]
	
	return highPositiveCorrelations,highNegativeCorrelations



def writeFile(input_location,fileName):
	highPositiveCorrelations,highNegativeCorrelations = analyzeStimulus(input_location)
	
	highNegativeCorrelations.insert(0,['neuron','neuron','delay','correlation coefficient'])
	highPositiveCorrelations.append(['neuron','neuron','delay','correlation coefficient'])
	highPositiveCorrelations.reverse()
	f=open(outputDirectory + 'neuronCorrelationRankings/' + fileName + '_HighlyPositive.txt','w')
	for line in highPositiveCorrelations:
		f.write(str(line)[1:-1]+'\n')
	f.close()

	f=open(outputDirectory + 'neuronCorrelationRankings/' + fileName + '_HighlyNegative.txt','w')
	for line in highNegativeCorrelations:
		f.write(str(line)[1:-1]+'\n')
	f.close()

for file in files:
	writeFile(outputDirectory + 'exportingN/' + file, file)

