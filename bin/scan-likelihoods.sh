#!/bin/bash

likepath=$1
obstype=$2

echo "$likepath,$obstype" | scan-likelihoods /dev/stdin
