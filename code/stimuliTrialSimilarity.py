print 'Stimuli Trial Similarity'
import os
import json
import re
import scipy.stats
import numpy as np
def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f


import numpy as np
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read('analysis.config')

f = open('compressedNormalData.txt', 'r')
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

def findSetsSize2(n):
	sets2 = []
	for x in range(n):
		for y in range(x):
			sets2.append([y, x])

	return sets2


stimuli={}
for stimulus in tempStimuli:
	stimuli[stimulus]=tempStimuli[stimulus]

def findSimilarityOfTrials(trial1, trial2):
	sims=0.
	total=0.
	for x in range(len(trial1)):
		if trial1[x]==trial2[x]:
			sims+=1.
		total+=1.
	return sims/total


def findSimilarityOfStimulus(stimulus):
	numTrials = len(stimulus)
	sets = findSetsSize2(numTrials)
	

	#trialSimilarities = map(lambda x: [x, findSimilarityOfTrials(stimulus[x[0]], stimulus[x[1]])], sets)
	trialSimilarities = map(lambda x: [x, scipy.stats.pearsonr(stimulus[x[0]], stimulus[x[1]])[0]], sets)

	
	return trialSimilarities


#print findSimilarityOfStimulus(stimuli['NoRunOdor2s180'])
#print findSimilarityOfStimulus(stimuli['NoRunBlankF180'])
def mergeTrials(stimulus):
	newStimulus = np.array(stimulus).transpose()
	newStimulus = map(lambda x: float(sum(x))/len(x), newStimulus)
	return newStimulus



baselineCorrelation =  scipy.stats.pearsonr(mergeTrials(stimuli['NoRunBlankF180']), mergeTrials(stimuli['NoRunOdor2s180']))[0]
print findSimilarityOfStimulus(stimuli['NoRunBlankF180'])
print findSimilarityOfStimulus(stimuli['NoRunOdor2s180'])

f = open('similarityOfTrialsInStimuli.txt', 'w')
f.write('baseline correlation: ' + str(baselineCorrelation) + '\n \n')
for stimulus in stimuli:
	f.write('Correlations of ' + stimulus + '\n')
	samples = []
	for combo in findSimilarityOfStimulus(stimuli[stimulus]):
		f.write(str(combo[0]) + ' : ' + str(combo[1])+ '\n')
		samples.append(combo[1])

	sampMean = float(sum(samples)) / len(samples)
	sampStdev = np.std(np.array(samples))
	f.write('mean for trial: ' + str(sampMean) + '\n')
	f.write('stdev for trial: ' + str(sampStdev) + '\n')
	z_score = (sampMean - baselineCorrelation)/ sampStdev
	f.write('z_score for trial ((mean - baseline)/stdev): ' + str(z_score) + '\n')


	f.write('\n')


f.close()


