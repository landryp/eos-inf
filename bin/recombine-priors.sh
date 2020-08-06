#!/bin/bash

priorcsvpath=$1
numeos=$2
nummass=$3
chunksize=$4

chunksize=10000
chunks=$(($numeos/$chunksize))
if [ "$chunks" -eq "0" ]; then
	chunks=1
fi

suffix=$(printf "%06d" 0)
head -n 1 $priorcsvpath$suffix > $priorcsvpath

for i in $(seq 0 $(($chunks-1)))
do
	suffix=$(printf "%06d" $i)
	tail -n +2 $priorcsvpath$suffix >> $priorcsvpath
	rm $priorcsvpath$suffix
done

chunksize=$((100*$nummass))
numlines=$(wc -l < $priorcsvpath)
chunks=$(($(($numlines+$chunksize-1))/$chunksize))

tail -n +2 $priorcsvpath | split -d -l $chunksize -a 6 - $priorcsvpath
for i in $(seq 0 $(($chunks-1)))
do
	suffix=$(printf "%06d" $i)
	echo -e "$(head -n 1 $priorcsvpath)\n$(cat $priorcsvpath$suffix)" > $priorcsvpath$suffix
done

