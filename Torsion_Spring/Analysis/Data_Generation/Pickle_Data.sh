#!/bin/bash

#PBS -l nodes=1
cd $PBS_O_WORKDIR
PYTHONPATH=$(which python)

$PYTHONPATH /home/rvangenderen/Workspace/Results/SCRIPTNAME NUMBER
