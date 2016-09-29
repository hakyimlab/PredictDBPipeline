#!/bin/bash
# Script to concatenate covariance fiels split by chromosome together

tissue=$1
allCovariances=$2
alpha=$3
snpset=$4
echo "GENE RSID1 RSID2 VALUE" > $allCovariances
for covfile in $(ls ../../data/intermediate/model_by_chr/${tissue}_chr*_${snpset}_alpha_${alpha}_covariances.txt); do
	cat $covfile >> $allCovariances
done
gzip $allCovariances

