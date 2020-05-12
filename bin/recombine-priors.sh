#!/bin/bash

priorcsvpath=$1
numeos=$2
nummass=$3

chunksize=1000
chunks=$(($numeos/$chunksize)

suffix=$(printf "%06d" 0)
head -n 1 $priorcsvpath$suffix > $priorcsvpath

for i in $(seq 0 $chunks)
do
	suffix=$(printf "%06d" $i)
	tail -n +2 $priorcsvpath$suffix >> $priorcsvpath.tmp
	rm $priorcsvpath$suffix
done

eoslist=()
while IFS=, read -r eos other
do
	counts=$(grep -o "$eos" <<< ${eoslist[*]} | wc -l)
	if [ "$counts" -le $nummass ]; then
		echo "$eos,$other" >> $priorcsvpath
		adds+=("$eos")
	fi
done < $priorcsvpath.tmp

rm $priorcsvpath.tmp

