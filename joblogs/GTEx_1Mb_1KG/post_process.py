#!/usr/bin/env python

import subprocess

from model_parameters import *

for i, study in enumerate(STUDY_NAMES):
    subprocess.call(
        ['../../scripts/make_all_results.sh',study,ALL_RESULTS_FILES[i],ALPHA,SNPSET])
    subprocess.call(
        ['../../scripts/make_all_betas.sh',study,ALL_BETAS_FILES[i],ALPHA,SNPSET])
    subprocess.call(['../../scripts/make_all_logs.sh',study,ALL_LOGS_FILES[i]])
    subprocess.call(
        ['../../scripts/make_all_covariances.sh',study,ALL_COVARIANCES_FILES[i],ALPHA,SNPSET])

for i, study, in enumerate(STUDY_NAMES):
    cmd = '../../scripts/make_sqlite_db.py --output {0} --betas {1} --results {2} --construction {3} --meta {4}'.format(
        DB_FILES[i], ALL_BETAS_FILES[i], ALL_RESULTS_FILES[i], ALL_LOGS_FILES[i], ALL_META_DATA_FILES[i])
    subprocess.call(cmd, shell=True)

# This chunk is not working on tarbell for some reason. Something with a
# mismatch between compiled and runtime versions of the RSQLite version.
# Had to run this chunk locally by mounting drive.
for i, study in enumerate(STUDY_NAMES):
    print("Filtering " + study + " on significance.")
    subprocess.call(['Rscript', '../../scripts/filter_on_significance.R', DB_FILES[i],
        INTER_DIR + GENE_ANN_DIR + GENE_ANNOT_INTER2, FILTERED_DB_FILES[i]])
