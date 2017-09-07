print 'makeHistogramData'
import numpy as np
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


stimuliNames = map(lambda x: x.rpartition('.')[0],listdir_nohidden(outputDirectory + 'exportingN'))

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
		
def writeFile(location,data):
	f = open(location+".txt", "w")
	f.write(str(data)[1:-1])
	f.close()


fullData=[]
temp=[]
for stimulus in stimuliNames:
	
	temp=getData(outputDirectory + "exportingN/" + stimulus)
	tempPositive = map(lambda x:
			map(lambda y: 0 if y==-1 else y,x),
		temp)
	tempNegative = map(lambda x:
			map(lambda y: 0 if y==1 else y,x),
		temp)


	newDataPositive=map(lambda x: sum(x) / len(x), (np.transpose(tempPositive)).tolist())
	newDataNegative=map(lambda x: -1* sum(x) / len(x), (np.transpose(tempNegative)).tolist())

	writeFile(outputDirectory + "histogramData/" + stimulus + "Positive", newDataPositive)
	writeFile(outputDirectory + "histogramData/" + stimulus + "Negative", newDataNegative)



