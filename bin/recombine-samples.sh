#!/bin/bash

priorcsvpath=$1
postpath=$2
nummass=$3

chunksize=$((1*nummass))
numlines=$(wc -l < $priorcsvpath)
chunks=$(($numlines/$chunksize))

suffix=$(printf "%06d" 0)
head -n 1 $priorcsvpath$suffix > $postpath

for i in $(seq 0 $(($chunks-1)))
do
	suffix=$(printf "%06d" $i)
	tail -n +2 $priorcsvpath$suffix >> $postpath
	rm $priorcsvpath$suffix
done
