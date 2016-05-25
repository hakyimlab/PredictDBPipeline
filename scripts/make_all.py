#!/usr/bin/env python

# Main script to build prediction model databases from source files
# to sqlite databases.
#
# Author: Scott Dickinson <spdickinson88@gmail.com>

import glob
import os
import subprocess
import sys
import time


input_dir = '../data/input/'
inter_dir = '../data/intermediate/'
output_dir = '../data/output/'

# Define all tissue models to make.
tissues = [f[:-18] for f in os.listdir(input_dir + 'genotypes/')]

# Process gene annotation---------------------------------------------/
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


# Process snp annotation----------------------------------------------/
# Splits the snp annotation file by chromosome number, and turns each
# into an RDS object, to make it faster to read into R.
snp_annot_stem = 'annotations/snp_annotation/GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6'
if len(os.listdir(inter_dir + 'annotations/snp_annotation')) == 0:
    print("Splitting snp annotation by chromosome, turning each into RDS object...")
    subprocess.call(['./split_snp_annot_by_chr.py', input_dir + snp_annot_stem + '.txt'])
    subprocess.call(['Rscript', 'snp_annot_to_RDS.R'])


# Process genotypes---------------------------------------------------/
# For each tissue, split the genotype file into 22 files by chromosome,
# and only use rows for snps.
for tissue in tissues:
    if len(glob.glob(inter_dir + 'genotypes/' + tissue + '_chr*')) == 0:
        print("Splitting {} genotype by chromosome, pulling biallelic snps only...".format(tissue))
        subprocess.call(['./split_genotype_by_chr.py', input_dir + 'genotypes/' + tissue + '_Analysis.snps.txt'])

# Process expression phenotypes---------------------------------------/
# Transpose gene expression file to have people as rows, and genes as
# columns, and save as an RDS file. 
for tissue in tissues:
    expr_stem = 'expression_phenotypes/' + tissue + '_Analysis.expr'
    if not os.path.isfile(inter_dir + expr_stem + '.RDS'):
        print("Transposing {} expression file and saving as RDS object...".format(tissue))
        subprocess.call(['Rscript', 'expr_to_transposed_RDS.R', input_dir + expr_stem + '.txt',
            inter_dir + expr_stem + '.RDS'])

# Make meta data file-------------------------------------------------/
# These text files contain info about the sample size, as well as some
# of the parameters that were used to build the model.
for tissue in tissues:
    if not os.path.isfile(output_dir + 'allMetaData/' + tissue + '.allMetaData.txt'):
        print("Making {} meta data file".format(tissue))
        subprocess.call(['Rscript', 'get_sample_size.R', tissue])

# Build model tissue by tissue, chromosome by chromosome--------------/
for tissue in tissues:
    if len(glob.glob(inter_dir + 'model_by_chr/TW_' + tissue + '_chr*')) == 0:
        for chrom in range(1, 23):
            subprocess.call('qsub -v tissue={0},chrom={1} -N build_{0}_model_chr{1} build_tissue_by_chr.pbs'.format(tissue, str(chrom)), shell=True)
            time.sleep(2)

#sys.exit()

# Cat tissue models split by chromosome together, so only one file per tissue
for tissue in tissues:
    allResultsFile = output_dir + 'allResults/' + tissue + '.allResults.txt'
    allBetasFile = output_dir + 'allBetas/' + tissue + '.allBetas.txt'
    allLogsFile = output_dir + 'allLogs/' + tissue + '.allLogs.txt'
    if not os.path.isfile(allResultsFile):
        subprocess.call(['./make_all_results.sh', tissue, allResultsFile])
    if not os.path.isfile(allBetasFile):
        subprocess.call(['./make_all_betas.sh', tissue, allBetasFile])
    if not os.path.isfile(allLogsFile):
        subprocess.call(['./make_all_logs.sh', tissue, allLogsFile])

# Make databases
if len(os.listdir(output_dir + 'dbs/')) == 0:
    subprocess.call('qsub -N build_model_dbs generate_db_job.pbs'.format(tissue), shell=True)

