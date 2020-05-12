#!/bin/bash

likepath=$1
priorcsvpath=$2
postpath=$3
props=$4
bw=$5

if test -f "$priorcsvpath"; then
	weigh-samples $likepath $priorcsvpath $postpath $props -v --bandwidth=$bw --weight-column Prior --weight-column-is-log Prior --invert-weight-column Prior
else
	echo "$priorcsvpath does not exist!"
fi
