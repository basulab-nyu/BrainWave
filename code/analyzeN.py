print 'analyzeN'
import getData
import random
import os
import ConfigParser
import random


#get name of dataset to work with
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'

#reads through config file and takes out settings
Config = ConfigParser.ConfigParser()
Config.read(rawDataDirectory + 'analysis.config')
NUMSHUFFLES = int(Config.get("analysis","number_of_shuffles"))
STEPSIZE = int(Config.get("analysis","group_size"))
THRESH = float(Config.get("analysis","threshold"))

def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

#gets all raw data files from within raw data directory. The files each represent a stimulus.
stimuliNames = map(lambda x: x.rpartition('.')[0], listdir_nohidden(rawDataDirectory + 'stimuliData'))

#takes some more data from the config file
numberOfFramesPerTrial = int(Config.get("analysis", "total_number_of_frames_in_trial")) 
NUMFRAMESBEFORE = int(Config.get("analysis", "number_of_frames_before"))
NUMFRAMESAFTER = int(Config.get("analysis", "number_of_frames_after"))

#mean function
def mean(list):
	return float(sum(list)) / len(list)

#function that returns a list of n zeroes
def zerolistmaker(n):
    return [0.] * n

#performs the analysis for an individual trial
def analyzeTrial(fileName, data, trialNum):
	#Needs numberOfFramesPerTrial frames. Should split up evenly.
	#analyzes individual neuron
	def analyzeNeuron(neuron):
		maxValue = max(neuron)
		if maxValue < THRESH:
			return [0] * (NUMFRAMESAFTER / STEPSIZE)

		realBefore = neuron[:NUMFRAMESBEFORE]
		realAfter = neuron[-NUMFRAMESAFTER:]
		realBeforeMean = mean(realBefore)
		realDiffMeans = []
		# calculates the real differences between means
		for x in range(0, NUMFRAMESAFTER, STEPSIZE):
			realDiffMeans.append(mean(realAfter[x : x + STEPSIZE]) - realBeforeMean)

		tempFrames = neuron[:]
		numOver = zerolistmaker(len(realDiffMeans))
		numBelow = zerolistmaker(len(realDiffMeans))
		# does it randomly and compares to the real
		for _ in range(NUMSHUFFLES):
			random.shuffle(tempFrames)
			tempBefore = tempFrames[:NUMFRAMESBEFORE]
			tempAfter = tempFrames[-NUMFRAMESAFTER:]
			tempBeforeMean = mean(tempBefore)
			tempDiff = []
			for x in range(0, NUMFRAMESAFTER, STEPSIZE): 	
				tempDiff.append(mean(tempAfter[x : x + STEPSIZE]) - tempBeforeMean)

			for x in range(len(realDiffMeans)):
				if realDiffMeans[x] > tempDiff[x]:
					numOver[x] += 1.
				elif realDiffMeans[x] < tempDiff[x]:
					numBelow[x] += 1.
		# evaluates significance of neuron at certain frames
		finalVals=[]
		for x in range(len(realDiffMeans)):
			if numOver[x] / NUMSHUFFLES > .95:
				finalVals.append(1)
			elif numBelow[x] / NUMSHUFFLES > .95:
				finalVals.append(-1)
			else:
				finalVals.append(0)
	
		return finalVals

	#runs analyze neuron on every neuron in the trial
	significantSpikes=[]
	for neuron in data:
		significantSpikes.append(analyzeNeuron(neuron))

	#outputs trial to a txt file
	def writeTrial(data):
		f = open(outputDirectory + "exportingN/" + fileName + "_" + str(trialNum+1) + ".txt", "w")
		for neuron in data:
			f.write(str(neuron)[1:-1] + "\n")
		f.close()

	writeTrial(significantSpikes)
	
#function for analyzing the trials within a stimulus
def analyzeStimulus(stimulusName):
	data = getData.getRawData(dataset, stimulusName)
	trials = []
	trialNum = len(data[0]) / numberOfFramesPerTrial


	for x in range(trialNum):
		trials.append(map(lambda neuron: neuron[x*numberOfFramesPerTrial:(x+1)*numberOfFramesPerTrial], data))

	for t in range(len(trials)):
		analyzeTrial(stimulusName, trials[t], t)

#analyzes each stimulus
for stimulus in stimuliNames:
	analyzeStimulus(stimulus)

