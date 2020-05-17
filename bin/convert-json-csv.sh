#!/bin/bash

priorpath=$1
priorcsvpath=$2

convert-json-csv $priorpath $priorcsvpath

rm $priorpath

