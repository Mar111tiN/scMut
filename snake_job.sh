#!/bin/bash

#$ -V
#$ -j y
#$ -N scMut
#$ -o logs
#$ -r yes
#$ -cwd
#$ -S /bin/bash
#$ -P control

export LOGDIR=/fast/users/${USER}/scratch/lox/scMut/${JOB_ID}
export TMPDIR=/fast/users/${USER}/scratch/tmp
# export WRKDIR=$HOME/work/projects/whWES

mkdir -p $LOGDIR

# somehow my environments are not set
# have to set it explicitly
conda activate scRNA-env
# outputs every output to the terminal
set -x

# !!! leading white space is important
DRMAA=" -pe smp {threads} -l h_rt=08:00:00 -l h_vmem=3g"
DRMAA="$DRMAA -V -P medium -o $LOGDIR/ -j yes"
snakemake --use-conda --drmaa "$DRMAA" -j 128 -p -r -k
snakemake --dag | dot -Tsvg > dax/dag.svg
# -k ..keep going if job fails
# -p ..print out shell commands
