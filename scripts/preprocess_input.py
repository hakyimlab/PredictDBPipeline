#!/usr/bin/env python
#
# Script to preprocess all input data before making models.
# This can be run in an interactive qsub session (qsub -I) or submitted
# as a job to tarbell.  Only needs to be run once for a given set of
# input files.
#
# Author: Scott Dickinson <spdickinson88@gmail.com>

import glob
import os
import subprocess
import sys

input_dir = '../data/input/'
inter_dir = '../data/intermediate/'
output_dir = '../data/output/'

# Define all tissue models to make.
tissues = [f[:-18] for f in os.listdir(input_dir + 'genotypes/')]

# Process gene annotation----------------------------------------------/
# Extract chromosome number, gene id, gene name, gene start position,
# and gene end position from gene annotation file (gtf format)
gene_annot_stem = 'annotations/gene_annotation/gencode.v19.genes.no-exons.patched_contigs'
if not os.path.isfile(inter_dir + gene_annot_stem + '.parsed.txt'):
    print("Parsing gene annotation...")
    print "Using {} for gene_annotation".format(input_dir + gene_annot_stem + '.gtf')
    subprocess.call(['./parse_gtf.py', input_dir + gene_annot_stem + '.gtf',
        inter_dir + gene_annot_stem + '.parsed.txt'])
if not os.path.isfile(inter_dir + gene_annot_stem + '.parsed.RDS'):
    print("Turning gene annotation into RDS object...")
    subprocess.call(['Rscript', 'geno_annot_to_RDS.R', inter_dir + gene_annot_stem + '.parsed.txt',
        inter_dir + gene_annot_stem + '.parsed.RDS'])


# Process snp annotation-----------------------------------------------/
# Splits the snp annotation file by chromosome number, and turns each
# into an RDS object, to make it faster to read into R.
snp_annot_stem = 'annotations/snp_annotation/GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6'
if len(os.listdir(inter_dir + 'annotations/snp_annotation')) == 0:
    print("Splitting snp annotation by chromosome, turning each into RDS object...")
    subprocess.call(['./split_snp_annot_by_chr.py', input_dir + snp_annot_stem + '.txt'])
    subprocess.call(['Rscript', 'snp_annot_to_RDS.R'])


# Process genotypes----------------------------------------------------/
# For each tissue, split the genotype file into 22 files by chromosome,
# and only use rows for snps.
for tissue in tissues:
    if len(glob.glob(inter_dir + 'genotypes/' + tissue + '_chr*')) == 0:
        print("Splitting {} genotype by chromosome, pulling biallelic snps only...".format(tissue))
        subprocess.call(['./split_genotype_by_chr.py', input_dir + 'genotypes/' + tissue + '_Analysis.snps.txt'])

# Process expression phenotypes----------------------------------------/
# Transpose gene expression file to have people as rows, and genes as
# columns, and save as an RDS file. 
for tissue in tissues:
    expr_stem = 'expression_phenotypes/' + tissue + '_Analysis.expr'
    if not os.path.isfile(inter_dir + expr_stem + '.RDS'):
        if os.path.isfile(input_dir + 'expression_phenotypes/' + tissue + '_Analysis.covariates.txt'):
            print("Transposing {} expression file, adjusting for covariates and saving as RDS object...").format(tissue)
            subprocess.call(['Rscript', 'expr_to_transposed_RDS.R', input_dir + expr_stem + '.txt',
                inter_dir + expr_stem + '.RDS', input_dir + 'expression_phenotypes/' + tissue + '_Analysis.covariates.txt'])
        else:
            print("Transposing {} expression file and saving as RDS object...".format(tissue))
            subprocess.call(['Rscript', 'expr_to_transposed_RDS.R', input_dir + expr_stem + '.txt',
                inter_dir + expr_stem + '.RDS'])

# Make meta data file--------------------------------------------------/
# These text files contain info about the sample size, as well as some
# of the parameters that were used to build the model.
for tissue in tissues:
    if not os.path.isfile(output_dir + 'allMetaData/' + tissue + '.allMetaData.txt'):
        print("Making {} meta data file".format(tissue))
        subprocess.call(['Rscript', 'get_sample_size.R', tissue])
