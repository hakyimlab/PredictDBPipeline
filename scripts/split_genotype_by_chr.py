#! /usr/bin/env python

import os
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
genotype_by_chr_files = [os.path.join('genotype_by_chr', geno_file_name[:-3] + "chr" + str(i) + ".biallelic.txt") for i in range(1,23)]
geno_by_chr = [open(f, 'w') for f in genotype_by_chr_files]

with open(geno_file, 'r') as geno:
    # Write header in each file
    header = geno.readline()
    snps = set()
    for f in geno_by_chr:
        f.write(header)

    for line in geno:
        # First attribute of each line is chr_pos_refAllele_effAllele_build
        polymorphism_id = (line.split()[0]).split('_')      
        if len(polymorphism_id[2]) > 1 or len(polymorphism_id[3]) > 1:
            continue
        snp = '_'.join(polymorphism_id)
        # Some SNPs have 2 rows for some reason. Attributes are nearly identical.
        # Only keep first one.
        if snp in snps:
            continue
        snps.add(snp)
        # Pull chromosome number and write line to appropriate file
        index = int(polymorphism_id[0]) - 1
        geno_by_chr[index].write(line)

for f in geno_by_chr:
    f.close()
