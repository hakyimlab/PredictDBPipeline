#!/bin/bash
# Script to concatenate log files split by chromosome together.

tissue=$1
allLogs=$2
i=0
for logfile in $(ls ../data/intermediate/model_by_chr/${tissue}_chr*log.txt); do
        if [ $i -eq 0 ] ; then
                head -n 1 $logfile > $allLogs
                i=1
        fi
        tail -n +2 $logfile >> $allLogs
done
