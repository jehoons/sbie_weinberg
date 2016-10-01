#!/bin/bash
#   SBATCH -o myjob.%A.%a.%j.out 
#SBATCH -o myjob.%a.out 
#   SBATCH -D /home/hpc/.../.../mydir 
#SBATCH -J pbsjob
#SBATCH --get-user-env 
#SBATCH --nodes=1
# CPUS-PER-TASK: 
# --cpus-per-task is should be linked with 'OMP_NUM_THREADS' variable
#SBATCH --cpus-per-task=1 
#   SBATCH --mail-type=end 
#   SBATCH --mail-user=xyz@xyz.de 
#   SBATCH --export=NONE 
#SBATCH --array=0-199
#SBATCH --time=08:00:00 

#source /etc/profile.d/modules.sh
#cd mydir
#export OMP_NUM_THREADS=1

. ~/env2/bin/activate 
inputfile="inp_part_${SLURM_ARRAY_TASK_ID}.csv"
outputfile=`echo ${inputfile} | sed 's/inp_/out_/g'`
python main.py ${inputfile} ${outputfile} 


