#!/bin/bash

eosbank=$1
priorpath=$2
obstype=$3
numeos=$4
nummass=$5
mbounds=$6

sample-priors $eosbank $priorpath -O $obstype -n $numeos -N $nummass -m $mbounds
