#!/bin/bash
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
		cd $subDir/forestTrees

		genTrees
		cd ../../
	done
	cd ../
done


