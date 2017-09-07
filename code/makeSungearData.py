print 'makeSungearData'
import os
import json
import re
import numpy as np
import getData
def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

#get name of dataset to work with
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'

import numpy as np
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read(rawDataDirectory + 'analysis.config')
cutoffCoef = float(Config.get("sungear_analysis","percentage_of_trials_spiking_to_be_considered_signficant"))
stimuliNames = map(lambda s: s.strip(), Config.get("sungear_analysis","stimulus_order").split(','))

f = open(outputDirectory + 'compressedNormalData.txt', 'r')
data=[]
for line in f:
    data.append(line)
f.close()

data=map(lambda x: map(lambda y:y.strip().replace("'","").replace("_","") ,x.strip().split(',')), data)

number_of_stimuli = len(data)

tempStimuli={}

for x in range(len(data)):

	try:
		temp=tempStimuli[data[x][0]]
		temp.append(map(int,data[x][2:]))
		tempStimuli[data[x][0]]=temp
	except (NameError, KeyError):
		tempStimuli[data[x][0]]=[map(int,data[x][2:])]


stimuli={}
for stimulus in stimuliNames:
	stimuli[stimulus]=tempStimuli[stimulus]



def analyzeStimulus(stimulusData, sign):
	cutoff = len(stimulusData) * cutoffCoef
	transposed = np.transpose(stimulusData).tolist()
	neuronValues = map(lambda l: l.count(sign), transposed)
	stimulusSignficances = []
	for x in neuronValues:
		if x >= cutoff:
			stimulusSignficances.append(1)
		else:
			stimulusSignficances.append(0)
	
	return stimulusSignficances

stimuliPositive = {}
stimuliNegative = {}
for stimulus in stimuli:
	stimuliPositive[stimulus]=analyzeStimulus(stimuli[stimulus], 1)
	stimuliNegative[stimulus]=analyzeStimulus(stimuli[stimulus], -1)




#POSITIVE
#make anchors
anchors=[]
for stimulus in stimuliNames:
	anchors.append({'name' : stimulus})

with open(outputDirectory + 'sungearData/anchorsPositive.json', 'w') as outfile:
    json.dump(anchors, outfile)
outfile.close()

#make expsets

def listNeuronsSpiking(neurons):
	spikingNeurons=[]
	for n in range(len(neurons)): 
		if neurons[n]==1:
			spikingNeurons.append(str(n+1).rjust(3, '0'))

	return spikingNeurons

expSets={}
for stimulus in stimuli:
	expSets[stimulus] = listNeuronsSpiking(stimuliPositive[stimulus])

with open(outputDirectory + 'sungearData/expSetsPositive.json', 'w') as outfile:
    json.dump(expSets, outfile)
outfile.close()



#Make items
items=[]
for n in range(len(stimuliPositive[stimuliPositive.keys()[0]])):
	items.append(
		{
		"species" : "ROI",
		"id" : str(n+1).rjust(3, '0'),
		"description" : "ROI "+ str(n+1)
		}
		)

with open(outputDirectory + 'sungearData/itemsPositive.json', 'w') as outfile:
    json.dump(items, outfile)
outfile.close()





#NEGATIVE
#make anchors
anchors=[]
for stimulus in stimuliNames:
	anchors.append({'name' : stimulus})

with open(outputDirectory + 'sungearData/anchorsNegative.json', 'w') as outfile:
    json.dump(anchors, outfile)
outfile.close()

#make expsets

def listNeuronsSpiking(neurons):
	spikingNeurons=[]
	for n in range(len(neurons)): 
		if neurons[n]==1:
			spikingNeurons.append(str(n+1).rjust(3, '0'))

	return spikingNeurons

expSets={}
for stimulus in stimuli:
	expSets[stimulus] = listNeuronsSpiking(stimuliNegative[stimulus])

with open(outputDirectory + 'sungearData/expSetsNegative.json', 'w') as outfile:
    json.dump(expSets, outfile)
outfile.close()



#Make items
items=[]
for n in range(len(stimuliNegative[stimuliNegative.keys()[0]])):
	items.append(
		{
		"species" : "ROI",
		"id" : str(n+1).rjust(3, '0'),
		"description" : "ROI "+ str(n+1)
		}
		)

with open(outputDirectory + 'sungearData/itemsNegative.json', 'w') as outfile:
    json.dump(items, outfile)
outfile.close()
