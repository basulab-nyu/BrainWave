import numpy as np
import getData
import random
from sklearn import ensemble
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import getData
import itertools
import os
import subprocess

dataset = getData.getCurrentDataset()

#get name of dataset to work with
dataset = getData.getCurrentDataset()
stimuliNames = getData.getStimuliNames()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'


stimuliNamesKey = {}
for x in range(len(stimuliNames)):
	stimuliNamesKey[stimuliNames[x]] = x

inv_StimuliNamesKey = {v: k for k, v in stimuliNamesKey.iteritems()}

stimuliCombos = []
for i in range(2,len(stimuliNames) + 1):
	stimuliCombos += list(itertools.combinations(range(len(stimuliNames)), i))

f = open(rawDataDirectory + 'centers.txt', 'r')
rawCenters = f.read()
f.close()
centers = np.array(map(lambda x: 
			map(float,x.strip().split('\t')),
		  rawCenters.strip().split('\n'))).transpose().tolist()
		
f = open(outputDirectory + 'trainingData.txt', 'r')
trainingData=[]
for line in f:
    trainingData.append(line.strip().split(','))
f.close()

f = open(outputDirectory + 'testData.txt', 'r')
testData=[]
for line in f:
    testData.append(line.strip().split(','))
f.close()


trainingDataX = []
trainingDataY = []
for sample in trainingData:
	trainingDataX.append(map(float,sample[1:]))
	trainingDataY.append(stimuliNamesKey[sample[0][1:-1]])

testDataX = []
testDataY = []
for sample in testData:
	testDataX.append(map(float,sample[1:]))
	testDataY.append(stimuliNamesKey[sample[0][1:-1]])

def makeModel(numbersForNames):
	tempTrainingDataX = []
	tempTrainingDataY = []
	tempTestDataX = []
	tempTestDataY = []

	for i in range(len(trainingDataX)):
		if trainingDataY[i] in numbersForNames:
			tempTrainingDataX.append(trainingDataX[i])
			tempTrainingDataY.append(trainingDataY[i])

	for i in range(len(testDataX)):
		if testDataY[i] in numbersForNames:
			tempTestDataX.append(testDataX[i])
			tempTestDataY.append(testDataY[i])


	forest = ensemble.RandomForestClassifier(n_estimators=200, max_features='auto', max_depth=15 , random_state=1999)

	forest.fit(tempTrainingDataX,tempTrainingDataY)



	try:
		os.mkdir(outputDirectory + 'modelInformation/' + str(len(numbersForNames))+ 'stimuli')
	except:
		pass

	namesForNumbers = []
	for number in numbersForNames:
		namesForNumbers.append(inv_StimuliNamesKey[number])

	tempDir = outputDirectory + 'modelInformation/' + str(len(numbersForNames))+ 'stimuli/' + '_'.join(namesForNumbers) + '/'
	try:
		os.mkdir(tempDir)
	except:
		pass

	try:
		os.mkdir(tempDir + 'forestTrees')
	except:
		pass


	from sklearn import tree
	i_tree = 0
	for tree_in_forest in forest.estimators_:

	    with open(tempDir + 'forestTrees/tree_' + str(i_tree) + '.dot', 'w') as my_file:
	        my_file = tree.export_graphviz(tree_in_forest, out_file = my_file)
	    i_tree = i_tree + 1

	forestScore = forest.score(tempTestDataX,tempTestDataY)

	forestImportances = forest.feature_importances_.tolist()
	f = open(tempDir + 'forestROIimportances.txt', 'w')
	f.write(str(forestImportances)[1:-1])
	f.close()

	estimator = DecisionTreeClassifier(max_leaf_nodes=10, random_state=0)
	estimator.fit(tempTrainingDataX,tempTrainingDataY)
	with open(tempDir + 'decisionTree.dot', 'w') as my_file:
	    my_file = tree.export_graphviz(tree_in_forest, out_file = my_file)

	estimatorImportances = estimator.feature_importances_.tolist()
	f = open(tempDir + 'estimatorROIimportances.txt', 'w')
	f.write(str(estimatorImportances)[1:-1])
	f.close()

	estimatorScore = estimator.score(tempTestDataX,tempTestDataY)
	f = open(tempDir + 'scores.txt', 'w')
	f.write('forest score:' + str(forestScore) + '\ndecision tree score:' + str(estimatorScore))
	f.close()

	forestImportancesColors = []
	thresh = np.mean(forestImportances)
	for val in forestImportances:
		if val > thresh:
			forestImportancesColors.append('r')
		else:
			forestImportancesColors.append('k')
	plt.scatter(centers[0], centers[1], c = forestImportancesColors)
	#plt.show()
	#exit()
	plt.savefig(tempDir + 'ROIimportances.pdf')
	plt.close()


map(makeModel, stimuliCombos)

bashScript = """#!/bin/bash
#this script requires graphviz to be installed
cd ../

currentDataset=$(<currentDataset.txt)
#echo "$currentDataset"
cd analyzedDatasets/$currentDataset/modelInformation/



function genTrees {
	
		i=0
		for f in *.dot
		do
		   dot -Tpdf tree_$i.dot -o tree_$i.pdf
		   ((i=i+1))
		done
	
}

for dir in *
do
	cd $dir
	for subDir in *
	do
		cd $subDir
		dot -Tpdf decisionTree.dot -o decisionTree.pdf
		cd forestTrees

		genTrees
		cd ../../
	done
	cd ../
done
"""

subprocess.check_output(['bash','-c', bashScript])

