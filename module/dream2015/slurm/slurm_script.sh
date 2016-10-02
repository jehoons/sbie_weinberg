#!/bin/bash
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************
#   SBATCH -o myjob.%A.%a.%j.out 
#SBATCH -o myjob.%a.out 
#   SBATCH -D /home/hpc/.../.../mydir 
#SBATCH -J pbsjob
#SBATCH --get-user-env 
#SBATCH --nodes=1
# CPUS-PER-TASK: 
# --cpus-per-task=NUMBER is should be linked with 'export OMP_NUM_THREADS=NUMBER'
#SBATCH --cpus-per-task=1 
#   SBATCH --mail-type=end 
#   SBATCH --mail-user=xyz@xyz.de 
#   SBATCH --export=NONE 
#SBATCH --array=0-199
#SBATCH --time=08:00:00 

#export OMP_NUM_THREADS=1

. ~/env2/bin/activate 
inputfile="INPUT_PART_${SLURM_ARRAY_TASK_ID}.csv"
outputfile=`echo ${inputfile} | sed 's/INPUT_/OUTPUT_/g'`
python main.py ${inputfile} ${outputfile} 

