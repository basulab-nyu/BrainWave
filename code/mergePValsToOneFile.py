print 'mergePValsToOneFile'
#This file merges the trials for pvalue data into one file.
import getData
import os
def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'


stimuliNames = map(lambda x: x.rpartition('.')[0], listdir_nohidden(outputDirectory + 'exportingPValuesPositiveSignificance'))
stimuliNames = sorted(sorted(stimuliNames, key= lambda x: int(x.split('_')[1])), key= lambda x: x.split('_')[0])

#this is a different getData function
def getOutputData(location):
	f = open(location+'.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)

	data=data[0].strip()
	data=data.split(',')
	data=map(float,data)
	return data

		


positiveData=[]
temp=[]
for stimulus in stimuliNames:
	temp=getOutputData(outputDirectory + "exportingPValuesPositiveSignificance/" + stimulus)
	positiveData.append([stimulus[:-1], int(stimulus.split('_')[-1])] + temp)


negativeData=[]
temp=[]
for stimulus in stimuliNames:
	temp=getOutputData(outputDirectory + "exportingPValuesNegativeSignificance/" + stimulus)
	negativeData.append([stimulus[:-1],int(stimulus.split('_')[-1])]+temp)


def writeFile(data, significance):
	f = open(outputDirectory + "compressedPValues" + significance + "Significance.txt", "w")
	for stimulus in data:
		f.write(str(stimulus)[1:-1]+'\n')
	f.close()

writeFile(positiveData, 'Positive')
writeFile(negativeData, 'Negative')


