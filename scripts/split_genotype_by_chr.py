#! /usr/bin/env python

import os
import string
import sys

'''
Script to split a GTEx genotype file into multiple files by chromosome.

From commadline, first argument is the genotype file.

In splitting, toss out all non-biallelic SNP rows.
'''

geno_file = sys.argv[1]
geno_file_name = os.path.basename(geno_file)

# Make New File Names
# Expected genotype file ends in .txt
genotype_by_chr_files = [os.path.join('../data', 'intermediate', 'genotypes',
    string.replace(geno_file_name, "_Analysis", "_chr{}_Analysis".format(i))[:-3] + "biallelic.txt") for i in range(1,23)]

geno_by_chr = [open(f, 'w') for f in genotype_by_chr_files]
snp_complement = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}

with open(geno_file, 'r') as geno:
    # Write header in each file
    header = geno.readline()
    snps = set()
    for f in geno_by_chr:
        f.write(header)

    for line in geno:
        # First attribute of line is is chr_pos_refAllele_effAllele_build
        # Extract this attribute and parse into list
        varID_list = (line.split()[0].split('_'))
        chr = varID_list[0]
        refAllele = varID_list[2]
        effectAllele = varID_list[3]
        # Skip non_single letter polymorphisms
        if len(refAllele) > 1 or len(effectAllele) > 1:
            continue
        # Skip ambiguous strands
        if snp_complement[refAllele] == effectAllele:
            continue
        varID = '_'.join(varID_list)
        # Some snps have 2 rows for some reason. Attributes are nearly
        # identical. Only keep the first one found.
        if varID in snps:
            continue
        snps.add(varID)
        # Write line to appropriate file
        index = int(chr) - 1
        geno_by_chr[index].write(line)

for f in geno_by_chr:
    f.close()
