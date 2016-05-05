#! /usr/bin/env python

import sys
import os

'''
Script to split a SNP annotation file into multiple files by chromosome.

From commandline, first argument is the snp annotation file.

In splitting, toss out all non-biallelic SNP rows.
'''

annot_file = sys.argv[1]
annot_file_name = os.path.basename(annot_file)

# Make New File Names
# Expected annotation file ends in .txt
snps_by_chr_files= [os.path.join('data', 'intermediate', 'annotations', 'snp_annotation', annot_file_name[:-3] + 'chr' + str(i) + '.txt') for i in range(1,23)]
snp_by_chr = [open(f, 'w') for f in snps_by_chr_files]

with open(annot_file, 'r') as annot:
    # Write header in each file
    annot.readline()
    header = '\t'.join(['chr', 'pos', 'varID', 'refAllele', 'effectAllele', 'rsid']) + '\n'
    for f in snp_by_chr:
        f.write(header)

    for line in annot:
        attributes = line.split()
        chr = attributes[0]
        if len(attributes[3]) > 1 or len(attributes[4]) > 1:
            continue
        try:
            index = int(chr) - 1
            row = '\t'.join([attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[6]]) + '\n'
            snp_by_chr[index].write(row)
        except ValueError as e:
            continue

for f in snp_by_chr:
    f.close()
