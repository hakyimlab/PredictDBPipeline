#! /usr/bin/env python

import os
import sys

'''
Parses a gtf file to pull chromosome number, gene_id, gene_name, gene start
position, and gene end position, and put in a tab delimited file.

Runs from command line.  First argument is the gtf file, second is the
output file.
'''
try: 
    with open(sys.argv[1], 'r') as gtf:
        with open(sys.argv[2], 'w') as out:
            out_header = '\t'.join(['chr', 'gene_id', 'gene_name', 'start', 'end']) + '\n'
            out.write(out_header)
            for line in gtf:
                # Skip comments
                if line[0] == '#':
                    continue
                gene_fields = line.split('\t')
                gene_attributes = gene_fields[-1].split('; ')
                attr_dict = dict(attribute.split() for attribute in gene_attributes if attribute)
                # Some gtf files may have chromosome number with 'chr' prefix
                # Just want number.
                chr = gene_fields[0][3:] if "chr" in gene_fields[0] else gene_fields[0]
                start = gene_fields[3]
                end = gene_fields[4]
                id = attr_dict['gene_id'].strip('"')
                name = attr_dict['gene_name'].strip('"')
                out_line = '\t'.join([chr, id, name, start, end]) + '\n'
                out.write(out_line)
except IOError as e:
    print 'Operation failed: %s' % e.strerror
