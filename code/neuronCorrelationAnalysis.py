print 'neuron correlation analysis'
import os
import numpy as np
import scipy.stats
import itertools
import ConfigParser
import random
import getData
import math
Config = ConfigParser.ConfigParser()
#get name of dataset to work with
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'



Config.read(rawDataDirectory + 'analysis.config')
number_of_shuffles = int(Config.get("analysis","number_of_shuffles_for_correlation_analysis"))


def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f


#get number of neurons
originalFiles=map(lambda x: x.rpartition('.')[0],listdir_nohidden(rawDataDirectory + 'stimuliData'))
originalData=getData.getRawData(dataset, originalFiles[0])
number_of_neurons=len(originalData)



stimuliNames = map(lambda x: x.rpartition('.')[0], listdir_nohidden(outputDirectory + 'mergedExportingN'))

#generates all of the combinations of two different neurons
neuronCombinations=list(itertools.combinations(range(number_of_neurons),2))


def getOutputData(location):
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
	stimulusData = getOutputData(location)
	def analyzeNeurons(data,neuronNum1,neuronNum2,delay):
		neuron1 = data[neuronNum1]
		neuron2 = data[neuronNum2]

		if delay>0:
			neuron1 = neuron1[delay:]
			neuron2 = neuron2[:-delay]
		elif delay<0:
			neuron1 = neuron1[:delay]
			neuron2 = neuron2[-delay:]

		neuron1 = map(float, neuron1)
		neuron2 = map(float, neuron2)

		correlationVal=scipy.stats.pearsonr(neuron1 + [0.], neuron2 + [0.])[0]
		tempCorVals=0
		tempNeuron2=neuron2[:]
		lessThanCounter=0.0
		

		if math.isnan(correlationVal):
			percentile=correlationVal

			significance=0
		else:
			for x in range(number_of_shuffles):
				random.shuffle(tempNeuron2)
				tempCorVal=scipy.stats.pearsonr(neuron1 + [0.],tempNeuron2 + [0.])[0]
				
				if tempCorVal<=correlationVal:
					lessThanCounter+=1.0

			
			percentile=lessThanCounter / number_of_shuffles
			if percentile < .05:
				significance = -1
			elif percentile > .95:
				significance = 1
			else:
				significance = 0



		return [neuronNum1 + 1, neuronNum2 + 1, delay, correlationVal, percentile, significance]



	analyzedNeurons=[]
	analyzedNeurons.append(['neuron1','neuron2','delay','correlation coefficient','percentile','significance'])
	for combo in neuronCombinations:
		for delay in range(-3,4):
			analyzedNeurons.append(analyzeNeurons(stimulusData,combo[0],combo[1],delay))

	return analyzedNeurons
	


def writeFile(input_location,fileName):
	data=analyzeStimulus(input_location)
	f=open(outputDirectory + 'neuronCorrelationAnalysis/' + fileName + '.txt','w')
	for line in data:
		f.write(str(line)[1:-1]+'\n')
	f.close()

for file in stimuliNames:
	#writeFile('exportingN/' + file, file)
	writeFile(outputDirectory + 'mergedExportingN/' + file, file)

