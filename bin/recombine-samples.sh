#!/bin/bash

priorcsvpath=$1
postpath=$2
nummass=$3
chunksize=$4

chunksize=$((100*$nummass))
numlines=$(wc -l < $priorcsvpath)
chunks=$(($numlines/$chunksize))

suffix=$(printf "%06d" 0)
head -n 1 $postpath$suffix > $postpath

for i in $(seq 0 $chunks)
do
	suffix=$(printf "%06d" $i)
	if test -f "$postpath$suffix"; then
		tail -n +2 $postpath$suffix >> $postpath
		rm $postpath$suffix
	fi
	rm $priorcsvpath$suffix
done
