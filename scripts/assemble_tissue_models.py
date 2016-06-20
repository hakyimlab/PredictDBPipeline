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
