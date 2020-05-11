#!/bin/bash

postpath=$1
eospath=$2

marginalize-samples $postpath eos -o $eospath --weight-column logweight --weight-column-is-log logweight -v
