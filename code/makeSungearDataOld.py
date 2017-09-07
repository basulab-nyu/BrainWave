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
stimuliNames = Config.get("sungear_analysis","stimulus_order").split(',')

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



def analyzeStimulus(stimulusData):
	cutoff = len(stimulusData)*cutoffCoef
	transposed = np.transpose(stimulusData).tolist()
	neuronValues = map(sum,transposed)
	stimulusSignficances = []
	for x in neuronValues:
		if x>=cutoff:
			stimulusSignficances.append(1)
		else:
			stimulusSignficances.append(0)
	
	return stimulusSignficances

for stimulus in stimuli:
	stimuli[stimulus]=analyzeStimulus(stimuli[stimulus])





#make anchors
anchors=[]
for stimulus in stimuliNames:
	anchors.append({'name' : stimulus})

with open(outputDirectory + 'sungearData/anchors.json', 'w') as outfile:
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
	expSets[stimulus] = listNeuronsSpiking(stimuli[stimulus])

with open(outputDirectory + 'sungearData/expSets.json', 'w') as outfile:
    json.dump(expSets, outfile)
outfile.close()



#Make items
items=[]
for n in range(len(stimuli[stimuli.keys()[0]])):
	items.append(
		{
		"species" : "ROI",
		"id" : str(n+1).rjust(3, '0'),
		"description" : "ROI "+ str(n+1)
		}
		)

with open(outputDirectory + 'sungearData/items.json', 'w') as outfile:
    json.dump(items, outfile)
outfile.close()


