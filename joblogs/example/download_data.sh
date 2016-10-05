#!/usr/bin/env bash

# Download zipped tar file of input data.
curl -O https://s3.amazonaws.com/imlab-open/Data/PredictDB/predictdb_example.tar.gz

tar -zxvf predictdb_example.tar.gz

# Build directory tree
mkdir -pv \
    ../../data/input/annotations/gene_annotation/ \
    ../../data/input/annotations/snp_annotation/ \
    ../../data/input/expression_phenotypes/ \
    ../../data/input/genotypes/ \
    ../../data/intermediate/annotations/gene_annotation/ \
    ../../data/intermediate/annotations/snp_annotation/ \
    ../../data/intermediate/expression_phenotypes/ \
    ../../data/intermediate/genotypes/ \
    ../../data/intermediate/model_by_chr/ \
    ../../data/output/allBetas/ \
    ../../data/output/allCovariances/ \
    ../../data/output/allLogs/ \
    ../../data/output/allMetaData/ \
    ../../data/output/allResults/ \
    ../../data/output/dbs/ \

# Format expression, only include Europeans.
zless predictdb_example/GD462.GeneQuantRPKM.50FN.samplename.resk10.txt.gz | \
    cut -f1,5-284,374-466 > ../../data/input/expression_phenotypes/geuvadis.expr.txt
# Reduce gencode annotation to genes only
zless predictdb_example/gencode.v12.annotation.gtf.gz | \
    awk '$3 == "gene"' > ../../data/input/annotations/gene_annotation/gencode.v12.genes.gtf

# Decompress genotype and snp annotation and put in correct location.
gunzip -c predictdb_example/geuvadis.snps.txt > ../../data/input/genotypes/geuvadis.snps.txt
gunzip -c predictdb_example/geuvadis.annot.txt > ../../data/input/annotations/snp_annotation/geuvadis.annot.txt
