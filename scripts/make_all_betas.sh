#!/bin/bash
# Script to concatenate beta files split by chromosome together.

allBetas="create_db_input/allBetas/Uterus.allBetas.txt"
i=0
for betafile in $(ls output/TW_Uterus_elasticNet_alpha0.5_1KG_snps_weights_chr*); do
	if [ $i -eq 0 ] ; then
		head -n 1 $betafile > $allBetas
		i=1
	fi
	tail -n +2 $betafile >> $allBetas
done

