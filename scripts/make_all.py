#!/usr/bin/env python

# Main script to build prediction model databases from source files to sqlite databases
# Author: Scott Dickinson <spdickinson88@gmail.com>

import glob
import os
import subprocess
import sys
import time


input_dir = '../data/input/'
inter_dir = '../data/intermediate/'

# Process Gene Annotation
gene_annot_stem = 'annotations/gene_annotation/gencode.v19.genes.no-exons.patched_contigs'
if not os.path.isfile(inter_dir + gene_annot_stem + '.txt'):
    print("Parsing gene annotation...")
    print "Using {} for gene_annotation".format(input_dir + gene_annot_stem + '.gtf')
    assert os.path.isfile(input_dir + gene_annot_stem + '.gtf')
    subprocess.call(['./parse_gtf.py', input_dir + gene_annot_stem + '.gtf',
        inter_dir + gene_annot_stem + '.txt'])
if not os.path.isfile(inter_dir + gene_annot_stem + '.RDS'):
    print("Turning gene annotation into RDS object...")
    subprocess.call(['Rscript', 'geno_annot_to_RDS.R', inter_dir + gene_annot_stem + '.txt',
        inter_dir + gene_annot_stem + '.RDS'])

# Process SNP Annotation
snp_annot_stem = 'annotations/snp_annotation/GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6'
if len(os.listdir(inter_dir + 'annotations/snp_annotation')) == 0:
    print("Splitting snp annotation by chromosome, turning each into RDS object...")
    subprocess.call(['./split_snp_annot_by_chr.py', input_dir + snp_annot_stem + '.txt'])
    subprocess.call(['Rscript', 'snp_annot_to_RDS.R'])

# Define Tissues
tissues = [
    'Prostate',
    'Uterus'
]

# Process genotypes
for tissue in tissues:
    if len(glob.glob(inter_dir + 'genotypes/' + tissue + '_chr*')) == 0:
        print("Splitting {} genotype by chromosome, pulling biallelic snps only...".format(tissue))
        subprocess.call(['./split_genotype_by_chr.py', input_dir + 'genotypes/' + tissue + '_Analysis.snps.txt'])

# Process expression phenotypes
for tissue in tissues:
    expr_stem = 'expression_phenotypes/' + tissue + '_Analysis.expr'
    if not os.path.isfile(inter_dir + expr_stem + '.RDS'):
        print("Transposing {} expression file and saving as RDS object...".format(tissue))
        subprocess.call(['Rscript', 'expr_to_transposed_RDS.R', input_dir + expr_stem + '.txt',
            inter_dir + expr_stem + '.RDS'])

# Build model tissue by tissue, chromosome by chromosome
for tissue in tissues:
    if len(glob.glob(inter_dir + 'model_by_chr/TW_' + tissue + '_chr*')) == 0:
        for chrom in range(1, 23):
            subprocess.call('qsub -v tissue={0},chrom={1} -N build_{0}_model_chr{1} build_tissue_by_chr.pbs'.format(tissue, str(chrom)), shell=True)
            time.sleep(2)

# Cat tissue models split by chromosome together, so only one file per tissue

# Make databases

# Clean up
