#!/bin/bash
# Script to concatenate covariance fiels split by chromosome together

tissue=$1
allCovariances=$2
echo "GENE RSID1 RSID2 VALUE" > $allCovariances
for covfile in $(ls ../data/intermediate/model_by_chr/${tissue}_chr*_snpset_hapmap_snps_alpha_0.5_covariances.txt); do
	cat $covfile >> $allCovariances
done
