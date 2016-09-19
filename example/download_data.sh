#!/usr/bin/env bash

# Download gEUVADIS expression data
curl -O http://www.ebi.ac.uk/arrayexpress/files/E-GEUV-1/GD462.GeneQuantRPKM.50FN.samplename.resk10.txt.gz
# Download gencode v12 gene annotation
curl -O ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_12/gencode.v12.annotation.gtf.gz
# TODO: Download preprocessed gEUVADIS genotype data from hakyimlab aws


# Build directory tree
mkdir -pv ../joblogs \
    ../data/input/annotations/gene_annotation/ \
    ../data/input/annotations/snp_annotation/ \
    ../data/input/expression_phenotypes/ \
    ../data/input/genotypes/ \
    ../data/intermediate/annotations/gene_annotation/ \
    ../data/intermediate/annotations/snp_annotation/ \
    ../data/intermediate/expression_phenotypes/ \
    ../data/intermediate/genotypes/ \
    ../data/intermediate/model_by_chr/ \
    ../data/output/allBetas/ \
    ../data/output/allCovariances/ \
    ../data/output/allLogs/ \
    ../data/output/allMetaData/ \
    ../data/output/allResults/ \
    ../data/output/dbs/ \

# Format expression
zless GD462.GeneQuantRPKM.50FN.samplename.resk10.txt.gz | \
    cut -f1,5-466 > ../data/input/expression_phenotypes/geuvadis.expr.txt
# Reduce gencode annotation to genes only
zless gencode.v12.annotation.gtf.gz | \
    awk '$3 == "gene"' > ../data/input/annotations/gene_annotation/gencode.v12.genes.gtf
