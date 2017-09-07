#this file makes a text file from the config file that can be parsed by Mathematica

print 'making mathematica config'
import ConfigParser
import os
import getData
#here it reads the config file
dataset = getData.getCurrentDataset()
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'
Config = ConfigParser.ConfigParser()
Config.read(rawDataDirectory + 'analysis.config')


def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

analysisOptions = Config.options("analysis")

#generate list of settings
analysisSettings = map(lambda option: option + ":" + Config.get('analysis', option), analysisOptions)


#add number of neurons
files=map(lambda x: x.rpartition('.')[0], listdir_nohidden(rawDataDirectory + 'stimuliData'))
data=getData.getRawData(dataset, files[0])
analysisSettings.append('number_of_neurons:' + str(len(data)))

#write file
f = open(outputDirectory + "mathematicaConfig.txt", "w")
for option in analysisSettings:
	f.write(option + '\n')
f.close()