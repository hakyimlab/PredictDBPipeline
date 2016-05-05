#!/bin/bash
###############################
# Resource Manager Directives #
###############################
### Set the name of the job
#PBS -N build_Uterus_model_db
### Select the shell you would like the script to execute within.
#PBS -S /bin/bash
### Inform the scheduler of the expected rutime, where
### walltime=HH:MM:SS.
#PBS -l walltime=3:00:00
### Inform the scheduler of the number of CPU cores for your job.
### This example will allocate two cores on a single node
#PBS -l nodes=1:ppn=2
### Inform the scheduler of the amount of memory you expect
### to use.  Use units of 'b', 'kb', 'mb', or 'gb'.
#PBS -l mem=5gb
### Set the destination for your program's output: stdout and stderr.
#PBS -o $HOME/${PBS_JOBNAME}.e${PBS_JOBID}
#PBS -e $HOME/${PBS_JOBNAME}.o${PBS_JOBID}

# Load Modules
module load python/2.7.9
#################
# Job Execution #
#################
# the program to be executed
cd /group/im-lab/nas40t2/scott/modelgeneration
./generate_sqlite_dbs.py --input_folder create_db_input/ --output_folder model_dbs --betas_include_clause .allBetas. --results_include_clause .allResults
