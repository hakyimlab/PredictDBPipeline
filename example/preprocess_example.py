#!/usr/bin/env python

import os
import subprocess
import sys

INPUT_DIR = '../data/input/'
INTER_DIR = '../data/intermediate/'
OUTPUT_DIR = '../data/output/'
GENE_ANN_DIR = 'annotations/gene_annotation/'
SNP_ANN_DIR = 'annotations/snp_annotation/'
GENOTYPE_DIR = 'genotypes/'
EXPRESSION_DIR = 'expression_phenotypes/'


STUDY_NAMES = ['gEUVADIS']
GENE_ANNOTATION_FN = 'gencode.v12.genes.gtf'
SNP_ANNOTATION_FN = 'geuvadis.annot.txt'
GENOTYPE_FNS = ['geuvadis.snps.txt']
EXPRESSION_FNS = ['geuvadis.expr.txt']

GENE_ANNOT_INTER1 = 'gencode.v12.genes.parsed.txt'
GENE_ANNOT_INTER2 = 'gencode.v12.genes.parsed.RDS'

SNP_ANN_INTER_PREFIX1 = 'geuvadis.annot'
SNP_ANN_INTER_PREFIX2 = 'geuvadis.annot.chr'

GENOTYPE_INTER_PREFIX = ['geuvadis.snps']

EXPR_INTER = ['geuvadis']

SNPSET = 'HapMap'
ALPHA = '0.5'
N_K_FOLDS = '10'
RSID_LABEL = 'RSID_dbSNP137'
WINDOW = '1e6'

# Process gene annotation----------------------------------------------/
print("Parsing gene annotation...")
subprocess.call(
    ['../scripts/parse_gtf.py',
    INPUT_DIR + GENE_ANN_DIR + GENE_ANNOTATION_FN,
    INTER_DIR + GENE_ANN_DIR + GENE_ANNOT_INTER1
    ])
print("Turning gene annotation into RDS object")
subprocess.call(
    ['Rscript', '../scripts/geno_annot_to_RDS.R',
    INTER_DIR + GENE_ANN_DIR + GENE_ANNOT_INTER1,
    INTER_DIR + GENE_ANN_DIR + GENE_ANNOT_INTER2
    ])


# Process snp annotation-----------------------------------------------/
print("Splitting SNP annotation file up by chromosome...")
subprocess.call(
    ['../scripts/split_snp_annot_by_chr.py',
    INPUT_DIR + SNP_ANN_DIR + SNP_ANNOTATION_FN,
    INTER_DIR + SNP_ANN_DIR + SNP_ANN_INTER_PREFIX1
    ])
print("Saving each snp annotation file as RDS object")
subprocess.call(
    ['Rscript', '../scripts/snp_annot_to_RDS.R',
    INTER_DIR + SNP_ANN_DIR + SNP_ANN_INTER_PREFIX2])

# Process genotype files-----------------------------------------------/
print("Splitting genotype files up by chromosome...")
for i in range(len(GENOTYPE_FNS)):
    subprocess.call(
        ['../scripts/split_genotype_by_chr.py',
        INPUT_DIR + GENOTYPE_DIR + GENOTYPE_FNS[i],
        INTER_DIR + GENOTYPE_DIR + GENOTYPE_INTER_PREFIX[i]])

# Process expression files---------------------------------------------/
print("Transposing expression data and saving as RDS object...")
for i in range(len(EXPRESSION_FNS)):
    subprocess.call(
        ['Rscript', '../scripts/expr_to_transposed_RDS.R',
        INPUT_DIR + EXPRESSION_DIR + EXPRESSION_FNS[i],
        INTER_DIR + EXPRESSION_DIR + EXPR_INTER[i]])
    
# Create metadata files------------------------------------------------/
for i in range(len(STUDY_NAMES)):
    command = ' '.join(['../scripts/create_meta_data.py',
        '--geno', INPUT_DIR + GENOTYPE_DIR + GENOTYPE_FNS[i],
        '--expr', INPUT_DIR + EXPRESSION_DIR + EXPRESSION_FNS[i],
        '--snpset', SNPSET,
        '--alpha', ALPHA,
        '--n_k_folds', N_K_FOLDS,
        '--rsid_label', RSID_LABEL,
        '--window', WINDOW,
        '--out_prefix', OUTPUT_DIR + 'allMetaData/' + STUDY_NAMES[i]])
    subprocess.call(command, shell=True)
