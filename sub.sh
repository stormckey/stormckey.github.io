#! /bin/bash
source fmt.sh
set -x 
gs
ga
gc -m $1
gp
set +x
