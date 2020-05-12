#!/bin/bash

priorpath=$1
priorcsvpath=$2
#nummass=$3

convert-json-csv $priorpath $priorcsvpath

#chunksize=$((100*$nummass))
#numlines=$(wc -l < $priorcsvpath)
#chunks=$(($numlines/$chunksize))
#echo $chunks
#tail -n +2 $priorcsvpath | split -d -l $chunksize -a 6 - $priorcsvpath
#for i in $(seq 0 $chunks)
#do
#	suffix=$(printf "%06d" $i)
#	echo $suffix
#	echo $(head -n 1 $priorcsvpath)
#	echo -e "$(head -n 1 $priorcsvpath)\n$(cat $priorcsvpath$suffix)" > $priorcsvpath$suffix
#done
