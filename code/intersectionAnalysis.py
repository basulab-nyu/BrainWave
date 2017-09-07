import numpy as np
import ConfigParser
import getData


#get name of dataset to work with
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'


Config = ConfigParser.ConfigParser()
Config.read(rawDataDirectory + 'analysis.config')
cutoffCoef = float(Config.get("intersection_analysis","percentage_of_trials_spiking_to_be_considered_signficant"))

f = open(outputDirectory + 'compressedNormalData.txt', 'r')
data=[]
for line in f:
    data.append(line)
f.close()

data = map(lambda x: map(lambda y:y.strip().replace("'","").replace("_","") ,x.strip().split(',')), data)

number_of_stimuli = len(data)

stimuli={}

for x in range(len(data)):

	try:
		temp=stimuli[data[x][0]]
		temp.append(map(int,data[x][2:]))
		stimuli[data[x][0]]=temp
	except (NameError, KeyError):
		stimuli[data[x][0]]=[map(int,data[x][2:])]





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

stimuliValues=[]
for stimulus in stimuli:
	stimuliValues.append(analyzeStimulus(stimuli[stimulus]))

number_of_stimuli = len(stimuliValues)

numberOfOccurences=map(sum,np.transpose(stimuliValues).tolist())


intersectedNeurons=[]
for x in range(len(numberOfOccurences)):
	if numberOfOccurences[x]==number_of_stimuli:
		intersectedNeurons.append(x+1)

f=open(outputDirectory + 'intersectedNeurons.txt','w')
f.write(str(intersectedNeurons)[1:-1])
f.close()



