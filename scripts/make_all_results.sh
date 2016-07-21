#!/bin/bash
# Script to concatenate result files split by chromosome together.

tissue=$1
allResults=$2
alpha=$3
i=0
for resultsfile in $(ls ../data/intermediate/model_by_chr/working_TW_${tissue}_exp_10-foldCV_elasticNet_alpha${alpha}_1KG_snps_chr*); do
        if [ $i -eq 0 ] ; then
                head -n 1 $resultsfile > $allResults
                i=1
        fi
        tail -n +2 $resultsfile >> $allResults
done
