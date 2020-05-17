#!/bin/bash

likepath=$1
priorcsvpath=$2
postpath=$3
props=$4
bw=$5

if test -f "$priorcsvpath"; then
	if [ "$props" == "m R" ]; then
		weigh-samples $likepath $priorcsvpath $postpath $props -v --bandwidth=$bw --weight-column Prior --weight-column-is-log Prior --invert-weight-column Prior
	elif [ "$props" == "m1 m2 Lambda1 Lambda2" ]; then
		weigh-samples $likepath $priorcsvpath $postpath $props -v --bandwidth=$bw --weight-column Prior --weight-column-is-log Prior --invert-weight-column Prior --reflect --column-range Lambda1 0 5000 --column-range Lambda2 0 5000 --prune
	elif [ "$props" == "m" ]; then
		cumweigh-samples $likepath $priorcsvpath $postpath "m" "Mmax" 0.1 3.5 -v
	else
		weigh-samples $likepath $priorcsvpath $postpath $props -v --bandwidth=$bw
	fi
else
	echo "$priorcsvpath does not exist!"
fi
