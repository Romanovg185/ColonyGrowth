#!/bin/bash

#PBS -l nodes=1:ppn=1

FOLDER="np=3_9"

for h in 500 1000 1500 2000 2500 3000 3500
do
	for i in {3..8}
	do
		FILELOC="$FOLDER/"
		cd "/home/rvangenderen/Workspace/Results/$FILELOC"	
		python /home/rvangenderen/Workspace/Results/Image_Export.py "result$i.txt" $h
	done
done
