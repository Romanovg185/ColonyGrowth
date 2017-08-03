#!/bin/bash
PATHNAME="/home/romano/Desktop/TADA/ColonyGrowth-master/Torsion_Spring"
FILENAME="my_result"
mkdir $PATHNAME/Results/$FILENAME
for h in 0
do
    FOLDERNAME="$PATHNAME/Results/$FILENAME"
    mkdir $FOLDERNAME/$h
    for ar in 3 4
    do
    	echo $FOLDERNAME/$i
  	    mkdir $FOLDERNAME/$h/$ar
        cp $PATHNAME/* $FOLDERNAME/$h/$ar/
        cd $FOLDERNAME/$h/$ar
        pwd
        ./build -o my.out -std=gnu++11 -O3
        sed -i "s/PATH/$FOLDERNAME/" run_on_cluster.sh
        sed -i "s/NUMBER/$ar/" run_on_cluster.sh
        sed -i "s/DIGIT/$ar/" run_on_cluster.sh
        qsub run_on_cluster.sh
    done
done

