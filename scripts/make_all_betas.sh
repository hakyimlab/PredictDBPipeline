#!/bin/bash
# Script to concatenate beta files split by chromosome together.

tissue=$1
allBetas=$2
alpha=$3
i=0
for betafile in $(ls ../data/intermediate/model_by_chr/TW_${tissue}_elasticNet_alpha${alpha}_1KG_snps_weights_chr*); do
	if [ $i -eq 0 ] ; then
		head -n 1 $betafile > $allBetas
		i=1
	fi
	tail -n +2 $betafile >> $allBetas
done

