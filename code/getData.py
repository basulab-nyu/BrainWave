#this is a module for pulling in raw data
import os
def getCurrentDataset():
	f=open('../currentDataset.txt','r')
	return f.read()


#define function
def getRawData(dataset, stimuli):
	#make connection to the raw data file in the specified dataset with the specified stimuli
	f = open('../datasets/' + getCurrentDataset() + '/stimuliData/' + stimuli + '.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)

	
	data=map(lambda x: 
			map(lambda y: 
				float(y.strip())
			,x.strip().split('\t'))
		,data)	

	
	return data


def getStimuliNames():
	dir = '../datasets/' + getCurrentDataset() + '/stimuliData/'
	def listdir_nohidden(path):
		for f in os.listdir(path):
	         if not f.startswith('.'):
				if not f.endswith('p'):
					yield f

	#gets all raw data files from within raw data directory. The files each represent a stimulus.
	stimuliNames = map(lambda x: x.rpartition('.')[0], listdir_nohidden(dir))
	return stimuliNames

