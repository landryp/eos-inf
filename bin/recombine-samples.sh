#!/bin/bash

priorcsvpath=$1
postpath=$2
nummass=$3

chunksize=$((100*$nummass))
numlines=$(wc -l < $priorcsvpath)
chunks=$(($numlines/$chunksize))

suffix=$(printf "%06d" 0)
head -n 1 $postpath$suffix > $postpath

for i in $(seq 0 $chunks)
do
	suffix=$(printf "%06d" $i)
	tail -n +2 $postpath$suffix >> $postpath
	rm $priorcsvpath$suffix
	rm $postpath$suffix
done
