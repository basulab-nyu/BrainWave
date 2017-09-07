print 'similarity to distance histograms'
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import os

def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

distanceBinSize = 50

originalFiles=map(lambda x: x.rpartition('.')[0],listdir_nohidden('neuronSimilarityAnalysis'))

def getSimilarities(location):
	f = open(location+'.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)
	data=data[1:]
	data=map(lambda x: 
			map(lambda y: 
				y.strip()
			,x.strip().split(','))[:5]
		,data)

	return data

def getLocations():
	f = open('data/neuronLocations/centers.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)
	data=map(lambda x: 
			map(lambda y: 
				float(y.strip())
			,x.strip().split('\t'))
		,data)

	return data

def euclidDistance(pt1,pt2):
	return np.linalg.norm(np.array(pt1)-np.array(pt2))



neuronLocations=getLocations()

def createPlot(name):	
	similarities = getSimilarities('neuronSimilarityAnalysis/'+name)

	for x in range(len(similarities)):
		similarities[x][0]=int(similarities[x][0])
		similarities[x][1]=int(similarities[x][1])
		similarities[x][2]=int(similarities[x][2])
		similarities[x][3]=float(similarities[x][3])
		similarities[x][4]=float(similarities[x][4])

	distanceToSimilarities={}
	maxDistance=0
	for simil in similarities:
		neuron1=simil[0]
		neuron2=simil[1]
		shift=simil[2]
		similarity=simil[3]
		distance=euclidDistance(neuronLocations[neuron1-1],neuronLocations[neuron2-1])
		percentile=simil[4]
		if distance>maxDistance:
			maxDistance=distance
		try:
			distanceToSimilarities[shift]=distanceToSimilarities[shift]+[[distance,similarity]]

		except (KeyError, AttributeError) as e:
			distanceToSimilarities[shift]=[]
			distanceToSimilarities[shift]=distanceToSimilarities[shift]+[[distance,similarity]]

	def makeHistogram(key):
		distanceBinsKeys = range(0, int(maxDistance) + distanceBinSize, distanceBinSize)
		distanceBins={}
		for x in distanceBinsKeys:
			distanceBins[x] = []

		data=distanceToSimilarities[key]
		for point in data:
			distanceBins[int(round(point[0]/float(distanceBinSize))*distanceBinSize)] = distanceBins[int(round(point[0]/float(distanceBinSize))*distanceBinSize)] + [point[1]]
		
		histogramValues=[]
		for x in distanceBinsKeys:
			numTerms=len(distanceBins[x])
			if numTerms==0:
				histogramValues.append([0,0])
			else:
				histogramValues.append([sum(distanceBins[x])/numTerms,numTerms])

		means,lengths=np.array(histogramValues).transpose().tolist()
		print means
		print lengths
		ind = np.arange(len(means))  # the x locations for the groups
		width = 0.35       # the width of the bars

		fig, ax = plt.subplots()
		rects1 = ax.bar(ind, (np.array(means)*10000).tolist(), width, color='r')

	
		rects2 = ax.bar(ind + width, lengths, width, color='y')

		# add some text for labels, title and axes ticks

		ax.set_xticks(ind)
		ax.set_xticklabels(distanceBinsKeys)

		ax.legend((rects1[0], rects2[0]), ('means*10000', 'lengths'))



		plt.savefig('similarityToDistanceHistograms/' + name + 'Shift' + str(shift) + '.pdf')
		plt.close()




	for shift in distanceToSimilarities:
		makeHistogram(shift)





for file in originalFiles:
	createPlot(file)




