#!/bin/bash
# author: Je-Hoon Song, song.jehoon@gmail.com
# 
# Usage: 
# sbatch batch_pydream.sh 

#   #SBATCH --nodelist=darwin
#SBATCH --exclude=tesla0

#SBATCH --job-name=dream2015

# Using ARRAY and corresponding OUTPUT pattern.  
# You can use -o, --output=<filename pattern>. For  example the filename pattern
# can be "slurm-%A_%a.out" or "slurm-%j.out". %A/%a is about array_job and %j is
# about single_job.  Therefore, if you are not using array then define output 
# pattern as follows: 
#   #SBATCH --output=slurm-%j.out
# If you use ARRAY, then define output pattern as follows: 
#SBATCH --array=1-1000
#SBATCH --output=slurm-%A_%a.out
#   #SBATCH --output=slurm-%j.out

#SBATCH --time=10:00:00

# If workdir is not set, then the location in which you submit is set to its 
# workdir.
#   #SBATCH --workdir=/tmp

#   #SBATCH --partition=kicp

#   #SBATCH --account=kicp

# NODES - if NODES is set to 2, then the job will be duplicated on two nodes,
# not parallelized across them as we would probably want. So, it is recommended
# to set NODES to 1.
#SBATCH --nodes=1

#SBATCH --ntasks-per-node=2
# openmp parallel is set to 2, thereby each task should be meant be n=4 tasks
# for each node. The option --ntasks-per-node=2 indicates this to sbatch.
# ref: http://www.umbc.edu/hpcf/resources-tara-2010/how-to-run-openmp.html
export OMP_NUM_THREADS=2

#   #SBATCH --exclusive

echo "computing node: `hostname`"

# Matlab path: 
# export PATH=/usr/local/MATLAB/R2013a/bin:$PATH

# The LOGFILE name and --output="output-pattern" should be match.
#   #SBATCH --output=slurm-%A_%a.out
LOGFILE="slurm-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out"
# LOGFILE="slurm-${SLURM_JOBID}.out"

# ORG is the location(host:path) where the job is submitted.
ORG="${SLURM_SUBMIT_HOST}:${SLURM_SUBMIT_DIR}"

SLURM_WD=`pwd`

echo "working directory: `pwd`"

INPUT=`printf "output%04d.json" ${SLURM_ARRAY_TASK_ID}`
OUTPUT=`printf "score%04d.json" ${SLURM_ARRAY_TASK_ID}`
DATA=`printf "score%04d_data.tar.gz" ${SLURM_ARRAY_TASK_ID}`

echo "input: ${INPUT}"
echo "output: ${OUTPUT}"
echo "data: ${DATA}"

python post_training.py ${INPUT} ${OUTPUT}

# After work, we return the result file to original server:path. 
scp -rpB ${OUTPUT} ${ORG}
scp -rpB ${DATA} ${ORG}

# We also return slurm execution log to original server:path. 
#scp -rpB ${SLURM_WD}/${LOGFILE} ${ORG}/slurm-${OUTPUT}.log

echo "Good bye!"

# clean after work
#cd ${SLURM_WD}
#rm -rf ${TEMP_WD}
#rm -f ${SLURM_WD}/${LOGFILE}

# trace 
# scp -rpB ${SLURM_WD}/${LOGFILE} ${SLURM_SUBMIT_HOST}:${SLURM_SUBMIT_DIR}
# exit 0

