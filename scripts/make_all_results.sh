#!/bin/bash
# Script to concatenate result files split by chromosome together.

allResults="create_db_input/allResults/Uterus.allResults.txt"
i=0
for resultsfile in $(ls output/working_TW_Uterus_exp_10-foldCV_elasticNet_alpha0.5_1KG_snps_chr*); do
        if [ $i -eq 0 ] ; then
                head -n 1 $resultsfile > $allResults
                i=1
        fi
        tail -n +2 $resultsfile >> $allResults
done
