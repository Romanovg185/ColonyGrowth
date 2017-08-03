#!/bin/bash
PATHNAME="/home/rvangenderen/Workspace/"
FILENAME="my_result"
for h in 0 1 2 3 4 5 6 7 8 9
do
    FOLDERNAME="$PATHNAME/Results/$FILENAME/$h"
    mkdir $FOLDERNAME
    for ar in 3 4 5 6 7 8
    do
  	    mkdir $FOLDERNAME/$i/
        cp $PATHNAME/* $FOLDERNAME/$ar/
        cd /home/rvangenderen/Workspace/Results/$FOLDERNAME/$ar
        ./build -o my.out -std=gnu++11 -O3
        sed -i "s/PATH/$FOLDERNAME/" run_on_cluster.sh
        sed -i "s/NUMBER/$ar/" run_on_cluster.sh
        sed -i "s/DIGIT/$ar/" run_on_cluster.sh
        qsub run_on_cluster.sh
    done
done

