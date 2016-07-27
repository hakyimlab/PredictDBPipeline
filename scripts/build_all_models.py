#!/usr/bin/env python
#
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
alpha = '0.5'
window = '1e6'
# Build model tissue by tissue, chromosome by chromosome--------------/
for tissue in tissues:
    if len(glob.glob(inter_dir + 'model_by_chr/TW_' + tissue + '_chr*')) == 0:
        for chrom in range(1, 23):
            print("Tissue: " + tissue + " chromosome: " + str(chrom))
            subprocess.call('qsub -v tissue={0},chrom={1},alpha={2},window={3} -N {0}_model_chr{1} build_tissue_by_chr.pbs'.format(tissue, str(chrom), alpha, window), shell=True)
            time.sleep(2)
