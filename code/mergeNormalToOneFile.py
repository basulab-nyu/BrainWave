print 'mergeNormalToOneFile'
#This file merges the trials for normal data into one file. 
import getData
import os
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

stimuliNames = map(lambda x: x.rpartition('.')[0], listdir_nohidden(outputDirectory + 'exportingNormal'))

#this is a different getData function
def getOutputData(location):
	f = open(location+'.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)


	data=data[0].strip()
	data=data.split(',')
	data=map(int,data)
	return data

#formats data so it is of format: stimulus, trial #, significance values
fullData=[]
temp=[]
stimuliNames = sorted(sorted(stimuliNames, key= lambda x: int(x.split('_')[1])), key= lambda x: x.split('_')[0])
for stimulus in stimuliNames:
	temp  = getOutputData(outputDirectory + "exportingNormal/" + stimulus)
	fullData.append([stimulus.split('_')[0], int(stimulus.split('_')[-1])] + temp)

#this function writes the data
def writeFile(data):
	f = open(outputDirectory + "compressedNormalData.txt", "w")
	for stimulus in data:
		f.write(str(stimulus)[1:-1]+'\n')
	f.close()

writeFile(fullData)

