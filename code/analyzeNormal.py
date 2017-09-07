print 'analyzeNormal'
import getData
import random
import os
import ConfigParser

#get name of dataset to work with
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'




#reads through config file and takes out settings
Config = ConfigParser.ConfigParser()
Config.read(rawDataDirectory + 'analysis.config')
NUMSHUFFLES = int(Config.get("analysis","number_of_shuffles"))
THRESH = float(Config.get("analysis","threshold"))




def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

#gets all raw data files from within raw data directory. The files each represent a stimulus.
stimuliNames = map(lambda x: x.rpartition('.')[0],listdir_nohidden(rawDataDirectory + 'stimuliData'))

#takes some more data from the config file
numberOfFramesPerTrial=int(Config.get("analysis","total_number_of_frames_in_trial")) #It is 401 instead of 400 because the middle frame must be ignored.
NUMFRAMESBEFORE=int(Config.get("analysis","number_of_frames_before"))
NUMFRAMESAFTER=int(Config.get("analysis","number_of_frames_after"))

#mean function
def mean(list):
	return float(sum(list))/len(list)

#performs the analysis for an individual trial
def analyzeTrial(stimulusName, data,trialNum):
	#needs number of frames per trial
	#analyzes individual neurons in each trial
	def analyzeNeuron(frames):
		#makes sure that the values are above a certain threshold at some point in the time series
		maxValue = max(frames)
		if maxValue < THRESH:
			return 0., 0. 
		
		#finds the actual difference between means of before and after	
		realDiffMean=mean(frames[-NUMFRAMESAFTER:]) - mean(frames[:NUMFRAMESBEFORE])
		#makes a copy of the frames
		tempFrames=frames[:]
		#these are counters that count the number of times the randomly shuffled difference is above or below the real one
		numOver=0.
		numBelow=0.
		for x in range(NUMSHUFFLES):
			random.shuffle(tempFrames)
			tempBefore = tempFrames[:NUMFRAMESBEFORE]
			tempAfter = tempFrames[-NUMFRAMESAFTER:]
			tempDiffMean = mean(tempAfter) - mean(tempBefore)
			
			if realDiffMean > tempDiffMean:
				numOver += 1.
			elif realDiffMean < tempDiffMean:
				numBelow += 1.
		
		#these values are 1 - the p value. They tell us if the changes in fluorescence are signficant or not.
		return numOver / NUMSHUFFLES, numBelow / NUMSHUFFLES
		
	#makes a list of p values for each ROI in the stimulus
	pvalsBelow = []
	pvalsOver = []
	for neuron in data: 
		tempValOver, tempValBelow = analyzeNeuron(neuron)
		pvalsBelow.append(1-tempValBelow)
		pvalsOver.append(1-tempValOver)

	#makes a list of 1,0, -1 to indicate signficance of 
	significantChanges = []
	for x in range(len(pvalsBelow)):
		if pvalsOver[x] < .05:
			significantChanges.append(1)
		elif pvalsBelow[x] < .05:
			significantChanges.append(-1)
		else:
			significantChanges.append(0)

	
	#writes the significance data to a file
	def writeSignificantChanges(data):
		f = open(outputDirectory + "exportingNormal/" + stimulusName + "_" + str(trialNum+1) + ".txt", "w")
		f.write(str(data)[1:-1] + "\n")
		f.close()

	writeSignificantChanges(significantChanges)

	#writes pvals to a file
	def writePVals(pValsOver, pValsBelow):
		f = open(outputDirectory + "exportingPValuesPositiveSignificance/" + stimulusName + "_" + str(trialNum+1)+".txt", "w")
		f.write(str(pValsOver)[1:-1] + "\n")
		f.close()
		f = open(outputDirectory + "exportingPValuesNegativeSignificance/" + stimulusName + "_" + str(trialNum+1)+".txt", "w")
		f.write(str(pValsBelow)[1:-1] + "\n")
		f.close()

	writePVals(pvalsOver, pvalsBelow)
	
#analyzes the entire stimulus and breaks it up into individual trials
def analyzeStimulus(stimulusName):
	data=getData.getRawData(dataset, stimulusName)
	trials=[]
	trialNum= len(data[0]) / numberOfFramesPerTrial
	for x in range(trialNum):
		trials.append(map(lambda neuron: neuron[x*numberOfFramesPerTrial:(x+1)*numberOfFramesPerTrial],data))

	for t in range(len(trials)):
		analyzeTrial(stimulusName,trials[t],t)

#analyzes every stimulus
for name in stimuliNames:
	analyzeStimulus(name)

	