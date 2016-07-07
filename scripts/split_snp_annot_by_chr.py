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
snps_by_chr_files= [os.path.join('../data', 'intermediate', 'annotations', 'snp_annotation', annot_file_name[:-3] + 'chr' + str(i) + '.txt') for i in range(1,23)]
snp_by_chr = [open(f, 'w') for f in snps_by_chr_files]

snp_complement = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}

with open(annot_file, 'r') as ann:
    # Write header in each file
    ann.readline()
    header_attrs = ['chr','pos','varID','refAllele','effectAllele','rsid']
    header = '\t'.join(header_attrs)+'\n'
    for f in snp_by_chr:
        f.write(header)
    # Extract rows from input and write to body in appropriate output.
    for line in ann:
        attrs = line.split()
        chr = attrs[0]
        pos = attrs[1]
        varID = attrs[2]
        refAllele = attrs[3]
        effectAllele = attrs[4]
        rsid = attrs[6]
        # Skip non-single letter polymorphisms
        if len(refAllele) > 1 or len(effectAllele) > 1:
            continue
        # Skip ambiguous strands
        if snp_complement[refAllele] == effectAllele:
            continue
        if rsid == '.':
            continue
        index = int(chr) - 1
        row = '\t'.join([chr,pos,varID,refAllele,effectAllele,rsid])+'\n'
        snp_by_chr[index].write(row)
# Close each output
for f in snp_by_chr:
    f.close()
